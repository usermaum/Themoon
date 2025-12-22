# 이미지 최적화 서비스 개선 플랜 (Phase 1 완료 후 개선)

## 📋 현재 상태 요약

### ✅ 구현 완료된 기능
- ImageService 클래스 구현 (`backend/app/services/image_service.py`, 121줄)
- 4단계 보안 검증 (파일 크기, 확장자, MIME 타입, 무결성)
- 3종 이미지 생성 (original/webview/thumbnail)
- 연/월별 폴더 자동 생성
- inbound.py 라우터 통합
- DB 스키마 컬럼 추가 완료
- requirements.txt에 Pillow, python-magic 추가

### ❌ 발견된 문제점

**Critical**
1. 타입 힌팅 오류 (Line 56: `Dict[str, any]` → `Dict[str, Any]`)

**High Priority (보안)**
2. EXIF 민감 데이터 미제거 (GPS, 카메라 정보 유출 가능)
3. 경로 검증 미흡 (심볼릭 링크 공격, 경로 순회 취약점)
4. 에러 처리 과도하게 광범위 (`except Exception`)

**High Priority (안정성)**
5. 원자적 저장 미구현 (부분 파일 남을 수 있음)
6. 디스크 용량 체크 없음
7. 부분 실패 시 정리 로직 없음

**Medium Priority**
8. 전역 싱글톤 구조 (테스트 어려움)
9. config.py에 이미지 설정 없음 (하드코딩)
10. 로깅 부족 (성능 메트릭, 구조화 로깅)

---

## 🎯 개선 목표

- **보안**: EXIF 유출 방지, 경로 공격 차단
- **안정성**: 원자적 저장으로 부분 실패 방지
- **테스트 가능성**: 의존성 주입 패턴 적용
- **운영 가시성**: 구조화된 로깅 및 메트릭

---

## 📝 개선 작업 목록 (우선순위별)

### Priority 1: Critical (5분) ⚠️ 즉시 수정

#### Task 1.1: 타입 힌팅 오류 수정
**파일**: `backend/app/services/image_service.py`

**수정 내용**:
```python
# Line 9: Any 임포트 추가
from typing import Tuple, Dict, Optional, Any  # Any 추가

# Line 56: 타입 힌팅 수정
def process_and_save(self, file_content: bytes, original_filename: str) -> Dict[str, Any]:  # any → Any
```

**검증**: `mypy backend/app/services/image_service.py`

---

### Priority 2: High - 보안 강화 (30분)

#### Task 2.1: EXIF 민감 데이터 제거
**파일**: `backend/app/services/image_service.py`

**추가 메서드**:
```python
def _strip_sensitive_exif(self, img: Image) -> Image:
    """EXIF 민감 데이터 제거 (GPS, 카메라 정보 등)"""
    from PIL import ImageOps

    # 1. 방향 정보 적용 (회전)
    img = ImageOps.exif_transpose(img)

    # 2. 모든 EXIF 데이터 제거
    data = list(img.getdata())
    img_without_exif = Image.new(img.mode, img.size)
    img_without_exif.putdata(data)

    return img_without_exif
```

**적용 위치**: Line 86-90을 위 메서드 호출로 대체

---

#### Task 2.2: 경로 검증 강화
**파일**: `backend/app/services/image_service.py`

**추가 메서드**:
```python
def _validate_path_security(self, path: Path) -> bool:
    """경로 보안 검증 (심볼릭 링크, 경로 순회 방어)"""
    try:
        # 1. 절대 경로로 해석
        resolved_path = path.resolve()

        # 2. 기준 경로 확인
        base_path = self.base_dir.resolve()

        # 3. 기준 경로 내부에 있는지 확인
        try:
            resolved_path.relative_to(base_path)
        except ValueError:
            logger.error(f"Path traversal attempt: {path}")
            return False

        # 4. 심볼릭 링크 확인
        if path.is_symlink():
            logger.warning(f"Symlink detected: {path}")
            return False

        return True
    except Exception as e:
        logger.error(f"Path validation error: {e}")
        return False
```

**적용 위치**: `process_and_save()` Line 68 이후 (저장 전)

---

#### Task 2.3: 구체적 에러 타입 처리
**파일**: `backend/app/services/image_service.py`

**수정 위치**: Line 47-52, 87-90, 114-116

**변경 내용**:
```python
# Before (Line 114-116)
except Exception as e:
    logger.error(f"Failed to process and save image: {str(e)}")
    raise e

# After
except (IOError, OSError) as e:
    logger.error(f"Image I/O error: {e}", exc_info=True)
    raise
except PIL.UnidentifiedImageError as e:
    logger.error(f"Invalid image format: {e}")
    raise
except Exception as e:
    logger.exception(f"Unexpected error during image processing: {e}")
    raise
```

---

### Priority 3: High - 안정성 강화 (1시간)

#### Task 3.1: 원자적 저장 구현
**파일**: `backend/app/services/image_service.py`

**추가 메서드**:
```python
def _save_atomic(self, img: Image, target_path: Path, **save_kwargs) -> None:
    """원자적 이미지 저장 (임시 파일 + rename)"""
    import tempfile

    # 1. 임시 파일 생성 (같은 디렉토리)
    temp_fd, temp_path = tempfile.mkstemp(
        suffix=target_path.suffix,
        dir=target_path.parent,
        prefix=".tmp_"
    )

    try:
        # 2. 임시 파일에 저장
        with os.fdopen(temp_fd, 'wb') as f:
            img.save(f, **save_kwargs)

        # 3. 원자적 rename
        os.replace(temp_path, target_path)

        logger.debug(f"Atomically saved: {target_path}")
    except Exception as e:
        # 4. 실패 시 임시 파일 정리
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise
```

**적용 위치**: Line 104-109의 `tier_img.save()` 호출을 `self._save_atomic()` 호출로 대체

---

#### Task 3.2: 디스크 용량 체크
**파일**: `backend/app/services/image_service.py`

**추가 메서드**:
```python
def _check_disk_space(self, min_free_gb: int = 5) -> None:
    """디스크 여유 공간 확인"""
    import shutil

    stat = shutil.disk_usage(self.base_dir)
    free_gb = stat.free / (1024 ** 3)

    if free_gb < min_free_gb:
        logger.error(f"Low disk space: {free_gb:.2f}GB < {min_free_gb}GB")
        raise IOError(
            f"Insufficient disk space: {free_gb:.2f}GB available, "
            f"{min_free_gb}GB required"
        )

    logger.debug(f"Disk space OK: {free_gb:.2f}GB free")
```

**적용 위치**: `process_and_save()` 초반부 (Line 61 이후)

---

#### Task 3.3: 부분 실패 정리 로직
**파일**: `backend/app/services/image_service.py`

**추가 메서드**:
```python
def _cleanup_partial(self, paths: list[Path]) -> None:
    """부분 실패 시 생성된 파일 정리"""
    for path in paths:
        if path and path.exists():
            try:
                path.unlink()
                logger.info(f"Cleaned up partial file: {path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {path}: {e}")
```

**process_and_save() 수정**:
```python
saved_paths = []  # 성공한 경로 추적

try:
    with Image.open(io.BytesIO(file_content)) as img:
        # ... 기존 로직 ...

        for tier, config in self.profiles.items():
            # ... 이미지 처리 ...

            # 저장
            self._save_atomic(tier_img, abs_path, ...)
            saved_paths.append(abs_path)

            results["paths"][tier] = str(rel_path).replace("\\", "/")

except Exception as e:
    # 롤백
    self._cleanup_partial(saved_paths)
    logger.error(f"Image processing failed, cleaned up {len(saved_paths)} files")
    raise
```

---

### Priority 4: Medium - 테스트 인프라 (1시간)

#### Task 4.1: 의존성 주입 패턴 적용
**파일**:
- `backend/app/services/image_service.py`
- `backend/app/api/v1/endpoints/inbound.py`

**image_service.py 수정**:
```python
# 팩토리 함수 추가 (Line 120 대체)
def get_image_service(upload_dir: str = "static/uploads/inbound") -> ImageService:
    """의존성 주입용 팩토리 함수"""
    return ImageService(upload_dir)

# 전역 싱글톤은 하위 호환성을 위해 유지
image_service = ImageService()
```

**inbound.py 수정**:
```python
# Line 8: 임포트 수정
from app.services.image_service import get_image_service, ImageService

# 엔드포인트에 의존성 주입 적용 (선택적)
@router.post("/analyze")
async def analyze_inbound_document(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    img_service: ImageService = Depends(get_image_service)  # 주입
):
    # 사용: img_service.validate_image(...) 대신 기존처럼 사용 가능
```

---

#### Task 4.2: 단위 테스트 파일 생성
**파일**: `backend/tests/test_image_service.py` (신규 생성)

**내용**:
```python
import pytest
from pathlib import Path
from PIL import Image
import io
from app.services.image_service import ImageService

@pytest.fixture
def test_image_bytes():
    """테스트용 이미지 생성"""
    img = Image.new('RGB', (800, 1200), color='red')
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()

@pytest.fixture
def image_service(tmp_path):
    """테스트용 ImageService"""
    return ImageService(upload_base_dir=str(tmp_path))

def test_validate_image_success(image_service, test_image_bytes):
    is_valid, error = image_service.validate_image(test_image_bytes, "test.jpg")
    assert is_valid
    assert error == ""

def test_validate_image_too_large(image_service):
    large_bytes = b"x" * (21 * 1024 * 1024)  # 21MB
    is_valid, error = image_service.validate_image(large_bytes, "test.jpg")
    assert not is_valid
    assert "exceeds limit" in error

def test_validate_image_wrong_extension(image_service, test_image_bytes):
    is_valid, error = image_service.validate_image(test_image_bytes, "test.exe")
    assert not is_valid
    assert "extension" in error.lower()

def test_process_and_save(image_service, test_image_bytes):
    result = image_service.process_and_save(test_image_bytes, "test.jpg")

    assert 'paths' in result
    assert 'original' in result['paths']
    assert 'webview' in result['paths']
    assert 'thumbnail' in result['paths']
    assert result['width'] == 800
    assert result['height'] == 1200

def test_atomic_save_rollback(image_service, test_image_bytes, monkeypatch):
    """원자적 저장 실패 시 롤백 테스트"""
    # TODO: 2번째 이미지 저장 시 실패하도록 모킹
    pass
```

**테스트 실행**:
```bash
pytest backend/tests/test_image_service.py -v
pytest backend/tests/test_image_service.py --cov=app.services.image_service
```

---

### Priority 5: Medium - 운영 개선 (30분)

#### Task 5.1: config.py에 이미지 설정 추가
**파일**: `backend/app/config.py`

**추가 내용** (Line 45 이후):
```python
    # Image Processing Settings
    IMAGE_UPLOAD_BASE_DIR: str = "static/uploads/inbound"
    IMAGE_MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 20MB
    IMAGE_MIN_FREE_DISK_SPACE_GB: int = 5  # 최소 여유 공간

    # Image Quality Profiles
    IMAGE_ORIGINAL_MAX_SIZE: tuple[int, int] = (1600, 2400)
    IMAGE_ORIGINAL_QUALITY: int = 95
    IMAGE_WEBVIEW_MAX_SIZE: tuple[int, int] = (1200, 1800)
    IMAGE_WEBVIEW_QUALITY: int = 85
    IMAGE_THUMBNAIL_MAX_SIZE: tuple[int, int] = (400, 400)
    IMAGE_THUMBNAIL_QUALITY: int = 75
```

**image_service.py 수정**:
```python
from app.config import settings

class ImageService:
    def __init__(self, upload_base_dir: str = None):
        self.base_dir = Path(upload_base_dir or settings.IMAGE_UPLOAD_BASE_DIR)
        # ...
        self.max_file_size = settings.IMAGE_MAX_FILE_SIZE

        self.profiles = {
            'original': {
                'max_size': settings.IMAGE_ORIGINAL_MAX_SIZE,
                'quality': settings.IMAGE_ORIGINAL_QUALITY,
                # ...
            },
            # ...
        }
```

---

#### Task 5.2: 구조화된 로깅 추가
**파일**: `backend/app/services/image_service.py`

**수정 내용**:
```python
import time

def process_and_save(self, file_content: bytes, original_filename: str) -> Dict[str, Any]:
    start_time = time.time()

    try:
        # ... 기존 로직 ...

        elapsed_ms = (time.time() - start_time) * 1000
        logger.info(
            "Image processing completed",
            extra={
                "event": "image_processed",
                "original_filename": original_filename,
                "file_size_bytes": len(file_content),
                "compressed_size": results['file_size_bytes'],
                "compression_ratio": round((1 - results['file_size_bytes'] / len(file_content)) * 100, 2),
                "processing_time_ms": round(elapsed_ms, 2),
                "paths": results['paths']
            }
        )

        return results

    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        logger.error(
            "Image processing failed",
            extra={
                "event": "image_processing_failed",
                "processing_time_ms": round(elapsed_ms, 2),
                "error": str(e),
                "error_type": type(e).__name__
            },
            exc_info=True
        )
        raise
```

---

## 🗂️ 수정 대상 파일 요약

| 파일 | 우선순위 | 작업 내용 |
|------|---------|----------|
| `backend/app/services/image_service.py` | Critical, High | 타입 힌팅, 보안, 안정성 개선 |
| `backend/app/config.py` | Medium | 이미지 설정 추가 |
| `backend/tests/test_image_service.py` | Medium | 신규 테스트 파일 생성 |
| `backend/app/api/v1/endpoints/inbound.py` | Medium | 의존성 주입 (선택적) |

---

## ⏱️ 예상 소요 시간

| 우선순위 | 총 소요 시간 |
|---------|-------------|
| **Priority 1 (Critical)** | 5분 |
| **Priority 2 (보안)** | 30분 |
| **Priority 3 (안정성)** | 1시간 |
| **Priority 4 (테스트)** | 1시간 |
| **Priority 5 (운영)** | 30분 |
| **통합 테스트 & 검증** | 1시간 |
| **총계** | **약 4시간** |

---

## ✅ 검증 체크리스트

### 기능 검증
- [ ] 타입 힌팅 오류 해결 (`mypy` 통과)
- [ ] EXIF GPS 데이터 제거 확인 (`exiftool`로 검증)
- [ ] 경로 순회 공격 차단 (테스트 케이스)
- [ ] 원자적 저장 검증 (중간 실패 시나리오)
- [ ] 디스크 용량 부족 시 에러 발생
- [ ] 부분 실패 시 롤백 확인

### 보안 검증
- [ ] 악성 파일 업로드 차단 (`.exe`, `.sh` 등)
- [ ] 심볼릭 링크 공격 방어
- [ ] 20MB 초과 파일 거부
- [ ] 손상된 이미지 탐지

### 성능 검증
- [ ] 평균 처리 시간 < 2초 (500KB 이미지 기준)
- [ ] 메모리 누수 없음 (100회 연속 처리)
- [ ] 압축률 60-80% 달성

### 테스트 커버리지
- [ ] 단위 테스트 커버리지 > 80%
- [ ] 통합 테스트: inbound.py 엔드포인트
- [ ] 엣지 케이스 테스트

---

## 📚 후속 작업 (Phase 2 이후)

### Phase 2: OCR 전처리 최적화
- 그레이스케일 변환
- 대비 향상 (CLAHE)
- 품질 검증 (해상도, 명도 체크)

### Phase 3: 백업 및 모니터링
- rsync 백업 스크립트 작성
- 디스크 사용량 대시보드
- 성능 메트릭 시각화

### Phase 4: 고급 기능
- 이미지 워터마크 추가
- 중복 이미지 탐지
- CDN 통합

---

## 🚀 구현 시작 명령

```bash
# 1. 타입 체크 (현재 상태)
mypy backend/app/services/image_service.py

# 2. 개선 후 테스트
pytest backend/tests/test_image_service.py -v

# 3. 커버리지 측정
pytest backend/tests/test_image_service.py --cov=app.services.image_service --cov-report=html
```

---

**작성일**: 2025-12-22
**버전**: 1.0
**다음 리뷰**: Priority 1-2 완료 후
