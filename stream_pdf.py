import streamlit as st
import tempfile
import sys
import os

# Ensure we can import from modules
sys.path.append(os.getcwd())

from modules.styles import PREMIUM_STYLE
from modules.ui import render_home, render_viewer

# --- APP CONFIG ---
st.set_page_config(
    page_title="Markdown to PDF Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Styles
st.markdown(PREMIUM_STYLE, unsafe_allow_html=True)

from modules.utils import get_fixed_temp_dir
import glob

# --- SESSION STATE & PERSISTENCE ---
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = get_fixed_temp_dir()

# Auto-load existing PDFs from temp dir to survive reloads
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = []
    # Scan for md and pdf pairs
    md_files = glob.glob(os.path.join(st.session_state.temp_dir, "*.md"))
    results = []
    for md_p in md_files:
        pdf_p = os.path.splitext(md_p)[0] + ".pdf"
        if os.path.exists(pdf_p):
            results.append((md_p, pdf_p))
    st.session_state.processed_files = results

if 'current_view' not in st.session_state:
    st.session_state.current_view = "home"

# --- ROUTER ---
# Sidebar is always rendered first to handle navigation
# Sidebar (Handled inside views for custom order)

if st.session_state.current_view == "home":
    render_home()
else:
    render_viewer() # Viewer adds EXTRA elements to sidebar
