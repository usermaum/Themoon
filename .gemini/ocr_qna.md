현재 작성하신 코드는 **Pillow(PIL)**를 활용한 기본적인 전처리 로직과 **Gemini/Claude** 같은 최신 멀티모달 LLM을 이용한 OCR 파이프라인으로 구성되어 있습니다.

이미지 처리 코드(`ImageService`)에 **인식률을 실질적으로 높일 수 있는 3가지 핵심 기능**을 추가하고, 이를 JSON 설정과 연동하는 방법을 정리해 드립니다.

---

### 1. `ImageService`에 추가해야 할 핵심 기능

LLM 기반 OCR은 인간의 눈과 비슷합니다. 따라서 **'기울기 보정'**과 **'선명도(Sharpness)'**가 인식률에 가장 큰 영향을 미칩니다.

#### 수정 제안: `preprocess_for_ocr` 메소드 확장

**Python**

```
# ImageService 클래스 내부의 preprocess_for_ocr 메소드에 아래 로직 추가 제안

def preprocess_for_ocr(self, img: PILImage, ...) -> PILImage:
    # ... (기존 설정 로드 로직) ...

    # 1. 자동 회전 및 수평 보정 (Auto-Deskew)
    # LLM은 돌아간 글자도 읽지만, 수평이 맞을 때 표(Table) 구조 파악 능력이 극대화됩니다.
    img = ImageOps.exif_transpose(img) 

    # 2. 선명도 향상 (Sharpening) - 신규 추가 추천
    # 대비(Contrast)만 높이면 글자가 뭉칠 수 있지만, 선명도를 높이면 경계선이 뚜렷해집니다.
    if getattr(config, "enhance_sharpness", True):
        sharpness_factor = getattr(config, "sharpness_factor", 2.0)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness_factor)

    # 3. 리사이징 (Upscaling) - 신규 추가 추천
    # 텍스트가 너무 작은 경우 AI가 획을 오인할 수 있습니다.
    width, height = img.size
    if width < 1500 or height < 1500: # 최소 권장 해상도
        img = img.resize((width * 2, height * 2), Image.Resampling.LANCZOS)

    # ... (기존 그레이스케일, 대비, 노이즈 로직) ...
    return img
```

---

### 2. 최적의 `image_processing_config.json` 설정값

Gemini 1.5/2.0 Flash와 Claude 3.5 Sonnet은 성능이 매우 뛰어나므로, 너무 과한 필터보다는 **"텍스트의 특징을 부각"**하는 설정이 유리합니다.

**JSON**

```
{
  "to_grayscale": true,
  "enhance_contrast": true,
  "contrast_factor": 1.5,
  "enhance_sharpness": true,   // 추가 추천
  "sharpness_factor": 2.0,      // 추가 추천
  "remove_noise": true,
  "median_filter_size": 3,
  "upscale_enabled": true       // 저해상도 대응
}
```

---

### 3. OCR 서비스(Prompt) 최적화 팁

현재 작성하신 `OCRService`의 프롬프트는 매우 훌륭합니다. 다만, 인식률(확률)을 더 높이기 위해 프롬프트의 **STEP 2** 부근에 아래 내용을 추가해 보세요.

* **좌표값 요청:** `"각 항목의 위치를 파악하며 읽어줘"`라는 암시를 주면 모델이 표 구조를 더 정확히 이해합니다.
* **한글 특화 지시:** `"거래처명이나 품목명에 포함된 한글 오타(예: '커피'를 '코피'로 인식)를 문맥에 맞게 교정해서 추출해줘"`라고 명시하면 AI의 사후 판단 능력이 개입되어 정확도가 올라갑니다.

---

### 4. 종합적인 인식률 향상 체크리스트

| **단계**     | **조치 사항**                | **기대 효과**                                             |
| ------------------ | ---------------------------------- | --------------------------------------------------------------- |
| **전처리**   | **Sharpening**필터 적용      | 흐릿한 스캔본의 글자 경계 강화                                  |
| **전처리**   | **Adaptive Resizing**        | 작은 영수증 글씨를 크게 키워 인식 오류 방지                     |
| **모델**     | **Gemini 2.0 Flash**우선순위 | 최신 모델일수록 노이즈 섞인 이미지 해석 능력이 압도적임         |
| **프롬프트** | **Zero-shot CoT**추가        | "먼저 전체 구조를 파악한 뒤, 표의 각 열을 순서대로 읽어라" 지시 |

현재 코드에서 `config_service.get_image_processing_config()`가 반환하는 객체에 `enhance_sharpness`와 같은 필드를 추가하여 관리하시면, 별도의 코드 수정 없이 JSON 파일만으로 현장에서 인식률을 튜닝하실 수 있습니다.

**다음 단계로, 추가된 전처리 옵션들이 실제로 이미지에 어떻게 적용되는지 확인할 수 있는 시각화(디버그용 저장) 코드가 필요하실까요?**
