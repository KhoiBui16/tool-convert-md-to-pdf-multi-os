import os
import sys
import subprocess
import glob
import shutil
import platform

def check_dependencies():
    """Check if Node.js/npx is installed."""
    print("[INIT] Checking system requirements...")
    
    # 1. Detect OS
    os_name = platform.system()
    print(f"   -> Operating System: {os_name}")
    
    # 2. Check Node.js / npx
    # shutil.which works cross-platform to find executables
    npx_path = shutil.which("npx")
    
    if npx_path:
        print(f"   -> Node.js (npx) found: {npx_path}")
        return True
    else:
        print("\n[!] CRITICAL ERROR: Node.js is NOT installed or not in PATH.")
        print("    To use this tool, you must install Node.js:")
        if os_name == "Windows":
             print("    -> Download: https://nodejs.org/en/download/ (Select Windows Installer)")
        elif os_name == "Darwin": # macOS
             print("    -> Run: brew install node")
        else: # Linux
             print("    -> Run: sudo apt install nodejs npm")
        return False

def get_valid_directory():
    """Ask user for directory, default to current."""
    while True:
        print(f"\n[?] Current Folder: {os.getcwd()}")
        path = input(">> Enter folder path containing .md files (Press Enter to use current): ").strip()
        if path == "":
            return os.getcwd()
        
        if os.path.isdir(path):
            return path
        else:
            print(f"[!] Path does not exist: {path}")

def main():
    print("==================================================")
    print("   CROSS-PLATFORM MD TO PDF CONVERTER             ")
    print("==================================================")

    # 0. Check Environment
    if not check_dependencies():
        input("\nPress Enter to exit...")
        return

    # 1. Select Directory
    work_dir = get_valid_directory()
    try:
        os.chdir(work_dir)
        print(f"\n[INFO] Working in: {work_dir}")
    except Exception as e:
        print(f"[!] Error changing directory: {e}")
        return

    # 2. List MD Files
    md_files = glob.glob("*.md")
    if not md_files:
        print("[!] No markdown (.md) files found in this folder.")
        return

    print(f"\n[LIST] Found {len(md_files)} files:")
    for i, f in enumerate(md_files):
        print(f"  {i+1}. {f}")

    # 3. Select Files
    print("\n[?] Select files to convert:")
    print("    - Type 'all' to convert everything.")
    print("    - Type numbers separated by comma (e.g., 1,3,4).")
    choice = input(">> Your choice: ").strip().lower()

    selected_files = []
    if choice == 'all':
        selected_files = md_files
    else:
        try:
            indices = [int(x.strip()) for x in choice.split(',') if x.strip().isdigit()]
            for idx in indices:
                if 1 <= idx <= len(md_files):
                    selected_files.append(md_files[idx-1])
        except ValueError:
            print("[!] Invalid input.")
            return

    if not selected_files:
        print("[!] No files selected.")
        return

    # 4. Construct Command
    # Quote filenames to handle spaces safely on all OSs
    quoted_files = [f'"{f}"' for f in selected_files]
    file_args = " ".join(quoted_files)
    
    # OS-specific adjustments
    # Linux often requires --no-sandbox for available Chrome/Puppeteer
    extra_flags = ""
    if platform.system() == "Linux":
        print("\n[INFO] Linux detected: Adding --no-sandbox to fix Puppeteer crash.")
        # Note: We use single quotes for the JSON string to avoid shell issues on Linux
        extra_flags = " --launch-options '{\"args\": [\"--no-sandbox\"]}'"

    command = f"npx md-to-pdf{extra_flags} {file_args}"
    
    print(f"\n[EXEC] Running conversion command...")
    print(f" > {command}")
    print("-" * 50)

    # 5. Execute
    try:
        # shell=True is generally required for npx on Windows cmd, 
        # and helpful on Linux to expand args properly
        subprocess.run(command, shell=True, check=True)
        print("-" * 50)
        print("\n[SUCCESS] Conversion completed! Check your PDF files.")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Command failed with exit code {e.returncode}.")
        print("Note: If 'npx' failed, try installing the tool globally: npm i -g md-to-pdf")
    except Exception as e:
        print(f"\n[EXCEPTION] {e}")

if __name__ == "__main__":
    main()
