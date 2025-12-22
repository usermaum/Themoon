import pytest
import os
import io
import shutil
from pathlib import Path
from PIL import Image
from app.services.image_service import ImageService

@pytest.fixture
def test_image_bytes():
    """Create a dummy test image in memory."""
    img = Image.new('RGB', (800, 1200), color='red')
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()

@pytest.fixture
def image_service(tmp_path):
    """Create an ImageService instance with a temporary directory."""
    return ImageService(upload_base_dir=str(tmp_path))

def test_validate_image_success(image_service, test_image_bytes):
    is_valid, error = image_service.validate_image(test_image_bytes, "test.jpg")
    assert is_valid
    assert error == ""

def test_validate_image_too_large(image_service):
    # Mocking a large file by creating a byte string larger than 20MB
    large_bytes = b"x" * (20 * 1024 * 1024 + 1)
    is_valid, error = image_service.validate_image(large_bytes, "test.jpg")
    assert not is_valid
    assert "exceeds limit" in error

def test_validate_image_wrong_extension(image_service, test_image_bytes):
    is_valid, error = image_service.validate_image(test_image_bytes, "test.exe")
    assert not is_valid
    assert "Unsupported file extension" in error

def test_process_and_save_success(image_service, test_image_bytes):
    result = image_service.process_and_save(test_image_bytes, "test.jpg")

    assert 'paths' in result
    assert 'original' in result['paths']
    assert 'webview' in result['paths']
    assert 'thumbnail' in result['paths']
    
    assert result['width'] == 800
    assert result['height'] == 1200
    
    # Verify files exist
    base = Path(image_service.base_dir)
    assert (base / result['paths']['original']).exists()
    assert (base / result['paths']['webview']).exists()
    assert (base / result['paths']['thumbnail']).exists()

def test_atomic_save_fail_cleanup(image_service, test_image_bytes, monkeypatch):
    """Test that partial files are cleaned up if a later step fails."""
    
    # We will simulate a failure during the saving of the 2nd tier
    original_save = image_service._save_atomic
    call_count = 0
    
    def mock_save_atomic(img, target_path, **kwargs):
        nonlocal call_count
        call_count += 1
        # Fail on the 2nd call (webview or thumbnail depending on dict order, usually webview)
        if call_count == 2:
            raise RuntimeError("Simulated Save Failure")
        return original_save(img, target_path, **kwargs)
        
    monkeypatch.setattr(image_service, '_save_atomic', mock_save_atomic)
    
    try:
        image_service.process_and_save(test_image_bytes, "test.jpg")
        pytest.fail("Should have raised RuntimeError")
    except RuntimeError:
        pass
    
    # Verify cleanup: The directory should be effectively empty of files 
    # (directories might remain, but no image files)
    # We recursively search for files
    files = list(Path(image_service.base_dir).rglob("*"))
    files = [f for f in files if f.is_file()]
    
    assert len(files) == 0, f"Found remaining files after cleanup: {files}"

def test_path_traversal_protection(image_service):
    """Test that path traversal attempts are blocked."""
    # This is an internal method test
    assert not image_service._validate_path_security(Path("/etc/passwd"))
    assert not image_service._validate_path_security(Path("../../../etc/passwd"))
    
    # Valid path
    assert image_service._validate_path_security(Path(image_service.base_dir) / "2024/01/test.jpg")
