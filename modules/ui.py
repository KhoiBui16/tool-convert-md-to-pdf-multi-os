import streamlit as st
import os
import glob
from modules.utils import run_conversion_command, create_zip, display_pdf, check_dependencies, is_cloud

def render_sidebar_shared(slot="bottom"):
    """Render shared sidebar elements (Status, Nav, Version)."""
    npx_path, os_name = check_dependencies()
    
    # Status
    st.markdown("### System Status")
    if npx_path:
        st.success(f"**Ready** (`{os_name}`)")
    else:
        st.error("🔴 **Node.js Missing**")
        st.stop()
    st.divider()

    # Navigation (Only needed if we are NOT in viewer, or as a secondary nav)
    # But user wants "Open PDF Viewer" in taskbar relative to Home.
    # We'll handle Nav logic in the main view functions or here contextually.
    
    if slot == "bottom":
        st.divider()
        st.caption("v3.3 Optimized | by KhoiBui16")

def render_home():
    st.title("📄 Markdown to PDF Pro")
    st.markdown("##### Professional Converter & Viewer")
    st.markdown("""
    <p style="color:#6b7280; font-size:15px; margin-top:-5px;">
    Transform your Markdown documents into beautifully styled PDFs. 
    Powered by <b>Puppeteer</b> engine for pixel-perfect rendering. 
    Supports <b>Windows, macOS, Linux</b> & Cloud Deployment.
    </p>
    """, unsafe_allow_html=True)
    st.divider()

    # SIDEBAR FOR HOME
    with st.sidebar:
        st.markdown("## 📄 PDF Pro")
        render_sidebar_shared(slot="top")
        
        st.divider()
        st.markdown("### 🧭 Navigation")
        if st.button("👁️ Open PDF Viewer", type="primary", use_container_width=True):
             st.session_state.current_view = "viewer"
             st.rerun()
        
        if st.session_state.processed_files:
            if st.button("🗑️ Clear History", use_container_width=True, help="Remove all files from the viewer session"):
                st.session_state.processed_files = []
                st.session_state.viewer_file = None
                st.success("History cleared!")
                st.rerun()

        st.divider()
        st.markdown("### 📝 Quick Guide")
        st.info("1. Upload/Select Files\n2. Convert\n3. Click **Viewer** to read")
        
        st.divider()
        st.caption("v3.3 Optimized | by KhoiBui16")

    tab_cloud, tab_local = st.tabs(["☁️ Cloud / Upload", "💻 Local Batch"])
    
    # --- CLOUD UPLOAD ---
    with tab_cloud:
        st.info("Files are processed in a secure temporary environment.")
        uploaded_files = st.file_uploader("Drop MD files here:", type=["md"], accept_multiple_files=True)
        
        if uploaded_files:
            if st.button("🚀 Convert Now", type="primary", use_container_width=True):
                with st.status("Processing...", expanded=True) as status:
                    input_paths = []
                    # Save files
                    for f in uploaded_files:
                        save_path = os.path.join(st.session_state.temp_dir, f.name)
                        with open(save_path, "wb") as w: w.write(f.getbuffer())
                        input_paths.append(save_path)
                    
                    status.write("⚙️ Running Engine...")
                    
                    # Progress logic
                    p_bar = st.progress(0, text="Starting...")
                    def up(p, t): p_bar.progress(p, text=t)
                    
                    s, o, e, new, skip = run_conversion_command(input_paths, progress_callback=up)
                    p_bar.empty()
                    
                    if s:
                        # Re-scan processed files from input
                        results = []
                        for md_p in input_paths:
                            pdf_p = os.path.splitext(md_p)[0] + ".pdf"
                            if os.path.exists(pdf_p): results.append((md_p, pdf_p))
                        
                        # UPDATE session state
                        existing_pdfs = {p[1] for p in st.session_state.processed_files}
                        for r in results:
                            if r[1] not in existing_pdfs:
                                st.session_state.processed_files.append(r)
                        
                        status.update(label=f"✅ Done! (Processed {new}, Cached {skip})", state="complete")
                    else:
                        status.update(label="❌ Failed", state="error")
                        st.error(e)

    # --- LOCAL BATCH ---
    with tab_local:
        if is_cloud():
            st.warning("⚠️ **Local Mode is for Desktop Only**")
            st.info("On Streamlit Cloud, the server cannot access your local files. Please use the **Cloud / Upload** tab instead.")
            st.expander("Why?", expanded=False).write("For security and technical reasons, web browsers cannot give websites access to your entire folder structure. Local Mode only works when you run the app on your own computer.")
        else:
            st.info("💡 **Tip**: Running on your desktop? You can process folders directly.")

        if 'local_path' not in st.session_state: st.session_state.local_path = os.getcwd()
        path_in = st.text_input("Local Folder Path:", st.session_state.local_path)
        
        if os.path.isdir(path_in):
            # Recursive search for .md files in all subfolders
            mds = glob.glob(os.path.join(path_in, "**", "*.md"), recursive=True)
            
            if mds:
                st.success(f"📂 Found **{len(mds)}** Markdown files")
                
                # Build dataframe for selection
                import pandas as pd
                df_data = []
                for f in mds:
                    rel_path = os.path.relpath(f, path_in)
                    df_data.append({
                        "Select": False,  # Default unchecked
                        "File": os.path.basename(f),
                        "Path": rel_path,
                        "Full Path": f
                    })
                
                df = pd.DataFrame(df_data)
                
                # Wrap in expander for collapse/expand
                with st.expander("📋 Select Files to Convert", expanded=True):
                    # Quick select toggle (using checkbox - no reload)
                    select_all = st.checkbox("☑️ Select All / Deselect All", value=False, key="toggle_all")
                    if select_all:
                        df["Select"] = True
                    
                    # Editable table with checkboxes
                    edited_df = st.data_editor(
                        df,
                        column_config={
                            "Select": st.column_config.CheckboxColumn("✓", width="small"),
                            "File": st.column_config.TextColumn("File Name", width="large"),
                            "Path": st.column_config.TextColumn("Path", width="large"),
                            "Full Path": None  # Hidden
                        },
                        disabled=["File", "Path", "Full Path"],
                        hide_index=True,
                        use_container_width=True,
                        height=350,
                        key="file_selector_df"
                    )
                
                # Get selected files
                selected_rows = edited_df[edited_df["Select"] == True]
                sel = selected_rows["Full Path"].tolist()
                
                st.caption(f"**{len(sel)}** / {len(mds)} files selected")
                
                if st.button("🚀 Convert Selected Files", type="primary", disabled=len(sel)==0):
                    with st.status("Converting...", expanded=True) as status:
                        # Progress logic
                        p_bar = st.progress(0, text="Initializing...")
                        def up(p, t): p_bar.progress(p, text=t)

                        s, o, e, new, skip = run_conversion_command(sel, progress_callback=up)
                        p_bar.empty()

                        if s:
                            results = []
                            for f in sel:
                                pdf_p = os.path.splitext(f)[0] + ".pdf"
                                if os.path.exists(pdf_p): results.append((f, pdf_p))
                            
                            st.session_state.processed_files = results 
                            status.update(label="✅ Done!", state="complete")
                            st.session_state.current_view = "viewer"
                            st.rerun()
                        else:
                            st.error(e)
            else:
                st.warning("No .md files found in this folder or subfolders.")

def render_viewer():
    if not st.session_state.processed_files:
        st.info("💡 **Viewer is Empty**")
        st.write("You haven't converted any files yet this session.")
        if st.button("⬅️ Back to Home to Convert"): 
             st.session_state.current_view = "home"
             st.rerun()
        
        # Still show shared sidebar elements even if empty
        with st.sidebar:
            st.markdown("## 📄 PDF Pro")
            st.divider()
            if st.button("🏠 Back to Home", type="secondary", use_container_width=True):
                 st.session_state.current_view = "home"
                 st.rerun()
            render_sidebar_shared(slot="top_no_caption")
        return

    # --- SIDEBAR (CUSTOM ORDER) ---
    with st.sidebar:
        st.markdown("## 📄 PDF Pro")
        
        # 1. FILES (TOP PRIORITY)
        st.subheader("📂 Converted Files")
        file_map = {os.path.basename(p[1]): p[1] for p in st.session_state.processed_files}
        
        # Selection Logic
        if 'viewer_file' not in st.session_state or st.session_state.viewer_file not in file_map.values():
             if file_map: st.session_state.viewer_file = list(file_map.values())[0]

        if file_map:
            current_name = os.path.basename(st.session_state.viewer_file)
            idx = list(file_map.keys()).index(current_name) if current_name in file_map else 0
            selected_name = st.radio("Select Document:", list(file_map.keys()), index=idx, label_visibility="collapsed")
            st.session_state.viewer_file = file_map[selected_name]

            # Zip Download
            st.write("")
            all_pdfs = list(file_map.values())
            if all_pdfs:
                 zip_path = create_zip(all_pdfs)
                 with open(zip_path, "rb") as f:
                     st.download_button("📦 Download All (.zip)", f, "batch_result.zip", "application/zip", use_container_width=True)
        
        st.divider()
        
        # 2. NAVIGATION & STATUS
        if st.button("🏠 Back to Home", type="secondary", use_container_width=True):
             st.session_state.current_view = "home"
             st.rerun()

        if st.button("🗑️ Clear All Results", use_container_width=True, help="Reset workspace"):
            st.session_state.processed_files = []
            st.session_state.viewer_file = None
            st.session_state.current_view = "home"
            st.rerun()
             
        render_sidebar_shared(slot="top_no_caption")
        
        # 3. FOOTER
        st.divider()
        st.caption("v3.3 Optimized | by KhoiBui16")
    
    # --- MAIN VIEWER CONTENT ---
    pdf_path = st.session_state.viewer_file
    
    if pdf_path and os.path.exists(pdf_path):
        # Header Row
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### 📄 {os.path.basename(pdf_path)}")
        with c2:
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF", f, os.path.basename(pdf_path), "application/pdf", type="primary")

        st.divider()
        
        # Full Height Preview
        display_pdf(pdf_path)
    else:
        st.error("File not found or deleted.")
