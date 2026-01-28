import os
import tempfile
import shutil
import platform
import subprocess
import zipfile
import base64
import streamlit as st

def check_dependencies():
    """Check if Node.js/npx is available."""
    npx_path = shutil.which("npx")
    return npx_path, platform.system()

def run_conversion_command(file_paths):
    """
    Run npx md-to-pdf on files, SKIPPING those that are already up-to-date.
    Returns: (success, stdout, stderr, count_new, count_skip)
    """
    to_process = []
    skipped = []
    
    for md_path in file_paths:
        pdf_path = os.path.splitext(md_path)[0] + ".pdf"
        # Check if PDF exists and is newer than MD file
        if os.path.exists(pdf_path):
            md_mtime = os.path.getmtime(md_path)
            pdf_mtime = os.path.getmtime(pdf_path)
            if pdf_mtime > md_mtime:
                skipped.append(md_path)
                continue
        to_process.append(md_path)
    
    # Run conversion ONLY for files that need it
    if to_process:
        quoted_files = [f'"{f}"' for f in to_process]
        file_args = " ".join(quoted_files)
        
        extra_flags = ""
        if platform.system() == "Linux":
            extra_flags = " --launch-options '{\"args\": [\"--no-sandbox\"]}'"
        
        command = f"npx md-to-pdf{extra_flags} {file_args}"
        
        try:
            # shell=True required for Windows to find npx sometimes, but also works on Linux
            process = subprocess.run(command, shell=True, capture_output=True, text=True)
            return process.returncode == 0, process.stdout, process.stderr, len(to_process), len(skipped)
        except Exception as e:
            return False, "", str(e), len(to_process), len(skipped)
    else:
        return True, "No files changed.", "", 0, len(skipped)

def create_zip(file_paths, zip_name="converted_docs.zip"):
    """Create a zip file from list of paths."""
    zip_path = os.path.join(os.path.dirname(file_paths[0]), zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in file_paths:
            if os.path.exists(file):
                 zipf.write(file, os.path.basename(file))
    return zip_path

def get_fixed_temp_dir():
    """Create a persistent temp directory for the project."""
    temp_dir = os.path.join(tempfile.gettempdir(), "md_to_pdf_pro_cache")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir

def display_pdf(file_path):
    """Embed PDF in Iframe with optimized height and zoom."""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Use #view=FitH to make PDF page fill the iframe width horizontally
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#view=FitH" class="pdf-viewer-frame"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
