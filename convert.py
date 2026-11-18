#!/usr/bin/env python3
"""
EPUB Converter for The Watcher Website
Converts saved HTML to EPUB format with table of contents
"""

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote
from bs4 import BeautifulSoup
from ebooklib import epub

def load_config(config_path=Path(__file__).parent / "config.json"):
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

def extract_chapters(soup, toc_items, base_dir):
    """Split the article into chapters. Each chapter starts at its <h2> and runs
    until the next <h2>, across ALL wp-content blocks (each block is a separate
    sibling-less div, so they must be walked in document order)."""
    toc_ids = [unquote(t['id']) for t in toc_items]
    chapters, current, images = {}, None, {}
    for div in soup.find_all('div', class_='wp-content'):
        for elem in div.find_all(recursive=False):
            if elem.name == 'h2' and elem.get('id') in toc_ids:
                current = chapters.setdefault(elem['id'], [f"<h2>{elem.decode_contents()}</h2>"])
            elif current is not None:
                for img in elem.find_all('img'):
                    src = unquote(img.get('src', ''))
                    path = (base_dir / src).resolve()
                    if path.is_file():
                        name = f"images/{path.name}"
                        images[name] = path
                        img['src'] = name
                        img.attrs.pop('style', None)
                    else:
                        print(f"Warning: image '{src}' not found, dropped")
                        img.decompose()
                current.append(str(elem))
    missing = [i for i in toc_ids if i not in chapters]
    if missing:
        print(f"Warning: headings not found: {missing}")
    return [("\n".join(chapters.get(i, [])) if i in chapters else "") for i in toc_ids], images

def clean_html_content(html_content):
    """Clean and format HTML content"""
    # Remove empty paragraphs with only &nbsp;
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.S)
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
            img {{ max-width: 100%; }}
            table, td {{ border: 1px solid #888; border-collapse: collapse; padding: 0.3em; }}
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

def create_epub(toc_items, chapters_content, metadata, output_path, images=None):
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
    
    for name, path in (images or {}).items():
        book.add_item(epub.EpubItem(file_name=name, media_type=f"image/{path.suffix.lstrip('.').lower().replace('jpg', 'jpeg')}", content=path.read_bytes()))

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
    
    # Input is always the ./input folder next to this script
    root = Path(__file__).parent
    input_folder = root / "input"
    html_files = sorted(input_folder.glob("*.html"))
    if not html_files:
        print(f"Error: no .html file found in '{input_folder}'!")
        sys.exit(1)
    html_file = html_files[0]
    output_folder = root / config['output_folder']
    output_folder.mkdir(exist_ok=True)

    print(f"   Input folder: {input_folder}")
    print(f"   HTML file: {html_file.name}")
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
    chapters_content, images = extract_chapters(soup, toc_items, input_folder)
    print(f"   Extracted {len(chapters_content)} chapters, {len(images)} images")

    # Create EPUB
    print("\n5. Creating EPUB file...")
    output_file = output_folder / f"{config['book_metadata']['title']}.epub"
    create_epub(toc_items, chapters_content, config['book_metadata'], output_file, images)
    
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
