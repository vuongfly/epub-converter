#!/usr/bin/env python3
"""
EPUB Converter for The Watcher Website
Converts saved HTML to EPUB format with table of contents
"""

import json
import os
import sys
from pathlib import Path
from urllib.parse import unquote
from bs4 import BeautifulSoup
from ebooklib import epub

def load_config(config_path="config.json"):
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found!")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{config_path}'!")
        sys.exit(1)

def read_html_file(file_path):
    """Read and parse HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return BeautifulSoup(f.read(), 'html.parser')
    except FileNotFoundError:
        print(f"Error: HTML file '{file_path}' not found!")
        sys.exit(1)

def extract_toc(soup):
    """Extract table of contents from HTML"""
    toc_items = []
    
    # Find TOC list items
    toc_lists = soup.find_all('li', class_='cursor-pointer')
    
    for item in toc_lists:
        link = item.find('a', class_='toc-link')
        if link and link.get('href'):
            # Extract chapter number and title
            divs = link.find_all('div')
            if len(divs) >= 2:
                chapter_num = divs[0].get_text(strip=True)
                chapter_title = divs[1].get_text(strip=True)
                chapter_id = link.get('href').split('#')[-1]
                
                toc_items.append({
                    'number': chapter_num,
                    'title': chapter_title,
                    'id': chapter_id
                })
    
    print(f"Found {len(toc_items)} chapters in TOC")
    return toc_items

def extract_chapter_content(soup, chapter_id, next_chapter_id=None):
    """Extract content for a specific chapter"""
    # URL decode the chapter ID
    chapter_id = unquote(chapter_id)
    if next_chapter_id:
        next_chapter_id = unquote(next_chapter_id)
    
    # Find the heading with the chapter ID
    heading = soup.find(id=chapter_id)
    if not heading:
        print(f"Warning: Chapter '{chapter_id}' not found!")
        return ""
    
    # Find the parent div containing this chapter's content
    content_div = heading.find_parent('div', class_='wp-content')
    if not content_div:
        print(f"Warning: Content div not found for '{chapter_id}'!")
        return ""
    
    # Start with the heading
    content_html = f"<h2>{heading.get_text()}</h2>\n"
    
    # Collect all content until next chapter or end
    current = content_div
    while current:
        # Get all wp-content divs from this point
        for elem in current.find_all(['h2', 'p', 'blockquote', 'ul', 'ol']):
            # Stop if we hit the next chapter
            if next_chapter_id and elem.get('id') == next_chapter_id:
                return content_html
            
            # Skip the current heading (already added)
            if elem.get('id') == chapter_id:
                continue
            
            # Add the element HTML
            content_html += str(elem) + "\n"
        
        # Move to next wp-content div
        next_div = current.find_next_sibling('div')
        if next_div and 'wp-content' in next_div.get('class', []):
            current = next_div
        else:
            break
    
    return content_html

def clean_html_content(html_content):
    """Clean and format HTML content"""
    # Remove empty paragraphs with only &nbsp;
    html_content = html_content.replace('<p>&nbsp;</p>', '')
    html_content = html_content.replace('<p></p>', '')
    
    # Add basic CSS styling
    styled_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: serif; line-height: 1.6; }}
            h2 {{ text-align: center; margin: 2em 0 1em 0; }}
            p {{ text-align: justify; margin: 1em 0; }}
            strong {{ font-weight: bold; }}
            em {{ font-style: italic; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    return styled_html

def create_epub(toc_items, chapters_content, metadata, output_path):
    """Create EPUB file from chapters"""
    # Create EPUB book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('thewatcher_masterclass')
    book.set_title(metadata['title'])
    book.set_language(metadata['language'])
    book.add_author(metadata['author'])
    
    # Create chapters
    epub_chapters = []
    spine = ['nav']
    
    for i, (toc_item, content) in enumerate(zip(toc_items, chapters_content)):
        if not content:
            continue
            
        chapter_file = f"chapter_{i+1}.xhtml"
        chapter_title = f"{toc_item['number']}. {toc_item['title']}"
        
        # Clean content
        cleaned_content = clean_html_content(content)
        
        # Create chapter
        chapter = epub.EpubHtml(
            title=chapter_title,
            file_name=chapter_file,
            lang=metadata['language']
        )
        chapter.content = cleaned_content
        
        # Add chapter to book
        book.add_item(chapter)
        epub_chapters.append(chapter)
        spine.append(chapter)
    
    # Create table of contents
    book.toc = tuple(epub_chapters)
    
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Set spine
    book.spine = spine
    
    # Write EPUB file
    epub.write_epub(output_path, book)
    print(f"\nEPUB created successfully: {output_path}")

def main():
    """Main function"""
    print("=" * 60)
    print("EPUB Converter for The Watcher")
    print("=" * 60)
    
    # Load configuration
    print("\n1. Loading configuration...")
    config = load_config()
    
    # Construct paths
    input_folder = Path(config['input_folder'])
    html_file = input_folder / config['html_file']
    output_folder = Path(config['output_folder'])
    output_folder.mkdir(exist_ok=True)
    
    print(f"   Input folder: {input_folder}")
    print(f"   HTML file: {html_file}")
    print(f"   Output folder: {output_folder}")
    
    # Read HTML
    print("\n2. Reading HTML file...")
    soup = read_html_file(html_file)
    print("   HTML file loaded successfully")
    
    # Extract TOC
    print("\n3. Extracting table of contents...")
    toc_items = extract_toc(soup)
    
    if not toc_items:
        print("   Error: No chapters found in TOC!")
        sys.exit(1)
    
    for item in toc_items[:3]:  # Show first 3
        print(f"   - {item['number']}. {item['title']}")
    print(f"   ... and {len(toc_items) - 3} more chapters")
    
    # Extract chapter contents
    print("\n4. Extracting chapter contents...")
    chapters_content = []
    
    for i, toc_item in enumerate(toc_items):
        chapter_id = toc_item['id']
        next_chapter_id = toc_items[i+1]['id'] if i+1 < len(toc_items) else None
        
        print(f"   Processing: {toc_item['number']}. {toc_item['title']}")
        content = extract_chapter_content(soup, chapter_id, next_chapter_id)
        chapters_content.append(content)
    
    print(f"   Extracted {len(chapters_content)} chapters")
    
    # Create EPUB
    print("\n5. Creating EPUB file...")
    output_file = output_folder / f"{config['book_metadata']['title']}.epub"
    create_epub(toc_items, chapters_content, config['book_metadata'], output_file)
    
    print("\n" + "=" * 60)
    print("Conversion completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nConversion cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
