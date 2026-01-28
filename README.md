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

## 🏃 Usage

### 🪟 On Windows

**Option 1 (Easiest):**
Double-click the **`convert_md_to_pdf.bat`** file.

**Option 2 (Command Line):**

```cmd
.\convert_md_to_pdf.bat
```

### 🍎 On macOS / 🐧 On Linux (Ubuntu, CentOS...)

1.  **Grant permission** (First time only):

    ```bash
    chmod +x convert_md_to_pdf.sh
    ```

2.  **Run the script**:
    ```bash
    ./convert_md_to_pdf.sh
    ```

---

## ❓ Troubleshooting

**1. "Node.js is NOT installed" error:**

- Please install Node.js from the link in Prerequisites.
- On Linux, you can run: `sudo apt install nodejs npm`

**2. "Puppeteer / Sandbox" errors on Linux:**

- The tool automatically adds `--no-sandbox` flag when running on Linux to fix this. If you still see errors, ensure you are running the latest version of this script (`md_to_pdf.py`).

**3. "File not found" or "Command not found":**

- Ensure you are inside the directory containing the scripts before running commands.

---

**Author**: KhoiBui16
