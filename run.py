#!/usr/bin/env python3
"""
더문 드립바 로스팅 원가 계산기 - 메인 런처
The Moon Drip BAR - Roasting Cost Calculator - Main Launcher
"""

import sys
import subprocess
import os

def main():
    """Run the Streamlit application"""
    app_path = os.path.join(os.path.dirname(__file__), 'app', 'app.py')

    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        app_path,
        '--server.port', '8501',
        '--server.headless', 'true'
    ]

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n애플리케이션이 종료되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
