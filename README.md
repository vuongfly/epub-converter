# EPUB Converter cho The Watcher

Tool chuyển đổi trang web đã lưu thành file EPUB với mục lục đầy đủ.

## ✅ Đã hoàn thành

File EPUB đã được tạo thành công tại: `output/Masterclass: The perfect lifeskills.epub`

- 18 chương với nội dung đầy đủ
- Mục lục tương tác
- Format gốc (bold, italic, heading)
- Kích thước: ~54KB

## Cài đặt (Chỉ cần làm 1 lần)

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Cấu hình

Chỉnh sửa file `config.json` nếu cần thay đổi đường dẫn:

```json
{
  "input_folder": "/Users/vuongfly/Downloads/Web the watcher",
  "html_file": "The Watcher.html",
  "output_folder": "output",
  "book_metadata": {
    "title": "Masterclass: The perfect lifeskills",
    "author": "The Watcher",
    "language": "vi"
  }
}
```

### Các tùy chọn config:

- **input_folder**: Đường dẫn folder chứa file HTML (thay đổi theo máy của bạn)
- **html_file**: Tên file HTML
- **output_folder**: Folder lưu EPUB output
- **book_metadata**: 
  - **title**: Tên sách trong EPUB
  - **author**: Tác giả
  - **language**: Mã ngôn ngữ (vi = Vietnamese)

## Sử dụng

### macOS/Linux

**Cách 1: Script nhanh (Khuyến nghị)**
```bash
./run.sh
```

**Cách 2: Chạy thủ công**
```bash
source venv/bin/activate
python convert.py
```

### Windows

**Cách 1: Script nhanh (Khuyến nghị)**
```batch
run.bat
```

**Cách 2: Chạy thủ công**
```batch
venv\Scripts\activate
python convert.py
```

**Lưu ý Windows**: Cần sửa đường dẫn trong `config.json`:
```json
"input_folder": "C:/Users/YourName/Downloads/Web the watcher"
```

File EPUB sẽ được tạo trong folder `output/`

## Output

File EPUB bao gồm:
- ✅ 18 chương với nội dung đầy đủ
- ✅ Mục lục (Table of Contents) tương tác
- ✅ Format gốc (bold, italic, headings)
- ✅ Không có hình ảnh (chỉ text theo yêu cầu)
- ✅ Tương thích với mọi ebook reader

## Cấu trúc project

```
epub-converter/
├── venv/                    # Virtual environment
├── output/                  # EPUB output
│   └── Masterclass: The perfect lifeskills.epub
├── config.json              # Cấu hình đường dẫn
├── convert.py               # Script chính
├── requirements.txt         # Python dependencies
├── run.sh                   # Script chạy nhanh (macOS/Linux)
├── run.bat                  # Script chạy nhanh (Windows)
└── README.md               # File này
```

## Chỉnh đường dẫn cho máy khác

Nếu muốn chạy trên máy khác hoặc với file HTML khác:

1. Mở `config.json`
2. Sửa `input_folder` thành đường dẫn folder chứa HTML của bạn
3. Chạy lại: `./run.sh`

## Troubleshooting

**Lỗi: "Config file not found"**
- Đảm bảo chạy từ folder chứa project

**Lỗi: "HTML file not found"**
- Kiểm tra đường dẫn trong `config.json`
- Đảm bảo file `The Watcher.html` tồn tại
- Windows: Dùng `C:/Users/...` hoặc `C:\Users\...`

**Lỗi: "Permission denied" (macOS/Linux)**
- Chạy: `chmod +x run.sh`

**Windows: "venv\Scripts\activate" không chạy**
- Mở PowerShell/CMD as Administrator
- Hoặc chạy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Yêu cầu hệ thống

- macOS/Linux/Windows 
- Python 3.7+
- Quyền đọc/ghi file
