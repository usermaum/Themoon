import asyncio
import os
import sys

# Backend root directory setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ocr_service import OCRService

async def main():
    print("running ocr verification for supplier name...")
    
    image_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "frontend", "public", "images", "IMG_1660.JPG"
    )
    
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    print(f"Reading image from: {image_path}")
    
    with open(image_path, "rb") as f:
        image_bytes = f.read()
        
    service = OCRService()
    
    try:
        # Use stream for better feedback or just analyze_image for simplicity
        # Using analyze_image_stream to see progress
        print("Starting OCR stream...")
        final_result = None
        async for update in service.analyze_image_stream(image_bytes, mime_type="image/jpeg"):
            status = update.get("status")
            if status == "progress":
                print(f"[Progress] {update.get('message')}")
            elif status == "complete":
                final_result = update.get("data")
                print("\n[Complete] OCR Result received.")
            elif status == "error":
                print(f"[Error] {update.get('message')}")
                
        if final_result:
            supplier = final_result.get("supplier_name")
            raw_text = final_result.get("debug_raw_text", "")
            print(f"KEYS: {list(final_result.keys())}")
            print(f"SUPPLIER DICT: {final_result.get('supplier')}")
            print(f"RAW TEXT HEAD (100 chars): {raw_text[:100]}")
            
            print("\n" + "="*50)
            print(f"EXTRACTED SUPPLIER NAME: {supplier}")
            print("="*50)
            
            # Additional validation
            if supplier and "LACIELO" in supplier.upper():
                 print("✅ VERIFICATION SUCCESS: 'LACIELO' found in supplier name.")
            else:
                 print(f"⚠️ VERIFICATION WARNING: Expected 'LACIELO' but got '{supplier}'")
                 
            # Print items for sanity check
            items = final_result.get("items", [])
            print(f"\nExtracted {len(items)} items:")
            for item in items[:3]: # print first 3
                print(f"- {item.get('bean_name')} ({item.get('total_weight', 0)}kg)")
                
    except Exception as e:
        print(f"Fatal Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
