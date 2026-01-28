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

st## 📂 File Structure

Here is the explanation of the files in this repository:

| File                    | Description                                                                            |
| :---------------------- | :------------------------------------------------------------------------------------- |
| **`stream_pdf.py`**     | The main **Streamlit App**. Run this to start the UI.                                  |
| **`requirements.txt`**  | List of **Python libraries** (Streamlit, Watchdog) required to run the app.            |
| **`packages.txt`**      | List of **Linux System Packages** (Chromium, Libs) for **Streamlit Cloud** deployment. |
| `md_to_pdf.py`          | (Legacy) Interactive command-line script for Python.                                   |
| `convert_md_to_pdf.bat` | (Legacy) Windows shortcut to run the CLI tool.                                         |
| `convert_md_to_pdf.sh`  | (Legacy) macOS/Linux shortcut to run the CLI tool.                                     |

---

## 📦 What is `packages.txt`? (Important for Cloud)

This file is **crucial for Streamlit Community Cloud deployment**.

The conversion engine uses **Puppeteer**, which launches a headless Chrome browser. On a simplified cloud server (Linux), Chrome needs specific system libraries (like `libnss3`, `libatk1.0`) to run.

- **Local Machine**: You likely don't need this, as your OS handles these libraries.
- **Streamlit Cloud**: This file tells the server to run `apt-get install` for these dependencies. **Without it, the app will crash on Cloud.**

---

## 🔧 Setup Guide (Virtual Environment)

It is recommended to use a **Virtual Environment** (venv) instead of installing globally or using Conda.

### 🪟 On Windows

1.  **Create Environment**:

    ```cmd
    python -m venv venv
    ```

2.  **Activate**:

    ```cmd
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**:

    ```cmd
    pip install -r requirements.txt
    ```

4.  **Run App**:
    ```cmd
    streamlit run stream_pdf.py
    ```

### 🍎/🐧 On macOS / Linux (Ubuntu)

1.  **Create Environment**:

    ```bash
    python3 -m venv venv
    ```

2.  **Activate**:

    ```bash
    source venv/bin/activate
    ```

3.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run App**:
    ```bash
    streamlit run stream_pdf.py
    ```

---

## 🏃 Usage (Web Interface)

Once the app is running:

1.  **Upload Mode**: Drag & Drop MD files -> Convert -> Preview PDF -> Download ZIP.
2.  **Local Mode**: Select local folder -> Batch Convert -> **View & Download directly in UI**.

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
