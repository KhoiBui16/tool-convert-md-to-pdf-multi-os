#!/bin/bash
# Script convert PDF dành cho macOS và Linux (Ubuntu/CentOS...)

# 1. Kiem tra Python
if command -v python3 &>/dev/null; then
    python3 md_to_pdf.py
elif command -v python &>/dev/null; then
    python md_to_pdf.py
else
    echo "[ERROR] Python chưa được cài đặt (Python is not installed)."
    echo "Please install Python 3 first."
fi

# Giữ màn hình terminal sau khi chạy xong (cho macOS dễ đọc)
read -p "Press [Enter] key to exit..."
