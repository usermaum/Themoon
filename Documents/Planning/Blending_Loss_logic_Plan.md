# 블렌딩 손실률 로직 구현 계획 (Blending Loss Logic Implementation Plan)

> **문서 버전**: v1.0
> **관련 문서**: Documents/Planning/Themoon_Rostings_v2.md
> **작성 일자**: 2025-12-07

## 1. 개요 (Overview)

`Themoon_Rostings_v2.md` 문서의 2.2항 및 3.3항에 명시된 "블렌딩 시 각 품목별 손실률 적용" 요구사항을 구현하기 위한 기술적 계획입니다.
본 계획은 **선배합 후로스팅 (Pre-roast Blending)** 프로세스에서 각 구성 생두의 특성을 고려한 정확한 예상 필요 생두량을 산출하는 것을 목표로 합니다.

## 2. 문제 정의 및 해석 (Problem Definition)

* **요구사항**: "기준 손실률: 각 품목별로 정확한 손실률을 계산하여 적용"
* **프로세스**: 생두 혼합 -> 단일 로스팅 (Pre-roast Blending)
* **해석**: 물리적으로는 한 번에 로스팅되지만, 투입량 계산 시 **각 생두의 고유 손실률(예: 수분율 차이 등)**을 가중 평균하여 **"블렌드 전체의 예상 손실률"**을 동적으로 도출해야 합니다.

## 3. 구현 계획 (Implementation Plan)

### 3.1 데이터 모델 변경 (Data Model Changes)

`Bean` 모델(Green Bean)에 개별 손실률 속성을 추가하여, 각 생두가 로스팅될 때 평균적으로 발생하는 손실률을 관리합니다.

* **파일**: `backend/app/models/bean.py`
* **변경 내용**:

    ```python
    class Bean(Base):
        # ... 기존 필드 ...
        
        # 예상 손실률 (Default: 0.15 = 15%)
        # 품종, 가공 방식(Natural vs Washed)에 따라 다른 값 적용 가능
        expected_loss_rate = Column(Float, default=0.15, nullable=False, comment="예상 로스팅 손실률 (0.0 ~ 1.0)")
    ```

### 3.2 비즈니스 로직 구현 (Business Logic)

블렌드 생산 시뮬레이션 및 실행 시, 아래 공식을 적용하여 필요 생두량을 역산합니다.

* **파일**: `backend/app/services/roasting_service.py` (또는 `blend_service.py`)
* **로직 흐름**:
    1. 사용자가 **블렌드 목표 생산량(Target Weight)** 입력 (예: 10kg)
    2. 블렌드 레시피의 각 아이템(`bean_id`, `ratio`) 순회
    3. 각 생두의 `expected_loss_rate` 조회
    4. **가중 평균 손실률 (Weighted Average Loss Rate)** 계산:
        $$ L_{avg} = \sum (Ratio_i \times LossRate_i) $$
    5. **총 필요 생두량 (Total Green Bean Required)** 계산:
        $$ W_{total\_green} = \frac{W_{target}}{1 - L_{avg}} $$
    6. **개별 생두 투입량 (Individual Green Bean Weight)** 계산:
        $$ W_{green\_i} = W_{total\_green} \times Ratio_i $$

### 3.3 예시 시나리오 (Example Scenario)

* **블렌드**: 풀문 (Full Moon)
* **목표 생산량**: 10kg
* **레시피 및 생두 정보**:
  * 마사이 (40%): 손실률 18% (0.18) - *수분 많음*
  * 안티구아 (40%): 손실률 15% (0.15)
  * 모모라 (10%): 손실률 14% (0.14)
  * 시다모 (10%): 손실률 14% (0.14)

* **계산**:
    1. **가중 평균 손실률**:
        $(0.4 \times 0.18) + (0.4 \times 0.15) + (0.1 \times 0.14) + (0.1 \times 0.14)$
        $= 0.072 + 0.060 + 0.014 + 0.014 = 0.16$ **(16%)**
    2. **총 필요 생두량**:
        $10\text{kg} / (1 - 0.16) = 11.90\text{kg}$
    3. **개별 투입량**:
        * 마사이: $11.90 \times 0.4 = 4.76\text{kg}$
        * 안티구아: $11.90 \times 0.4 = 4.76\text{kg}$
        * 모모라: $11.90 \times 0.1 = 1.19\text{kg}$
        * 시다모: $11.90 \times 0.1 = 1.19\text{kg}$

## 4. 실행 계획 (Action Items)

1. [x] `recreate_db.py`에 블렌드 레시피(풀문, 뉴문, 이클립스문) 반영
2. [ ] `Bean` 모델에 `expected_loss_rate` 필드 추가 (Migration 필요)
3. [ ] `Blend` 상세 페이지 또는 `Roasting` 페이지에 위 계산 로직 적용된 "생산 시뮬레이터" 구현
