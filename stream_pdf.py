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
    
# --- REUSABLE RESULTS DISPLAY ---
def show_results(file_list_tuples):
    """
    Display results UI (Zip, Preview, Download) for a list of (md_path, pdf_path).
    """
    if not file_list_tuples:
        return

    st.divider()
    st.subheader("🎉 Results")
    
    # 1. Download All Zip
    pdf_list = [p[1] for p in file_list_tuples]
    if pdf_list:
        try:
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
        except Exception as e:
            st.warning(f"Could not create ZIP: {e}")

    # 2. Individual Files List
    for md_path, pdf_path in file_list_tuples:
        file_name = os.path.basename(pdf_path)
        
        # Check if file exists before trying to open
        if not os.path.exists(pdf_path):
            st.error(f"File not found: {pdf_path}")
            continue

        with st.expander(f"📄 {file_name}", expanded=False):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.write("**Actions:**")
                # Download Button
                try:
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=f,
                            file_name=file_name,
                            mime="application/pdf",
                            key=f"dl_{file_name}_{os.path.getmtime(pdf_path)}" # Unique key
                        )
                except Exception as e:
                    st.error(f"Read error: {e}")
            
            with col2:
                st.write("**Preview:**")
                try:
                    display_pdf(pdf_path)
                except Exception as e:
                    st.warning(f"Preview unavailable: {e}")

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
    1. **Choice Mode**: Cloud Upload or Local Folder.
    2. **Convert**: Click the magic button.
    3. **Preview & Download**: View results instantly.
    """)

# TABS
tab_cloud, tab_local = st.tabs(["☁️ Upload & Convert", "📂 Local Batch Mode"])

# --- TAB 1: CLOUD / UPLOAD MODE ---
with tab_cloud:
    st.info("📂 **Project Workspace**: Upload files here. They will be processed in a temporary environment.")

    uploaded_files = st.file_uploader(
        "Drop Markdown files here:", 
        type=["md"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("🚀 Start Conversion (Cloud)", type="primary"):
            st.session_state.processed_files = [] # Reset
            
            progress_bar = st.progress(0)
            status_container = st.status("Processing...", expanded=True)
            
            input_paths = []
            
            # Save to Temp
            for i, uploaded_file in enumerate(uploaded_files):
                safe_name = uploaded_file.name
                save_path = os.path.join(st.session_state.temp_dir, safe_name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                input_paths.append(save_path)
                status_container.write(f"📄 Uploaded: `{safe_name}`")
            
            # Convert
            status_container.write("⚙️ Engine Running...")
            success, out, err = run_conversion_command(input_paths)
            progress_bar.progress(100)
            
            if success:
                status_container.update(label="✅ Cloud Conversion Complete!", state="complete", expanded=False)
                # Collect Results
                results = []
                for md_path in input_paths:
                    pdf_path = os.path.splitext(md_path)[0] + ".pdf"
                    if os.path.exists(pdf_path):
                        results.append((md_path, pdf_path))
                st.session_state.processed_files = results
            else:
                status_container.update(label="❌ Failed", state="error")
                st.error(err)

    # Display Cloud Results
    if st.session_state.processed_files:
        show_results(st.session_state.processed_files)


# --- TAB 2: LOCAL MODE ---
with tab_local:
    st.warning("⚠️ **Local Mode**: Edits files directly on your disk.")
    
    if 'local_results' not in st.session_state:
        st.session_state.local_results = []

    if 'local_path' not in st.session_state:
        st.session_state.local_path = os.getcwd()

    c1, c2 = st.columns([4, 1])
    path_in = c1.text_input("Local Folder Path:", st.session_state.local_path)
    if c2.button("Reload"):
        st.session_state.local_path = path_in
        st.rerun()

    if os.path.isdir(path_in):
        os.chdir(path_in)
        
        # --- NEW: LIST ALL FILES ---
        all_files = [f for f in os.listdir('.') if os.path.isfile(f)]
        if all_files:
            with st.expander("📂 View Files in Folder", expanded=True):
                file_data = []
                for f in all_files:
                    try:
                        size_kb = os.path.getsize(f) / 1024
                        file_data.append({
                            "File Name": f, 
                            "Size (KB)": f"{size_kb:.1f}", 
                            "Type": os.path.splitext(f)[1]
                        })
                    except:
                        pass
                st.dataframe(file_data, use_container_width=True, hide_index=True)

        mds = glob.glob("*.md")
        
        if mds:
            col_sel1, col_sel2 = st.columns([3,1])
            with col_sel1:
                sel = st.multiselect("Select Files:", mds, default=mds)
            with col_sel2:
                st.write("")
                st.write("")
                if st.button("🚀 Convert Local", type="primary", disabled=not sel):
                    st.session_state.local_results = [] # Reset
                    
                    with st.status("Converting locally...", expanded=True) as status:
                        # 1. Convert
                        s, o, e = run_conversion_command(sel)
                        
                        if s:
                            status.update(label="✅ Local Conversion Done!", state="complete", expanded=False)
                            # 2. Collect Results (Absolute Paths)
                            results = []
                            for f in sel:
                                abs_md = os.path.abspath(f)
                                abs_pdf = os.path.splitext(abs_md)[0] + ".pdf"
                                if os.path.exists(abs_pdf):
                                    results.append((abs_md, abs_pdf))
                            st.session_state.local_results = results
                        else:
                            status.update(label="❌ Failed", state="error")
                            st.error(e)
            
            # Display Local Results using the SAME function
            if st.session_state.local_results:
                st.info(f"📂 Output Folder: `{path_in}`")
                show_results(st.session_state.local_results)
                
        else:
            st.info("No .md files found in this folder.")
    else:
        st.error("Invalid path.")
