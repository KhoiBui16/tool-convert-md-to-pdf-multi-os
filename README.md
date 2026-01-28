# 📄 Markdown to PDF Pro

A robust, premium Markdown-to-PDF converter with **Streamlit Web UI**. Powered by [md-to-pdf](https://github.com/simonhaenisch/md-to-pdf) (Puppeteer/Chromium) for pixel-perfect rendering.

Supports **Windows**, **macOS**, **Linux**, and **Streamlit Cloud** deployment.

---

## 🚀 Features

### Core Capabilities

- **Cross-Platform**: Works on Windows, macOS, Ubuntu/Linux with consistent experience.
- **Pixel-Perfect Rendering**: Uses Chromium (headless Chrome) for perfect CSS, Fonts (Unicode/Vietnamese), and Layouts.
- **Auto-Sandbox Fix**: Automatically handles Linux sandbox issues (`--no-sandbox`).

### UI/UX Highlights

- **Premium Design**: Animated gradient background, glassmorphism cards, modern typography.
- **Two-View SPA**: Dedicated **Home** (conversion) and **Viewer** (reading) views.
- **Zen Mode PDF Viewer**: Full-width, 90vh height iframe with `#view=FitH` for optimal reading.
- **Collapsible File Selector**: Expander-based table with checkboxes for easy batch selection.
- **Recursive Folder Scan**: Finds `.md` files in all subfolders automatically.

### Performance

- **Smart Caching**: Skips re-conversion of unchanged files based on modification time.
- **Persistent Temp Directory**: Converted files survive browser reloads.

---

## 📂 Project Structure

```
tool-convert-md-to-pdf-multi-os/
├── stream_pdf.py          # Main Streamlit App Entry Point
├── modules/
│   ├── __init__.py
│   ├── ui.py              # Home & Viewer rendering logic
│   ├── utils.py           # Conversion, ZIP, PDF display utilities
│   └── styles.py          # Premium CSS styling
├── requirements.txt       # Python dependencies (streamlit, pandas)
├── packages.txt           # Linux system packages for Streamlit Cloud
├── md_to_pdf.py           # (Legacy) CLI interactive script
├── convert_md_to_pdf.bat  # (Legacy) Windows shortcut
└── convert_md_to_pdf.sh   # (Legacy) macOS/Linux shortcut
```

---

## 🛠️ Prerequisites

1.  **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2.  **Node.js 16+** (includes `npx`): [Download Node.js](https://nodejs.org/)

> **Note**: You do NOT need to manually install `md-to-pdf`. The script uses `npx` to run it directly.

---

## 📥 Installation

```bash
# Clone repository
git clone https://github.com/KhoiBui16/tool-convert-md-to-pdf-multi-os.git
cd tool-convert-md-to-pdf-multi-os

# Create virtual environment (recommended)
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🏃 Usage

### Start the Web App

```bash
streamlit run stream_pdf.py
```

The app will open at `http://localhost:8501`.

### Cloud Upload Mode

1. Go to **☁️ Cloud / Upload** tab.
2. Drag & drop your `.md` files.
3. Click **🚀 Convert Now**.
4. View results in PDF Viewer or download ZIP.

### Local Batch Mode

1. Go to **💻 Local Batch** tab.
2. Enter local folder path containing `.md` files.
3. Use the **checkbox table** to select/deselect files.
4. Click **🚀 Convert Selected Files**.
5. Auto-redirect to Viewer for preview.

### PDF Viewer

- Navigate via sidebar **👁️ Open PDF Viewer** button.
- Select files from sidebar list.
- **Download All (.zip)** for batch export.
- **Download PDF** for individual file.

---

## ☁️ Streamlit Cloud Deployment

### Required Files

| File               | Purpose                                       |
| ------------------ | --------------------------------------------- |
| `requirements.txt` | Python packages (streamlit, pandas, watchdog) |
| `packages.txt`     | Linux apt packages for Chromium/Puppeteer     |

### What is `packages.txt`?

The conversion engine uses **Puppeteer**, which launches a headless Chrome browser. On Streamlit Cloud (Linux), Chrome needs specific system libraries.

```
chromium
libnss3
libatk1.0-0
libatk-bridge2.0-0
libcups2
libxkbcommon0
libxcomposite1
libxrandr2
libgbm1
libpango-1.0-0
libasound2
```

Without this file, the app will crash on Cloud deployment.

---

## ❓ Troubleshooting

**1. "Node.js is NOT installed" error:**

- Install Node.js from [nodejs.org](https://nodejs.org/).
- On Streamlit Cloud, ensure `packages.txt` includes `nodejs`.

**2. "Puppeteer / Sandbox" errors:**

- The tool handles this automatically (`--no-sandbox`).
- On Linux, ensure `chromium` is installed.

**3. PDF content appears small in viewer:**

- The viewer uses `#view=FitH` to fit page width.
- Use the browser's PDF zoom controls (`+`/`-`) to adjust.

**4. Files not persisting after reload:**

- The app uses a fixed temp directory (`md_to_pdf_pro_cache`).
- Files should persist across reloads automatically.

---

## 📋 Version History

| Version | Changes                                                        |
| ------- | -------------------------------------------------------------- |
| v3.3    | Modular codebase, collapsible file selector, Select All toggle |
| v3.2    | Recursive folder scan, data_editor table with checkboxes       |
| v3.1    | Zen Mode viewer, sidebar reordering, persistent cache          |
| v3.0    | SPA architecture (Home/Viewer), premium UI overhaul            |
| v2.0    | Streamlit Web UI, Cloud deployment support                     |
| v1.0    | CLI tool with interactive menu                                 |

---

## 👤 Author

**KhoiBui16**

- GitHub: [KhoiBui16](https://github.com/KhoiBui16)

---

## 📄 License

MIT License - Feel free to use and modify.
