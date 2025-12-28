import sys
import os
import asyncio
from dotenv import load_dotenv

# Setup path
current_dir = os.path.dirname(os.path.abspath(__file__))
# backend root is current_dir since this file is in backend/
sys.path.append(current_dir)

# Load env from .env file in backend/
load_dotenv(os.path.join(current_dir, ".env"))

from app.services.ocr_service import OCRService

async def verify_ocr():
    print("🚀 Initializing OCR Service...")
    service = OCRService()
    
    # Image path from user metadata
    image_path = "C:/Users/HomePC/.gemini/antigravity/brain/fae9dfdf-c0f3-4a8e-a6bd-45638e2f8fd7/uploaded_image_1766861664145.png"
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found at {image_path}")
        return

    print(f"📸 Loading image: {image_path}")
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    print("🤖 Running Analysis (may take a few seconds)...")
    try:
        # Use simple sync wrapper or just await the async generator? 
        # The service has analyze_image (sync-ish wrapper) and analyze_image_stream
        # analyze_image calls sync versions. Let's use analyze_image for simplicity if it exists and works.
        # Wait, analyze_image in ocr_service.py is synchronous.
        
        result = service.analyze_image(image_bytes)
        
        print("\n✅ Analysis Complete!")
        print("-" * 50)
        
        items = result.get("items", [])
        print(f"📦 Found {len(items)} items:")
        
        for i, item in enumerate(items):
            print(f"\n[Item {i+1}]")
            print(f"  - Bean Name: {item.get('bean_name')}")
            print(f"  - Total Weight (raw): {item.get('total_weight')}  <-- CHECK THIS")
            print(f"  - Quantity: {item.get('quantity')}")
            print(f"  - Unit: {item.get('unit')}")
            
            # Simple Validation Rule
            weight = item.get('total_weight')
            qty = item.get('quantity')
            
            if weight and "40" in str(weight):
                print("  ✨ SUCCESS: '40' found in total_weight!")
            elif qty == 2 or str(qty) == "2":
                 if not weight:
                     print("  ⚠️ WARNING: Quantity is 2, but Total Weight is MISSING!")
                 else:
                     print("  ℹ️ Quantity is 2. Weight is present.")
            else:
                 print("  ❓ Output needs manual check.")

        print("-" * 50)
        print("Raw Result (Partial):")
        print(str(result)[:500])

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # service.analyze_image is sync, so we don't strictly need asyncio unless we use the stream method.
    # But let's check the code: analyze_image is defined as `def analyze_image(...)`.
    # It calls `_call_gemini_sync` etc. So it is synchronous blocking.
    import time
    start = time.time()
    
    # Wrap in try/except block just in case
    try:
        # Re-import to avoid async def issue if I change my mind, but let's just stick to sync execution for analyze_image
        print("🚀 Initializing OCR Service (Sync)...")
        service = OCRService()
        
        image_path = "C:/Users/HomePC/.gemini/antigravity/brain/fae9dfdf-c0f3-4a8e-a6bd-45638e2f8fd7/uploaded_image_1766861664145.png"
        
        if not os.path.exists(image_path):
             # Fallback to local test image if absolute path fails (unlikely in this env but good practice)
             print(f"❌ Image not found: {image_path}")
             sys.exit(1)
             
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            
        print("🤖 Analyzing...")
        result = service.analyze_image(image_bytes, mime_type="image/png")
        
        print("\n✅ Result:")
        items = result.get("items", [])
    except Exception as e:
        print(f"❌ Failed: {e}")
        with open("backend/verify_result.txt", "w", encoding="utf-8") as f:
            f.write(f"FAILED: {e}")

    else:
        with open("backend/verify_result.txt", "w", encoding="utf-8") as f:
            f.write("OCR RESULT:\n")
            items = result.get("items", [])
            for i, item in enumerate(items):
                line = f"Item {i+1}: Weight='{item.get('total_weight')}', Qty='{item.get('quantity')}'"
                print(line)
                f.write(line + "\n")
            f.write("\nFULL_JSON:\n" + str(result))
