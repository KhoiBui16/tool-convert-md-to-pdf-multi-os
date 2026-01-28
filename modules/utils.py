import os
import tempfile
import shutil
import platform
import subprocess
import zipfile
import base64
import streamlit as st

def is_cloud():
    """Detect if running on Streamlit Cloud."""
    return os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud" or "AMPLIFY_ID" in os.environ

def check_dependencies():
    """Check if Node.js/npx is available."""
    npx_path = shutil.which("npx")
    return npx_path, "Cloud" if is_cloud() else platform.system()

def run_conversion_command(file_paths, progress_callback=None):
    """
    Run md-to-pdf on files, SKIPPING those that are already up-to-date.
    Uses batches to prevent RAM crashes on large selections.
    """
    to_process = []
    skipped = []
    
    for md_path in file_paths:
        pdf_path = os.path.splitext(md_path)[0] + ".pdf"
        if os.path.exists(pdf_path):
            md_mtime = os.path.getmtime(md_path)
            pdf_mtime = os.path.getmtime(pdf_path)
            if pdf_mtime > md_mtime:
                skipped.append(md_path)
                continue
        to_process.append(md_path)
    
    if not to_process:
        return True, "No files changed.", "", 0, len(skipped)

    # BATCHED PROCESSING (e.g., 5 files at a time to stay under RAM limits)
    batch_size = 5
    total_new = len(to_process)
    
    extra_flags = ""
    if platform.system() == "Linux":
        extra_flags = " --launch-options '{\"args\": [\"--no-sandbox\"]}'"

    success_all = True
    all_out, all_err = "", ""
    
    for i in range(0, total_new, batch_size):
        batch = to_process[i:i+batch_size]
        quoted_files = [f'"{f}"' for f in batch]
        file_args = " ".join(quoted_files)
        
        # Prefer local node_modules if present (much faster)
        binary = "npx md-to-pdf"
        if os.path.exists("node_modules/.bin/md-to-pdf"):
            binary = "node_modules/.bin/md-to-pdf" if platform.system() != "Windows" else "node_modules\\.bin\\md-to-pdf.cmd"

        command = f"{binary}{extra_flags} {file_args}"
        
        if progress_callback:
            progress_callback(i / total_new, f"Converting batch {i//batch_size + 1}...")

        try:
            # shell=True required for Windows/npx
            process = subprocess.run(command, shell=True, capture_output=True, text=True)
            all_out += process.stdout
            all_err += process.stderr
            if process.returncode != 0:
                success_all = False
        except Exception as e:
            all_err += f"\nRuntime Error: {str(e)}"
            success_all = False
            
    return success_all, all_out, all_err, total_new, len(skipped)

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
