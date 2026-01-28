import streamlit as st
import os
import subprocess
import shutil
import platform
import glob
import tempfile
import base64
import zipfile
from pathlib import Path

# --- CONFIGURATION ---
st.set_page_config(
    page_title="PDF Converter Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING ---
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 5px;
    }
    div[data-testid="stExpander"] {
        border-radius: 8px;
        border: 1px solid #ddd;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def check_dependencies():
    """Check if Node.js/npx is available."""
    npx_path = shutil.which("npx")
    return npx_path, platform.system()

def run_conversion_command(file_paths):
    """Run npx md-to-pdf on selected files."""
    quoted_files = [f'"{f}"' for f in file_paths]
    file_args = " ".join(quoted_files)
    
    extra_flags = ""
    if platform.system() == "Linux":
        extra_flags = " --launch-options '{\"args\": [\"--no-sandbox\"]}'"
    
    command = f"npx md-to-pdf{extra_flags} {file_args}"
    
    try:
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        return process.returncode == 0, process.stdout, process.stderr
    except Exception as e:
        return False, "", str(e)

def display_pdf(file_path):
    """Embed PDF in Iframe for preview."""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" style="border:none; border-radius:8px;"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def create_zip(file_paths, zip_name="converted_docs.zip"):
    """Create a zip file from a list of files."""
    zip_path = os.path.join(os.path.dirname(file_paths[0]), zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in file_paths:
            zipf.write(file, os.path.basename(file))
    return zip_path

# --- SESSION STATE INITIALIZATION ---
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = [] # List of tuples: (md_path, pdf_path)
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp()
    
# --- MAIN UI ---
st.title("📄 Markdown to PDF Pro")
st.markdown("### Professional Converter & Viewer")
st.caption("Powered by **Puppeteer** (Chromium) | Optimized for Windows, Mac, Linux & Cloud")

# Sidebar Status
npx_path, os_name = check_dependencies()
with st.sidebar:
    st.markdown("### ⚙️ System Status")
    if npx_path:
        st.success(f"🟢 **Ready**\n\nOS: `{os_name}`")
    else:
        st.error("🔴 **Node.js Missing**")
        st.info("Please install Node.js to continue.")
        st.stop()
    
    st.divider()
    st.markdown("### 📝 Instructions")
    st.markdown("""
    1. **Upload** your `.md` files.
    2. Click **Convert**.
    3. **Preview** the PDF.
    4. **Download** individually or as ZIP.
    """)

# TABS
tab_cloud, tab_local = st.tabs(["☁️ Upload & Convert", "📂 Local Batch Mode"])

# --- TAB 1: CLOUD / UPLOAD MODE ---
with tab_cloud:
    st.info("📂 **Project Workspace**: Upload files here. They will be processed in a temporary `docs` environment.")

    uploaded_files = st.file_uploader(
        "Drop Markdown files here:", 
        type=["md"], 
        accept_multiple_files=True,
        help="You can upload multiple files at once."
    )
    
    if uploaded_files:
        col_action, col_status = st.columns([1, 4])
        with col_action:
            convert_btn = st.button("🚀 Start Conversion", type="primary", use_container_width=True)
        
        if convert_btn:
            # Clear previous results
            st.session_state.processed_files = []
            
            # Progress UI
            progress_bar = st.progress(0)
            status_container = st.status("Processing files...", expanded=True)
            
            input_paths = []
            
            # 1. Save uploads to Temp Session Directory
            for i, uploaded_file in enumerate(uploaded_files):
                safe_name = uploaded_file.name
                save_path = os.path.join(st.session_state.temp_dir, safe_name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                input_paths.append(save_path)
                status_container.write(f"📄 Uploaded: `{safe_name}`")
                progress_bar.progress((i + 1) / (len(uploaded_files) * 2))

            # 2. Convert
            status_container.write("⚙️ Running PDF Engine...")
            success, out, err = run_conversion_command(input_paths)
            
            progress_bar.progress(100)
            
            if success:
                status_container.update(label="✅ Conversion Complete!", state="complete", expanded=False)
                
                # Check results
                results = []
                for md_path in input_paths:
                    pdf_name = os.path.splitext(os.path.basename(md_path))[0] + ".pdf"
                    pdf_path = os.path.join(st.session_state.temp_dir, pdf_name)
                    if os.path.exists(pdf_path):
                        results.append((md_path, pdf_path))
                
                st.session_state.processed_files = results
            else:
                status_container.update(label="❌ Conversion Failed", state="error")
                st.error("Error Log:")
                st.code(err)

    # --- DISPLAY RESULTS (PERSISTENT) ---
    if st.session_state.processed_files:
        st.divider()
        st.subheader("🎉 Results")
        
        # Download All Zip
        pdf_list = [p[1] for p in st.session_state.processed_files]
        zip_path = create_zip(pdf_list)
        
        col_zip, _ = st.columns([1, 3])
        with col_zip:
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📦 Download All (ZIP)",
                    data=f,
                    file_name="converted_docs.zip",
                    mime="application/zip",
                    type="primary"
                )

        # Individual Files List
        for md_path, pdf_path in st.session_state.processed_files:
            file_name = os.path.basename(pdf_path)
            
            with st.expander(f"📄 {file_name}", expanded=False):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.write("**Actions:**")
                    # Download Button
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=f,
                            file_name=file_name,
                            mime="application/pdf",
                            key=f"dl_{file_name}"
                        )
                
                with col2:
                    st.write("**Preview:**")
                    display_pdf(pdf_path)

# --- TAB 2: LOCAL MODE ---
with tab_local:
    st.warning("⚠️ Local Mode interacts directly with your computer's folders (Not for Cloud Use).")
    
    if 'local_path' not in st.session_state:
        st.session_state.local_path = os.getcwd()

    c1, c2 = st.columns([4, 1])
    path_in = c1.text_input("Local Folder Path:", st.session_state.local_path)
    if c2.button("Reload"):
        st.session_state.local_path = path_in
        st.rerun()

    if os.path.isdir(path_in):
        os.chdir(path_in)
        mds = glob.glob("*.md")
        if mds:
            sel = st.multiselect("Select Files:", mds, default=mds)
            if st.button("Convert Selected", disabled=not sel):
                with st.status("Converting locally..."):
                    s, o, e = run_conversion_command(sel)
                    if s: st.success("Done!")
                    else: st.error(e)
        else:
            st.info("No .md files found.")
    else:
        st.error("Invalid path.")
