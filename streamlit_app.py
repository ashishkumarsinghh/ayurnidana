"""Streamlit Cloud Production Entrypoint for AyurNidana.
Automatically discovered and launched by Streamlit Community Cloud and Docker deployments.
"""
import sys
import os
import runpy
import traceback
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(ROOT_DIR, ".env")
if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    load_dotenv()
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Execute the core UI application
app_path = os.path.join(ROOT_DIR, "ayurnidana", "ui", "app.py")
try:
    runpy.run_path(app_path, run_name="__main__")
except Exception:
    import streamlit as st
    st.error("🌿 AyurNidana encountered a startup error. Please refresh the page.")
    with st.expander("🔧 Technical Details"):
        st.code(traceback.format_exc())
