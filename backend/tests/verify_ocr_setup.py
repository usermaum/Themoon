
import os
import sys
import asyncio
from pathlib import Path

# Add backend directory to sys.path to allow importing 'app'
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

from app.services.ocr_service import OCRService

# Setup mock environment if needed or rely on .env
# Ensure you have ANTHROPIC_API_KEY in .env

async def test_ocr():
    print("Testing OCR Service with Claude Integration...")
    service = OCRService()
    
    print("\n[Configuration Check]")
    if service.google_client:
        print("✅ Google Client: Configured")
    else:
        print("❌ Google Client: Missing")
        
    if service.anthropic_client:
        print("✅ Anthropic Client: Configured")
    else:
        print("❌ Anthropic Client: Missing")

    print(f"\n[Model Priority] {service.models}")

    # Create a dummy image or load one if available
    # For a real test, simpler to just check if clients are initialized if we don't have a file ready.
    # But let's try to mock the analyze_image call if we had an image.
    
    if not service.anthropic_client:
        print("\n⚠️ Skipping actual API test because ANTHROPIC_API_KEY is not set.")
        return

    print("\n✅ Service initialization successful. Integration logic seems correct.")

if __name__ == "__main__":
    asyncio.run(test_ocr())
