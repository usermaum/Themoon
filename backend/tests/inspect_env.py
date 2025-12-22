
import os
from pathlib import Path

def inspect_env():
    # Assume script is in backend/tests/
    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    env_path = root_dir / ".env"
    
    print(f"Inspecting: {env_path}")
    
    if not env_path.exists():
        print("❌ .env file NOT found at root.")
        return

    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        found = False
        for i, line in enumerate(lines):
            if "ANTHROPIC" in line:
                print(f"Line {i+1}: {repr(line)}")
                found = True
                
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    print(f"  Key: '{key}'")
                    print(f"  Value Length: {len(value)}")
                    print(f"  Value Starts With: {value[:10]}...")
                else:
                    print("  ⚠️ Line does not contain '='")

        if not found:
            print("❌ 'ANTHROPIC' string not found in .env")
            
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    inspect_env()
