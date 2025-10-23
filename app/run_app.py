"""
Streamlit 애플리케이션 런처
Streamlit Application Launcher
"""

import streamlit as st
import subprocess
import sys
import os

if __name__ == '__main__':
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, 'app.py')

    # Run streamlit
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run',
        app_path,
        '--server.port', '8501',
        '--server.headless', 'true'
    ])
