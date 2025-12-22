import os
import io
import uuid
import logging
import magic
from datetime import datetime
from PIL import Image
from pathlib import Path
from typing import Tuple, Dict, Optional

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self, upload_base_dir: str = "static/uploads/inbound"):
        self.base_dir = Path(upload_base_dir)
        self.allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.tiff'}
        self.allowed_mime_types = {'image/jpeg', 'image/png', 'image/webp', 'image/tiff'}
        self.max_file_size = 20 * 1024 * 1024  # 20MB

        # Multi-tier configurations
        self.profiles = {
            'original': {'max_size': (1600, 2400), 'quality': 95, 'format': 'JPEG', 'suffix': ''},
            'webview': {'max_size': (1200, 1800), 'quality': 85, 'format': 'WEBP', 'suffix': '_web'},
            'thumbnail': {'max_size': (400, 400), 'quality': 75, 'format': 'WEBP', 'suffix': '_thumb'}
        }

    def validate_image(self, file_content: bytes, filename: str) -> Tuple[bool, str]:
        """
        Validates the image for security and integrity.
        Returns (success, error_message)
        """
        # 1. Size check
        if len(file_content) > self.max_file_size:
            return False, f"File size exceeds limit ({self.max_file_size // (1024*1024)}MB)"

        # 2. Extension check
        ext = os.path.splitext(filename)[1].lower()
        if ext not in self.allowed_extensions:
            return False, f"Unsupported file extension: {ext}"

        # 3. Magic bytes / MIME type check
        mime = magic.from_buffer(file_content, mime=True)
        if mime not in self.allowed_mime_types:
            return False, f"Invalid file content type: {mime}"

        # 4. Image integrity check using Pillow
        try:
            with Image.open(io.BytesIO(file_content)) as img:
                img.verify()
        except Exception as e:
            logger.error(f"Image integrity check failed: {str(e)}")
            return False, "Corrupted or invalid image file"

        return True, ""

    def process_and_save(self, file_content: bytes, original_filename: str) -> Dict[str, any]:
        """
        Main entry point to process an image and save it in 3 tiers.
        Returns a dictionary with paths and metadata.
        """
        # Create base filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        safe_base_name = f"invoice_{timestamp}_{unique_id}"

        # Get relative directory based on year/month
        rel_dir = Path(datetime.now().strftime("%Y/%m"))
        abs_base_dir = self.base_dir / rel_dir
        
        # Ensure directories exist
        for tier in self.profiles.keys():
            (abs_base_dir / tier).mkdir(parents=True, exist_ok=True)

        results = {
            "file_size_bytes": len(file_content),
            "original_filename": original_filename,
            "paths": {}
        }

        try:
            with Image.open(io.BytesIO(file_content)) as img:
                # Store original dimensions
                results["width"], results["height"] = img.size
                
                # Handle orientation if EXIF present
                try:
                    from PIL import ImageOps
                    img = ImageOps.exif_transpose(img)
                except Exception as e:
                    logger.warning(f"Failed to handle EXIF transpose: {e}")

                for tier, config in self.profiles.items():
                    tier_img = img.copy()
                    tier_img.thumbnail(config['max_size'], Image.Resampling.LANCZOS)
                    
                    file_ext = config['format'].lower()
                    if file_ext == 'jpeg': file_ext = 'jpg'
                    
                    tier_filename = f"{safe_base_name}{config['suffix']}.{file_ext}"
                    rel_path = rel_dir / tier / tier_filename
                    abs_path = self.base_dir / rel_path
                    
                    # Save image
                    tier_img.save(
                        abs_path, 
                        format=config['format'], 
                        quality=config['quality'], 
                        optimize=True
                    )
                    
                    # Store results (using forward slashes for URL compatibility)
                    results["paths"][tier] = str(rel_path).replace("\\", "/")

        except Exception as e:
            logger.error(f"Failed to process and save image: {str(e)}")
            raise e

        return results

image_service = ImageService()
