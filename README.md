# EPUB Converter cho The Watcher

Tool chuyển đổi trang web đã lưu thành file EPUB với mục lục đầy đủ.

## ✅ Đã hoàn thành

File EPUB đã được tạo thành công tại: `output/Masterclass: The perfect lifeskills.epub`

- 38 chương với nội dung đầy đủ
- Mục lục tương tác
- Format gốc (bold, italic, heading, bảng, ảnh)

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

## Chuẩn bị input

Mở trang web (đã đăng nhập), bấm Save Page As (Webpage, Complete) và lưu vào folder `input/` của project.
Tool sẽ tự lấy file `.html` đầu tiên trong `input/`, ảnh được đọc từ folder `*_files` đi kèm.

## Cấu hình

`config.json` chỉ còn tên folder output và thông tin sách:

```json
{
  "output_folder": "output",
  "book_metadata": {
    "title": "Masterclass: The perfect lifeskills",
    "author": "The Watcher",
    "language": "vi"
  }
}
```

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

File EPUB sẽ được tạo trong folder `output/`

## Output

File EPUB bao gồm:
- ✅ 38 chương với nội dung đầy đủ
- ✅ Mục lục (Table of Contents) tương tác
- ✅ Format gốc (bold, italic, headings)
- ✅ Có bảng và hình ảnh như trên web
- ✅ Tương thích với mọi ebook reader

## Cấu trúc project

```
epub-converter/
├── venv/                    # Virtual environment
├── input/                   # Trang web đã lưu (HTML + folder _files)
├── output/                  # EPUB output
│   └── Masterclass: The perfect lifeskills.epub
├── config.json              # Folder output và thông tin sách
├── convert.py               # Script chính
├── requirements.txt         # Python dependencies
├── run.sh                   # Script chạy nhanh (macOS/Linux)
├── run.bat                  # Script chạy nhanh (Windows)
└── README.md               # File này
```

## Troubleshooting

**Lỗi: "Config file not found"**
- Đảm bảo chạy từ folder chứa project

**Lỗi: "no .html file found"**
- Đảm bảo đã lưu trang web vào folder `input/`

**Lỗi: "Permission denied" (macOS/Linux)**
- Chạy: `chmod +x run.sh`

**Windows: "venv\Scripts\activate" không chạy**
- Mở PowerShell/CMD as Administrator
- Hoặc chạy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Yêu cầu hệ thống

- macOS/Linux/Windows 
- Python 3.7+
- Quyền đọc/ghi file
