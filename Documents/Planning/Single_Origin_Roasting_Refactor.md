# 싱글 오리진 로스팅 리팩토링 계획

## 1. 개요 (Overview)

현재 싱글 오리진 로스팅 페이지는 **결과 기록 중심(Log-Driven)**의 UI를 가지고 있습니다. 사용자는 투입량과 배출량을 모두 직접 입력해야 로스팅을 수행할 수 있습니다.
이는 "내가 원두 10kg를 만들려면 생두를 얼마나 넣어야 하지?"라는 생산 계획 수립(Production Planning) 단계에서 불편함을 초래합니다.

이에 **블렌드 로스팅 페이지의 "목표 생산량 중심(Goal-Driven)" 로직**을 싱글 오리진 로스팅에도 도입하여, 생산 편의성을 높이고 UI/UX를 통일하고자 합니다.

---

## 2. 주요 변경 사항 (Key Changes)

### 2.1 로직 변경: 목표량 기반 역산(Reverse Calculation) 도입

* **AS-IS**: 사용자 투입량(Input) 입력 -> 배출량(Output) 입력 -> 손실률(Loss) 사후 계산
* **TO-BE**: 사용자 목표량(Target Output) 입력 -> **필요 투입량(Required Input) 자동 계산** (DB의 `expected_loss_rate` 활용)

### 2.2 UI 구조 변경: 2-Column 레이아웃

* 블렌드 페이지와 동일한 2-Column 구조로 변경하여 정보 가독성 향상
  * **좌측 (설정)**: 생두 선택, 프로필 선택, 목표 생산량 입력
  * **우측 (명세/결과)**: 예상 손실률, 필요 생두량, 재고 현황(부족 여부), 시뮬레이션 결과

---

## 3. 상세 구현 계획 (Implementation Details)

### 3.1 상태 관리 (State Management)

* `targetWeight` (목표 생산량) 상태 추가
* `isSimulationMode` (시뮬레이션 모드) 토글 또는 자동 감지

### 3.2 계산 로직 (Calculation Logic)

생두의 `expected_loss_rate`가 15%(0.15)이고, 목표 원두 생산량이 10kg인 경우:

```typescript
const lossRate = bean.expected_loss_rate || 0.15; // 기본값 15%
const requiredInput = targetWeight / (1 - lossRate);
// 예: 10 / 0.85 = 11.76kg
```

### 3.3 페이지 로직 흐름

1. 사용자가 **생두**와 **로스팅 프로필**을 선택한다.
2. 사용자가 **목표 생산량(kg)**을 입력한다.
3. 시스템이 **필요 생두량**을 실시간으로 계산하여 우측 패널에 보여준다.
4. 동시에 현재 생두 **재고 부족 여부**를 체크하여 경고(Badge)를 표시한다.
5. [로스팅 실행] 버튼 클릭 시:
    * 계산된 투입량(`requiredInput`)과 목표 배출량(`targetWeight`)을 API로 전송한다.
    * 실제 로스팅에서는 오차가 발생할 수 있으므로, 최종 확인 팝업에서 수치를 미세 조정할 수 있게 한다. (선택 사항)

---

## 4. UI 디자인 (Draft)

### 좌측 패널 (Control Panel)

* **헤더**: 생산 설정 (Calculator Icon)
* **폼**:
  * 생두 선택 (Select) - 잔여 재고 표시
  * 로스팅 포인트 (Radio: Light/Medium/Dark)
  * 목표 생산량 (Input: kg)

### 우측 패널 (Simulation Board)

* **헤더**: 생산 명세서 (Bill of Materials)
* **정보 카드**:
  * 선택된 생두 정보 (원산지/품종)
  * 적용 손실률 (`expected_loss_rate`)
  * **필요 투입량 (Highlight)**
  * 현재 재고 상태 (충분/부족)
* **알림**: 재고 부족 시 붉은색 경고 메시지 및 실행 버튼 비활성화/경고 팝업

---

## 5. 기대 효과

1. **일관성**: 블렌드와 싱글 오리진 로스팅의 사용자 경험 통일
2. **편의성**: 복잡한 계산 없이 목표량만 입력하면 됨
3. **정확성**: DB에 저장된 생두별 특성(손실률)을 활용하여 더 정확한 생산 계획 수립 가능
