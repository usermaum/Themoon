
import sys
import os
import glob
from pathlib import Path

# Add backend directory to path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.image_service import ImageService
from app.config import settings

def optimize_bean_images():
    print("🖼️  Optimizing Bean Images...")

    # Define paths
    # Assuming the script is in backend/scripts, we go up two levels to project root
    project_root = Path(__file__).resolve().parent.parent.parent
    source_dir = project_root / "frontend" / "public" / "images" / "raw_material"
    
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return

    print(f"📂 Source Directory: {source_dir}")

    # Initialize ImageService (dummy base dir as we will override it)
    image_service = ImageService(upload_base_dir=str(source_dir))

    # Find all PNG files
    png_files = list(source_dir.glob("*.png"))
    print(f"found {len(png_files)} PNG files to process.")

    results = []

    for png_path in png_files:
        print(f"Processing: {png_path.name}...")
        try:
            with open(png_path, "rb") as f:
                content = f.read()
            
            # Use stem (filename without extension) as custom filename base
            # e.g. "01_yirgacheffe_raw.png" -> "01_yirgacheffe_raw"
            # This will generate:
            # 01_yirgacheffe_raw.jpg (Original profile)
            # 01_yirgacheffe_raw_web.webp (Webview profile)
            # 01_yirgacheffe_raw_thumb.webp (Thumbnail profile)
            
            res = image_service.process_and_save(
                file_content=content,
                original_filename=png_path.name,
                output_dir=source_dir,
                custom_filename=png_path.stem
            )
            results.append((png_path.name, "Success"))
        except Exception as e:
            print(f"❌ Failed to process {png_path.name}: {e}")
            results.append((png_path.name, f"Failed: {e}"))

    print("\n✅ Optimization Complete.")
    print(f"Processed {len(results)} images.")

if __name__ == "__main__":
    optimize_bean_images()
