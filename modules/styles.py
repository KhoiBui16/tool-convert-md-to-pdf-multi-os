# CSS Styles
PREMIUM_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Main Content Card */
    .block-container {
        background-color: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 1rem !important; /* Minimal padding */
        margin-top: 2rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        max-width: 98%; /* True Zen width */
    }

    /* Viewer Specific - Maximize Iframe */
    .pdf-viewer-frame {
        width: 100%;
        height: 90vh; /* Taller */
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }

    /* Header tweaks */
    header {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    h1, h2, h3, h5, p, li, span { color: #1f2937 !important; }
    h1 {
        font-weight: 900 !important;
        background: -webkit-linear-gradient(45deg, #1f2937, #4b5563);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-right: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Buttons */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        transition: all 0.2s;
        width: auto !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 12px -3px rgba(37, 99, 235, 0.3);
    }
    
    /* Secondary/Download Buttons */
    div.stDownloadButton > button {
        width: 100% !important;
        background-color: #f1f5f9;
        color: #334155;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1rem;
    }
    div.stDownloadButton > button:hover {
        border-color: #3b82f6;
        color: #3b82f6;
        background-color: white;
    }

    /* Inputs */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 30px;
        background: #f8fafc;
        text-align: center;
    }
</style>
"""
