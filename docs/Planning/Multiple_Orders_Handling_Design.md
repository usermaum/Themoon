# 다중 주문번호 명세서 처리 시스템 설계안

> **작성일**: 2025-12-28
> **최종 수정**: 2025-12-28
> **버전**: 1.1.0
> **상태**: 승인 대기 중 (수정사항 반영 완료)
>
> **변경 이력**:
> - v1.1.0 (2025-12-28): 취소 플로우 개선 + 완료 후 동작 변경
> - v1.0.0 (2025-12-28): 초기 설계안 작성

---

## 📌 개요

### 문제 정의
현재 시스템은 하나의 입고 명세서에 **단일 주문번호**만 처리할 수 있습니다.
하지만 실무에서는 **하나의 명세서에 여러 주문번호**가 포함된 경우가 있습니다.

**예시**: `/coffee_bean_receiving_Specification/IMG_1660.JPG`
- 주문번호 #1: `20251108-8B7C2` (브라질 산토스 40kg, 494,000원)
- 주문번호 #2: `20250926-8BD28` (에티오피아 모모라 20kg, 430,000원)
- 주문번호 #3: `20250822-9533C` (에티오피아 모모라 40kg, 870,000원)

### 설계 철학
❌ **자동 분할**: 시스템이 임의로 3개 문서로 분리
✅ **사용자 선택적 처리**: 사용자가 각 주문을 검증하고 개별 입고 처리

---

## 🎯 핵심 요구사항

1. **OCR 분석 완료 시** 주문번호가 2개 이상이면 안내창 표시
2. **안내창**: "3개의 주문번호가 감지되었습니다" + 승인 버튼
3. **승인 시**: 주문별로 그룹화된 리스트 표시
4. **개별 처리**: 사용자가 각 주문을 선택하여 "추가" 클릭
5. **경고문**: "추가하면 리스트에서 삭제됩니다. 취소 불가능" 표시
6. **확인 후**: 해당 주문만 입고 상세 정보로 전송 → 재고 업데이트 → 리스트에서 삭제

---

## 🏗️ 아키텍처 설계

### 1. Data Flow

```
사용자 이미지 업로드
    ↓
OCR 분석 (Gemini/Claude)
    ↓
후처리: order_groups 생성
    ↓
has_multiple_orders == true?
    ↓
YES → Modal 표시 ("3개 주문 감지")
    ↓
사용자 승인
    ↓
주문별 리스트 표시 (Accordion/Card)
    ↓
사용자 주문 선택 → "추가" 버튼 클릭
    ↓
경고 Dialog ("취소 불가능")
    ↓
확인 클릭
    ↓
POST /api/v1/inbound/confirm (해당 주문만)
    ↓
재고 업데이트 + 리스트에서 삭제
    ↓
모든 주문 처리 완료? → Inbound 페이지 유지 + 데이터 초기화
```

---

## 📊 데이터 구조

### OCR 응답 스키마 (신규 필드)

```json
{
  "error": null,
  "has_multiple_orders": true,
  "total_order_count": 3,
  "order_groups": [
    {
      "order_number": "20251108-8B7C2",
      "order_date": "2025-11-08",
      "items": [
        {
          "bean_name": "브라질 산토스 NY2 FC (2)",
          "quantity": 40,
          "unit": "kg",
          "unit_price": 12350,
          "amount": 494000,
          "order_number": "20251108-8B7C2"
        }
      ],
      "subtotal": 494000
    },
    {
      "order_number": "20250926-8BD28",
      "order_date": "2025-09-26",
      "items": [
        {
          "bean_name": "에티오피아 모모라 내추럴 G1 (1)",
          "quantity": 20,
          "unit": "kg",
          "unit_price": 21500,
          "amount": 430000,
          "order_number": "20250926-8BD28"
        }
      ],
      "subtotal": 430000
    },
    {
      "order_number": "20250822-9533C",
      "order_date": "2025-08-22",
      "items": [
        {
          "bean_name": "(주간생두)에티오피아 모모라 내추럴 G1 (2)",
          "quantity": 40,
          "unit": "kg",
          "unit_price": 21750,
          "amount": 870000,
          "order_number": "20250822-9533C"
        }
      ],
      "subtotal": 870000
    }
  ],
  "document_info": { ... },
  "supplier": { ... },
  "amounts": {
    "total_amount": 1794000
  }
}
```

---

## 🎨 UI/UX 설계

### Phase 1: 안내 Modal

**트리거 조건**: `has_multiple_orders === true`

```tsx
<AlertDialog open={showMultiOrderModal}>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>
        <AlertTriangle className="w-6 h-6 text-amber-500" />
        다중 주문 감지
      </AlertDialogTitle>
      <AlertDialogDescription>
        이 명세서에는 <strong>3개의 주문 번호</strong>가 포함되어 있습니다.
        각 주문을 개별적으로 입고 처리할 수 있습니다.
      </AlertDialogDescription>
    </AlertDialogHeader>

    <div className="space-y-2">
      {/* 주문 번호 목록 미리보기 */}
      <div className="p-3 bg-latte-50 rounded-lg">
        <Badge>20251108-8B7C2</Badge>
        <span className="ml-2">1개 품목</span>
        <span className="ml-2 font-mono">494,000원</span>
      </div>
      <div className="p-3 bg-latte-50 rounded-lg">
        <Badge>20250926-8BD28</Badge>
        <span className="ml-2">1개 품목</span>
        <span className="ml-2 font-mono">430,000원</span>
      </div>
      <div className="p-3 bg-latte-50 rounded-lg">
        <Badge>20250822-9533C</Badge>
        <span className="ml-2">1개 품목</span>
        <span className="ml-2 font-mono">870,000원</span>
      </div>
    </div>

    <AlertDialogFooter>
      <AlertDialogCancel onClick={handleCancelMultiOrders}>취소</AlertDialogCancel>
      <AlertDialogAction onClick={handleAcceptMultiOrders}>
        확인 - 개별 처리 모드로 전환
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>

{/* 🆕 취소 확인 Dialog */}
<AlertDialog open={showCancelConfirmDialog}>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle className="text-amber-600">
        작업 취소 확인
      </AlertDialogTitle>
      <AlertDialogDescription>
        <div className="bg-amber-50 border-2 border-amber-200 rounded-lg p-4 mt-2">
          <p className="text-amber-900 font-bold">
            ⚠️ 모든 내용이 초기화됩니다
          </p>
          <p className="text-sm text-amber-800 mt-2">
            진행 중인 OCR 분석 결과가 모두 삭제되며, 복구할 수 없습니다.
          </p>
        </div>
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel onClick={() => setShowCancelConfirmDialog(false)}>
        돌아가기
      </AlertDialogCancel>
      <AlertDialogAction
        onClick={confirmCancelWork}
        className="bg-amber-600 hover:bg-amber-700"
      >
        확인 - 작업 취소
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

---

### Phase 2: 주문별 리스트 (Accordion/Card)

**상태**: `pendingOrders` (Array of OrderGroup)

```tsx
<div className="space-y-4">
  <div className="flex justify-between items-center mb-4">
    <h2 className="text-2xl font-bold">입고 대기 주문 목록</h2>
    <Badge variant="secondary">
      {pendingOrders.length}개 주문 대기 중
    </Badge>
  </div>

  {pendingOrders.map((orderGroup, index) => (
    <Card key={orderGroup.order_number} className="border-2">
      <CardHeader>
        <CardTitle className="flex justify-between items-center">
          <div>
            <Badge variant="outline" className="text-base">
              {orderGroup.order_number}
            </Badge>
            <span className="ml-3 text-sm text-gray-500">
              {orderGroup.order_date}
            </span>
          </div>
          <span className="font-mono font-bold text-lg">
            {orderGroup.subtotal.toLocaleString()}원
          </span>
        </CardTitle>
      </CardHeader>

      <CardContent>
        <table className="w-full">
          <thead className="bg-latte-50">
            <tr>
              <th className="text-left p-2">품명</th>
              <th className="text-right p-2">수량</th>
              <th className="text-right p-2">단가</th>
              <th className="text-right p-2">금액</th>
            </tr>
          </thead>
          <tbody>
            {orderGroup.items.map((item, idx) => (
              <tr key={idx} className="border-t">
                <td className="p-2">{item.bean_name}</td>
                <td className="text-right p-2">
                  {item.quantity} {item.unit}
                </td>
                <td className="text-right p-2">
                  {item.unit_price.toLocaleString()}원
                </td>
                <td className="text-right p-2 font-bold">
                  {item.amount.toLocaleString()}원
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </CardContent>

      <CardFooter>
        <Button
          onClick={() => handleAddOrder(orderGroup, index)}
          className="w-full bg-green-600 hover:bg-green-700"
          size="lg"
        >
          <Plus className="w-5 h-5 mr-2" />
          이 주문 입고 처리하기
        </Button>
      </CardFooter>
    </Card>
  ))}
</div>
```

---

### Phase 3: 경고 Dialog

**트리거**: "추가" 버튼 클릭

```tsx
<AlertDialog open={showConfirmDialog}>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle className="text-red-600 flex items-center gap-2">
        <AlertTriangle className="w-6 h-6" />
        입고 처리 확인
      </AlertDialogTitle>
      <AlertDialogDescription>
        <div className="space-y-3">
          <p className="font-bold text-base text-gray-900">
            주문번호: {selectedOrder?.order_number}
          </p>
          <p className="text-sm text-gray-600">
            총 {selectedOrder?.items.length}개 품목 /
            {selectedOrder?.subtotal.toLocaleString()}원
          </p>

          <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4">
            <p className="text-red-900 font-bold mb-2">
              ⚠️ 주의사항
            </p>
            <ul className="list-disc list-inside text-sm text-red-800 space-y-1">
              <li><strong>입고 처리 후 리스트에서 삭제됩니다</strong></li>
              <li><strong>취소 불가능합니다</strong></li>
              <li>재고가 즉시 업데이트됩니다</li>
              <li>입고 내역이 데이터베이스에 저장됩니다</li>
            </ul>
          </div>
        </div>
      </AlertDialogDescription>
    </AlertDialogHeader>

    <AlertDialogFooter>
      <AlertDialogCancel>취소</AlertDialogCancel>
      <AlertDialogAction
        onClick={() => confirmAddOrder(selectedOrderIndex)}
        className="bg-red-600 hover:bg-red-700"
      >
        확인 - 입고 처리
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

---

## 💻 백엔드 구현

### 1. Database Migration

**파일**: `backend/app/models/inbound_item.py`

```python
# 신규 컬럼 추가
class InboundItem(Base):
    __tablename__ = "inbound_items"

    # ... 기존 필드들

    # NEW: 각 항목별 주문번호
    order_number = Column(String(100), nullable=True, index=True)
```

**Migration SQL**:
```sql
ALTER TABLE inbound_items
ADD COLUMN order_number VARCHAR(100);

CREATE INDEX idx_inbound_items_order_number
ON inbound_items(order_number);
```

---

### 2. OCR 프롬프트 수정

**파일**: `backend/app/resources/ocr_prompt_structure.json`

```json
{
  "items": [
    {
      "item_number": "순번, No",
      "order_number": "주문번호, Order No (YYYYMMDD-XXXXX 형식)",
      "bean_name": "품명, 원두명",
      "quantity": "수량 (Number)",
      "unit": "단위 (kg, bag, etc.)",
      "unit_price": "단가 (Number)",
      "amount": "금액 (Number)"
    }
  ]
}
```

**프롬프트 추가 지시사항**:
```
STEP 5-1. ORDER NUMBER EXTRACTION (NEW)
────────────────────────────────────────
If the document contains MULTIPLE order numbers (주문번호) for different items:

1. Each item MUST include its corresponding "order_number" field.
2. Format: YYYYMMDD-XXXXX (e.g., "20251108-8B7C2")
3. If order number appears in a column header or next to the item, extract it.
4. If unclear, extract from context (date + identifier pattern).

Example:
- Row 1: "20251108-8B7C2 브라질 산토스..." → order_number: "20251108-8B7C2"
- Row 2: "20250926-8BD28 에티오피아..." → order_number: "20250926-8BD28"
```

---

### 3. OCR 후처리 로직

**파일**: `backend/app/services/ocr_service.py`

```python
def _post_process_ocr_result(self, result: dict) -> dict:
    """
    OCR 결과를 후처리하여 주문별로 그룹화

    Returns:
        Enhanced result with:
        - has_multiple_orders: bool
        - total_order_count: int
        - order_groups: List[OrderGroup]
    """
    items = result.get("items", [])

    if not items:
        result["has_multiple_orders"] = False
        result["total_order_count"] = 0
        result["order_groups"] = []
        return result

    # 주문번호로 그룹화
    order_groups = {}

    for item in items:
        order_num = item.get("order_number") or "UNKNOWN"

        if order_num not in order_groups:
            order_groups[order_num] = {
                "order_number": order_num,
                "order_date": None,  # Extract from order_number (YYYYMMDD)
                "items": [],
                "subtotal": 0
            }

        order_groups[order_num]["items"].append(item)
        order_groups[order_num]["subtotal"] += item.get("amount", 0)

    # 주문 날짜 추출 (YYYYMMDD-XXXXX 형식에서)
    import re
    for group in order_groups.values():
        order_num = group["order_number"]
        match = re.match(r"^(\d{4})(\d{2})(\d{2})", order_num)
        if match:
            year, month, day = match.groups()
            group["order_date"] = f"{year}-{month}-{day}"

    # 결과 enrichment
    order_groups_list = list(order_groups.values())
    result["has_multiple_orders"] = len(order_groups_list) > 1
    result["total_order_count"] = len(order_groups_list)
    result["order_groups"] = order_groups_list

    return result

# analyze_image_stream()에서 호출
async def analyze_image_stream(self, image_bytes: bytes, mime_type: str = "image/jpeg"):
    # ... 기존 로직

    result_json = self._clean_and_parse_json(text_result)

    # 🆕 후처리 추가
    result_json = self._post_process_ocr_result(result_json)

    yield {"status": "complete", "data": result_json}
```

---

## 🎨 프론트엔드 구현

### 1. State 관리

**파일**: `frontend/app/inventory/inbound/page.tsx`

```typescript
'use client';

import { useState } from 'react';

interface OrderGroup {
  order_number: string;
  order_date: string;
  items: any[];
  subtotal: number;
}

export default function InboundPage() {
  // 기존 state
  const [ocrResult, setOcrResult] = useState(null);

  // 🆕 다중 주문 관련 state
  const [hasMultipleOrders, setHasMultipleOrders] = useState(false);
  const [totalOrderCount, setTotalOrderCount] = useState(0);
  const [orderGroups, setOrderGroups] = useState<OrderGroup[]>([]);

  // 🆕 Modal state
  const [showMultiOrderModal, setShowMultiOrderModal] = useState(false);
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);
  const [showCancelConfirmDialog, setShowCancelConfirmDialog] = useState(false);  // 🆕 취소 확인

  // 🆕 Pending orders (사용자가 아직 처리하지 않은 주문들)
  const [pendingOrders, setPendingOrders] = useState<OrderGroup[]>([]);
  const [selectedOrderIndex, setSelectedOrderIndex] = useState<number | null>(null);

  // ... 기존 로직
}
```

---

### 2. OCR 완료 후 처리

```typescript
const handleOCRComplete = (result: any) => {
  setOcrResult(result);

  // 🆕 다중 주문 체크
  if (result.has_multiple_orders) {
    setHasMultipleOrders(true);
    setTotalOrderCount(result.total_order_count);
    setOrderGroups(result.order_groups);
    setShowMultiOrderModal(true);  // Modal 표시
  } else {
    // 기존 플로우 (단일 주문)
    // ...
  }
};

const handleAcceptMultiOrders = () => {
  setShowMultiOrderModal(false);
  setPendingOrders([...orderGroups]);  // 모든 주문을 대기 리스트로
};

const handleCancelMultiOrders = () => {
  setShowMultiOrderModal(false);
  setShowCancelConfirmDialog(true);  // 🆕 취소 확인 Dialog 표시
};

const confirmCancelWork = () => {
  // 🆕 모든 데이터 초기화
  setOcrResult(null);
  setHasMultipleOrders(false);
  setOrderGroups([]);
  setPendingOrders([]);
  setShowCancelConfirmDialog(false);

  toast.info('작업이 취소되었습니다. 모든 데이터가 초기화되었습니다.');
};
```

---

### 3. 개별 주문 처리

```typescript
const handleAddOrder = (orderGroup: OrderGroup, index: number) => {
  setSelectedOrderIndex(index);
  setShowConfirmDialog(true);
};

const confirmAddOrder = async (index: number) => {
  if (index === null) return;

  const orderGroup = pendingOrders[index];

  try {
    // POST /api/v1/inbound/confirm
    const response = await fetch('/api/v1/inbound/confirm', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        document: {
          contract_number: orderGroup.order_number,  // 핵심!
          supplier_name: ocrResult.supplier.name,
          supplier_id: selectedSupplierId,
          total_amount: orderGroup.subtotal,
          invoice_date: orderGroup.order_date,
        },
        items: orderGroup.items,  // 해당 주문의 items만
        supplier: ocrResult.supplier,
        // ... 기타 필드
      })
    });

    if (!response.ok) {
      throw new Error('입고 처리 실패');
    }

    // 성공: 리스트에서 삭제
    setPendingOrders(prev => prev.filter((_, i) => i !== index));
    setShowConfirmDialog(false);

    toast.success(`${orderGroup.order_number} 입고 처리 완료`);

    // 🆕 모든 주문 처리 완료?
    if (pendingOrders.length === 1) {
      toast.success('모든 주문 처리 완료!');

      // /inventory로 이동 대신 데이터 초기화
      setOcrResult(null);
      setHasMultipleOrders(false);
      setOrderGroups([]);
      setPendingOrders([]);

      // Inbound 페이지 유지, 새 명세서 업로드 가능 상태
    }

  } catch (error) {
    toast.error('입고 처리 중 오류 발생');
    console.error(error);
  }
};
```

---

## 📋 구현 체크리스트

### Backend (Agent 3)

- [ ] **DB Migration**
  - [ ] `inbound_items.order_number` 컬럼 추가 (VARCHAR 100, nullable)
  - [ ] Index 생성: `idx_inbound_items_order_number`

- [ ] **OCR 프롬프트 수정**
  - [ ] `ocr_prompt_structure.json`에 `order_number` 필드 추가
  - [ ] STEP 5-1 지시사항 추가 (다중 주문번호 추출)

- [ ] **OCR Service 개선**
  - [ ] `_post_process_ocr_result()` 함수 구현
  - [ ] `analyze_image_stream()`에서 후처리 호출
  - [ ] 주문 날짜 자동 추출 로직 (YYYYMMDD 파싱)

- [ ] **API 응답 스키마**
  - [ ] `has_multiple_orders`, `total_order_count`, `order_groups` 필드 추가

---

### Frontend (Agent 2)

- [ ] **State 관리**
  - [ ] `hasMultipleOrders`, `orderGroups`, `pendingOrders` state 추가

- [ ] **UI 컴포넌트**
  - [ ] Multi-Order Detection Modal 구현
  - [ ] Cancel Confirmation Dialog 구현 (🆕 취소 확인)
  - [ ] Pending Orders List (Accordion/Card) 구현
  - [ ] Add Order Confirmation Dialog 구현 (입고 처리 경고문)

- [ ] **비즈니스 로직**
  - [ ] `handleOCRComplete()` - 다중 주문 감지 로직
  - [ ] `handleAcceptMultiOrders()` - 승인 후 리스트 표시
  - [ ] `handleCancelMultiOrders()` - 🆕 취소 버튼 클릭 시 확인 Dialog 표시
  - [ ] `confirmCancelWork()` - 🆕 취소 확인 후 데이터 초기화
  - [ ] `handleAddOrder()` - 개별 주문 선택
  - [ ] `confirmAddOrder()` - 입고 처리 및 리스트 삭제

- [ ] **UX 개선**
  - [ ] Toast 알림 (성공/실패)
  - [ ] 모든 주문 처리 완료 시 데이터 초기화 (Inbound 페이지 유지)
  - [ ] 취소 시 확인 Dialog 표시
  - [ ] Loading state 처리

---

### Testing

- [ ] **단위 테스트**
  - [ ] `_post_process_ocr_result()` 함수 테스트
  - [ ] 주문 날짜 추출 로직 테스트

- [ ] **통합 테스트**
  - [ ] Mock OCR 데이터로 3개 주문 케이스 테스트
  - [ ] 1개 주문 → 기존 플로우 정상 작동 확인

- [ ] **E2E 테스트**
  - [ ] 이미지 업로드 → OCR → Modal → 개별 처리 → 완료
  - [ ] 중간에 취소 시나리오
  - [ ] 모든 주문 처리 완료 플로우

---

## 🔄 플로우 다이어그램 (상세)

```
┌──────────────────────────────────────────────────────┐
│ START: 사용자가 명세서 이미지 업로드                   │
└────────────────────┬─────────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────────┐
│ OCR 분석 시작 (Gemini/Claude)                         │
│ - 이미지 파싱                                         │
│ - items 배열 추출                                     │
│ - 각 item의 order_number 추출                         │
└────────────────────┬─────────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────────┐
│ Backend 후처리: _post_process_ocr_result()            │
│ - items를 order_number로 그룹화                       │
│ - order_groups 생성 (주문별 items + subtotal)         │
│ - has_multiple_orders 플래그 설정                     │
└────────────────────┬─────────────────────────────────┘
                     ▼
              [주문 개수 확인]
                     │
        ┌────────────┴────────────┐
        │                         │
   1개 주문                   2개 이상 주문
        │                         │
        ▼                         ▼
┌──────────────┐      ┌────────────────────────────────┐
│ 기존 플로우   │      │ 🆕 MODAL 표시                   │
│ (변경 없음)   │      │ "3개의 주문번호가 감지되었습니다" │
└──────────────┘      │ - 주문 목록 미리보기             │
                      │ - [취소] [확인] 버튼             │
                      └──────────┬─────────────────────┘
                                 ▼
                        [사용자 버튼 선택]
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                  [취소]                    [확인]
                    │                         │
                    ▼                         ▼
         ┌────────────────────┐    ┌──────────────────────┐
         │ 🆕 취소 확인 Dialog │    │ 개별 처리 모드 진입   │
         │ "모든 내용 초기화"  │    │ pendingOrders 설정   │
         └──────────┬─────────┘    └──────────┬───────────┘
                    ▼                         ▼
           [확인 - 작업 취소]
                    │
                    ▼
         ┌────────────────────┐
         │ 데이터 초기화       │
         │ Inbound 페이지 유지 │
         └────────────────────┘
                                              ▼
                                   ┌─────────────────────────┐
                                   │ 🆕 주문별 리스트 표시     │
                                   │ (Accordion/Card UI)      │
                                   │ - 주문 #1 (Card)         │
                                   │ - 주문 #2 (Card)         │
                                   │ - 주문 #3 (Card)         │
                                   │ 각 Card에 [추가] 버튼    │
                                   └──────────┬──────────────┘
                                              ▼
                                   [사용자 주문 선택]
                                              │
                          ┌───────────────────┼───────────────────┐
                          ▼                   ▼                   ▼
                    [주문 #1 추가]       [주문 #2 추가]       [주문 #3 추가]
                          │                   │                   │
                          ▼                   ▼                   ▼
              ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
              │ 🆕 경고 Dialog    │ │ 🆕 경고 Dialog    │ │ 🆕 경고 Dialog    │
              │ "취소 불가능"     │ │ "취소 불가능"     │ │ "취소 불가능"     │
              │ "리스트 삭제"     │ │ "리스트 삭제"     │ │ "리스트 삭제"     │
              │ [취소][확인]      │ │ [취소][확인]      │ │ [취소][확인]      │
              └─────────┬────────┘ └─────────┬────────┘ └─────────┬────────┘
                        ▼                    ▼                    ▼
                   [확인 클릭]          [확인 클릭]          [확인 클릭]
                        │                    │                    │
                        ▼                    ▼                    ▼
           ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
           │ POST /inbound/confirm│ │ POST /inbound/confirm│ │ POST /inbound/confirm│
           │ contract_number:     │ │ contract_number:     │ │ contract_number:     │
           │ "20251108-8B7C2"     │ │ "20250926-8BD28"     │ │ "20250822-9533C"     │
           │ items: [브라질]      │ │ items: [에티오피아1] │ │ items: [에티오피아2] │
           └──────────┬──────────┘ └──────────┬──────────┘ └──────────┬──────────┘
                      ▼                       ▼                       ▼
           ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
           │ InboundDocument     │ │ InboundDocument     │ │ InboundDocument     │
           │ 생성 (DB)           │ │ 생성 (DB)           │ │ 생성 (DB)           │
           └──────────┬──────────┘ └──────────┬──────────┘ └──────────┬──────────┘
                      ▼                       ▼                       ▼
           ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
           │ InventoryLog 생성   │ │ InventoryLog 생성   │ │ InventoryLog 생성   │
           │ 재고 +40kg          │ │ 재고 +20kg          │ │ 재고 +40kg          │
           └──────────┬──────────┘ └──────────┬──────────┘ └──────────┬──────────┘
                      ▼                       ▼                       ▼
           ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
           │ 리스트에서 삭제      │ │ 리스트에서 삭제      │ │ 리스트에서 삭제      │
           │ pendingOrders[0]    │ │ pendingOrders[0]    │ │ pendingOrders[0]    │
           └──────────┬──────────┘ └──────────┬──────────┘ └──────────┬──────────┘
                      ▼                       ▼                       ▼
                 [Toast: 성공]           [Toast: 성공]           [Toast: 성공]
                      │                       │                       │
                      └───────────────────────┴───────────────────────┘
                                              ▼
                                   [pendingOrders.length === 0?]
                                              │
                                      ┌───────┴───────┐
                                     YES             NO
                                      │               │
                                      ▼               ▼
                          ┌──────────────────────┐  [대기 중]
                          │ 🆕 모든 주문 완료!     │  (추가 처리 가능)
                          │ - Toast 메시지 표시   │
                          │ - 데이터 초기화       │
                          │ - Inbound 페이지 유지 │
                          │ (새 명세서 업로드 가능)│
                          └──────────────────────┘
```

---

## 🎬 사용자 시나리오 예시

### 시나리오 1: 정상 플로우 (3개 주문 모두 처리)

1. **업로드**: 사용자가 IMG_1660.JPG 업로드
2. **OCR**: "3개의 주문번호가 감지되었습니다" Modal 표시
3. **승인**: 사용자가 "확인" 클릭
4. **리스트 표시**: 3개 주문 카드 표시
5. **첫 번째 주문 처리**:
   - "20251108-8B7C2 추가" 클릭
   - 경고문 확인
   - 입고 완료 → 리스트에서 삭제
6. **두 번째 주문 처리**: 동일 과정 반복
7. **세 번째 주문 처리**: 동일 과정 반복
8. **완료**: "모든 주문 처리 완료!" Toast 메시지 → Inbound 페이지 유지 + 데이터 초기화 (새 명세서 업로드 가능)

---

### 시나리오 2: 일부만 처리 (나머지는 보류)

1. **업로드**: IMG_1660.JPG 업로드
2. **OCR**: Modal 표시 → 승인
3. **첫 번째 주문만 처리**: 20251108-8B7C2 입고
4. **나머지 보류**: 리스트에 2개 주문 남아있음
5. **나중에 처리**: 사용자가 다시 와서 남은 주문 처리 가능
   - ⚠️ **제약**: 새로고침 시 데이터 손실 (Session Storage 필요 시 추가 구현)

---

### 시나리오 3: 취소

1. **업로드**: IMG_1660.JPG 업로드
2. **OCR**: "3개의 주문번호가 감지되었습니다" Modal 표시
3. **취소**: "취소" 버튼 클릭
4. **확인 Dialog**: "⚠️ 모든 내용이 초기화됩니다" 경고 표시
5. **확인**: "확인 - 작업 취소" 클릭
6. **결과**: OCR 분석 결과 모두 삭제, Inbound 페이지 초기 상태로 복원

---

## 🔧 추가 고려사항

### 1. Session Persistence (선택 사항)
현재 설계는 **메모리 기반 상태 관리**입니다.
새로고침 시 `pendingOrders` 손실 → 사용자가 다시 OCR 수행 필요

**개선안**:
```typescript
// Session Storage에 저장
useEffect(() => {
  if (pendingOrders.length > 0) {
    sessionStorage.setItem('pendingOrders', JSON.stringify(pendingOrders));
  }
}, [pendingOrders]);

// 페이지 로드 시 복원
useEffect(() => {
  const saved = sessionStorage.getItem('pendingOrders');
  if (saved) {
    setPendingOrders(JSON.parse(saved));
  }
}, []);
```

---

### 2. 주문 상태 표시
리스트에 각 주문의 처리 상태 표시:
- 🟢 **대기 중** (Pending)
- 🔵 **처리 중** (Processing)
- ✅ **완료** (Completed)

---

### 3. Batch Processing (선택 사항)
"모두 입고 처리" 버튼 추가:
```tsx
<Button onClick={handleBatchProcess}>
  <CheckCircle className="w-4 h-4 mr-2" />
  모든 주문 일괄 처리
</Button>
```

---

## 📝 승인 체크리스트

**메니저님 승인 전 확인사항**:

- [ ] OCR 분석 시 주문별 그룹화 로직 이해
- [ ] Modal → 리스트 → 경고 → 입고 플로우 확인
- [ ] "취소 불가능" 경고문 적절성 검토
- [ ] UI/UX 디자인 방향 확인
- [ ] 추가 요구사항 또는 변경사항 있는지 확인

---

## 📅 다음 단계

**승인 후 진행 순서**:

1. **가상 테스트** (Mock Data)
   - OCR 응답 Mock JSON 생성
   - Frontend 로직 테스트
   - 플로우 검증

2. **실제 구현**
   - Backend: DB Migration + OCR 수정
   - Frontend: UI 컴포넌트 구현
   - E2E 테스트

3. **배포**
   - Staging 환경 테스트
   - Production 배포

---

**작성자**: Claude Sonnet 4.5
**검토자**: 메니저
**승인 상태**: 🟡 대기 중
