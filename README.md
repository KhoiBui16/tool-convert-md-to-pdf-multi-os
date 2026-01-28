# 📄 Cross-Platform Markdown to PDF Converter

A robust, interactive tool to convert Markdown files (`.md`) into professional PDF documents using [md-to-pdf](https://github.com/simonhaenisch/md-to-pdf) (Puppeteer/Chromium).

Supports **Windows**, **macOS**, and **Linux** (including Ubuntu/CentOS).

---

## 🚀 Features

- **Cross-Platform**: Run on any OS with a consistent experience.
- **Smart Formatting**: Uses Chromium (headless Chrome) for perfect rendering of CSS, Fonts (Unicode/Vietnamese), and Layouts.
- **Interactive Menu**: Select specific files or convert all files in a folder.
- **Auto-Repair**: Automatically handles Linux sandbox issues (`--no-sandbox`).

---

## 🛠️ Prerequisites

Before running the tool, ensure you have the following installed:

1.  **Python 3.x**: [Download Python](https://www.python.org/downloads/)
2.  **Node.js** (includes `npx`): [Download Node.js](https://nodejs.org/en/download/)

_Note: You do not need to manually install `md-to-pdf`. The script uses `npx` to run it directly._

---

## 📥 Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/KhoiBui16/tool-convert-md-to-pdf-multi-os.git
cd tool-convert-md-to-pdf-multi-os
```

_(Or simply download the 3 files: `md_to_pdf.py`, `convert_md_to_pdf.bat`, `convert_md_to_pdf.sh`)_

---

## 📦 What is `packages.txt`?

This file is **crucial for Streamlit Community Cloud deployment**.

The conversion engine (`md-to-pdf`) uses **Puppeteer**, which launches a headless Chrome browser. On a cloud server (Linux), Chrome needs specific system libraries (like `libnss3`, `libatk1.0`) to run.

- **Local Machine**: You don't need this file because your computer likely already has Chrome or these libraries.
- **Streamlit Cloud**: This file tells the cloud server: _"Hey, please `apt-get install` these Chromium dependencies so my app doesn't crash."_

---

## 🏃 Usage

### 🌟 1. Web Interface (Streamlit) - **Recommended**

The new interface allows you to:

- **Upload** files directly (Works on Cloud).
- **Scan** local folders (Works on Desktop).
- **Download** PDFs instantly.

**Run Locally:**

```bash
pip install -r requirements.txt
streamlit run stream_pdf.py
```

**Deploy to Streamlit Cloud:**

1. Push this code to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your repo.
4. **Important**: The `packages.txt` file is automatically detected by Streamlit Cloud to install dependencies. You don't need to do anything extra!

---

### 💻 2. Command Line (Legacy)

If you prefer the old-school terminal way:

**🪟 On Windows:**
Double-click `convert_md_to_pdf.bat`.

**🍎/🐧 On macOS / Linux:**

```bash
chmod +x convert_md_to_pdf.sh
./convert_md_to_pdf.sh
```

---

## ❓ Troubleshooting

**1. "Node.js is NOT installed" error:**

- Please install Node.js from [nodejs.org](https://nodejs.org/).
- On Streamlit Cloud, checking `packages.txt` includes `nodejs`.

**2. "Puppeteer / Sandbox" errors:**

- The tool handles this automatically (`--no-sandbox`). If issues persist on Linux, check if `chromium` is installed.

**3. "File not found" or "Command not found":**

- Ensure you are inside the directory containing the scripts before running commands.

---

**Author**: KhoiBui16
