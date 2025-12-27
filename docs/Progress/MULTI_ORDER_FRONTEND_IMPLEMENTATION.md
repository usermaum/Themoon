# 다중 주문 처리 시스템 - Frontend 구현 완료 보고서

> **작성일**: 2025-12-28
> **버전**: 1.0.0
> **상태**: ✅ 구현 완료 (Backend 연동 대기)

---

## 📌 개요

### 구현 범위
하나의 명세서에 여러 주문번호가 포함된 경우를 처리하는 Frontend 시스템 구현 완료.

**구현 파일**:
- `/mnt/d/Ai/WslProject/Themoon/frontend/app/inventory/inbound/page.tsx`

**설계 문서 참조**:
- `/mnt/d/Ai/WslProject/Themoon/docs/Planning/Multiple_Orders_Handling_Design.md`

---

## ✅ 구현 완료 항목

### 1. TypeScript 타입 정의

```typescript
interface InboundItem {
  bean_name: string;
  quantity: number;
  unit_price: number;
  amount: number;
  order_number?: string;  // 🆕 추가
}

interface OrderGroup {
  order_number: string;
  order_date: string;
  items: InboundItem[];
  subtotal: number;
}
```

### 2. State 관리

#### 다중 주문 State
```typescript
const [hasMultipleOrders, setHasMultipleOrders] = useState(false);
const [totalOrderCount, setTotalOrderCount] = useState(0);
const [orderGroups, setOrderGroups] = useState<OrderGroup[]>([]);
```

#### Modal State
```typescript
const [showMultiOrderModal, setShowMultiOrderModal] = useState(false);
const [showConfirmDialog, setShowConfirmDialog] = useState(false);
const [showCancelConfirmDialog, setShowCancelConfirmDialog] = useState(false);
```

#### Pending Orders
```typescript
const [pendingOrders, setPendingOrders] = useState<OrderGroup[]>([]);
const [selectedOrderIndex, setSelectedOrderIndex] = useState<number | null>(null);
```

### 3. Event Handlers

#### `handleAnalyze` 수정
OCR 완료 후 다중 주문 감지 로직 추가:

```typescript
if (data.has_multiple_orders) {
  setHasMultipleOrders(true);
  setTotalOrderCount(data.total_order_count);
  setOrderGroups(data.order_groups);
  setShowMultiOrderModal(true);
  toast({
    title: '다중 주문 감지',
    description: `${data.total_order_count}개의 주문번호가 발견되었습니다.`
  });
  return; // 단일 주문 플로우 건너뛰기
}
```

#### `handleAcceptMultiOrders`
사용자가 다중 주문을 승인할 때:

```typescript
const handleAcceptMultiOrders = () => {
  setShowMultiOrderModal(false);
  setPendingOrders([...orderGroups]);
  toast({
    title: '개별 처리 모드',
    description: '각 주문을 개별적으로 처리할 수 있습니다.',
  });
};
```

#### `handleCancelMultiOrders` & `confirmCancelWork`
사용자가 작업을 취소할 때 (2단계 확인):

```typescript
const handleCancelMultiOrders = () => {
  setShowMultiOrderModal(false);
  setShowCancelConfirmDialog(true);
};

const confirmCancelWork = () => {
  // 모든 상태 초기화
  setOcrResult(null);
  setHasMultipleOrders(false);
  setOrderGroups([]);
  setPendingOrders([]);
  setShowCancelConfirmDialog(false);
  // ... 기타 초기화

  toast({
    title: '작업 취소',
    description: '모든 데이터가 초기화되었습니다.',
  });
};
```

#### `handleAddOrder` & `confirmAddOrder`
개별 주문 처리:

```typescript
const handleAddOrder = (orderGroup: OrderGroup, index: number) => {
  setSelectedOrderIndex(index);
  setShowConfirmDialog(true);
};

const confirmAddOrder = async () => {
  if (selectedOrderIndex === null) return;

  const orderGroup = pendingOrders[selectedOrderIndex];

  // POST /api/v1/inbound/confirm 호출
  const payload = {
    items: orderGroup.items,
    document: {
      contract_number: orderGroup.order_number,  // 핵심!
      supplier_name: ocrResult?.supplier?.name || '',
      invoice_date: orderGroup.order_date,
      total_amount: orderGroup.subtotal,
      // ... 기타 필드
    },
    // ... OCR 데이터
  };

  // API 호출 후 성공 시
  const newPendingOrders = pendingOrders.filter((_, i) => i !== selectedOrderIndex);
  setPendingOrders(newPendingOrders);

  // 모든 주문 처리 완료 체크
  if (newPendingOrders.length === 0) {
    toast({
      title: '모든 주문 처리 완료',
      description: '모든 주문이 성공적으로 입고 처리되었습니다.',
    });
    // 데이터 초기화 (Inbound 페이지 유지)
  }
};
```

### 4. UI 컴포넌트

#### 4.1 Multi-Order Detection Modal
**트리거**: `showMultiOrderModal === true`

**특징**:
- 감지된 주문 개수 표시
- 각 주문의 주문번호, 날짜, 품목 수, 금액 미리보기
- 2개의 액션: "취소", "확인 - 개별 처리 모드로 전환"

**주요 코드**:
```tsx
<AlertDialog open={showMultiOrderModal} onOpenChange={setShowMultiOrderModal}>
  <AlertDialogContent className="max-w-2xl">
    <AlertDialogTitle className="flex items-center gap-2 text-amber-600">
      <AlertCircle className="w-6 h-6" />
      다중 주문 감지
    </AlertDialogTitle>

    <div className="space-y-2 max-h-96 overflow-y-auto">
      {orderGroups.map((order, index) => (
        <div className="p-3 bg-latte-50 rounded-lg">
          <Badge variant="outline">{order.order_number}</Badge>
          <span>{order.items.length}개 품목</span>
          <span>{formatCurrency(order.subtotal)}</span>
        </div>
      ))}
    </div>

    <AlertDialogFooter>
      <AlertDialogCancel onClick={handleCancelMultiOrders}>취소</AlertDialogCancel>
      <AlertDialogAction onClick={handleAcceptMultiOrders}>
        확인 - 개별 처리 모드로 전환
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

#### 4.2 Cancel Confirmation Dialog
**트리거**: `showCancelConfirmDialog === true`

**특징**:
- ⚠️ 경고 스타일 (amber 색상)
- "모든 내용이 초기화됩니다" 명확한 경고문
- 2개의 액션: "돌아가기", "확인 - 작업 취소"

#### 4.3 Pending Orders List (Modal)
**트리거**: `pendingOrders.length > 0`

**특징**:
- Fixed overlay (z-50)
- Card 레이아웃
- 각 주문별 상세 테이블
- "이 주문 입고 처리하기" 버튼

**주요 코드**:
```tsx
{pendingOrders.length > 0 && (
  <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
    <Card className="w-full max-w-5xl max-h-[90vh] overflow-y-auto">
      <CardHeader>
        <CardTitle>입고 대기 주문 목록</CardTitle>
        <Badge>{pendingOrders.length}개 주문 대기 중</Badge>
      </CardHeader>

      <CardContent>
        {pendingOrders.map((orderGroup, index) => (
          <Card key={orderGroup.order_number}>
            {/* 주문 상세 테이블 */}
            <Button onClick={() => handleAddOrder(orderGroup, index)}>
              이 주문 입고 처리하기
            </Button>
          </Card>
        ))}
      </CardContent>
    </Card>
  </div>
)}
```

#### 4.4 Add Order Confirmation Dialog
**트리거**: `showConfirmDialog === true`

**특징**:
- 🔴 위험 스타일 (red 색상)
- 선택한 주문의 상세 정보 표시
- ⚠️ 주의사항 목록 (입고 처리 후 삭제, 취소 불가능, 즉시 재고 업데이트)

---

## 🔄 플로우 다이어그램

```
사용자 이미지 업로드
    ↓
OCR 분석 완료
    ↓
has_multiple_orders === true?
    │
    ├─ NO → 기존 단일 주문 플로우 (변경 없음)
    │
    └─ YES → Multi-Order Detection Modal 표시
         ↓
    [사용자 선택]
         │
    ┌────┴────┐
    │         │
  [취소]   [확인]
    │         │
    ↓         ↓
Cancel    Pending Orders List 표시
Confirm       │
Dialog        ↓
    │    [주문 선택 → "추가" 클릭]
    │         │
    ↓         ↓
데이터   Add Order Confirmation Dialog
초기화       │
            ↓
       [확인 클릭]
            │
            ↓
       POST /api/v1/inbound/confirm
            │
            ↓
       리스트에서 삭제
            │
            ↓
       모든 주문 완료?
            │
       ┌────┴────┐
       │         │
      YES       NO
       │         │
       ↓         ↓
    데이터   대기 중
    초기화   (추가 처리 가능)
```

---

## 🎨 디자인 특징

### 색상 체계
- **다중 주문 감지 Modal**: Amber (경고, 주의 필요)
- **취소 확인 Dialog**: Amber (중요한 결정)
- **입고 처리 확인 Dialog**: Red (되돌릴 수 없는 액션)
- **입고 처리 버튼**: Green (긍정적 액션)

### UX 개선
1. **명확한 단계 표시**: 각 Dialog의 목적이 명확함
2. **되돌릴 수 없는 액션 강조**: Red 색상 + ⚠️ 아이콘 + 주의사항 목록
3. **진행 상황 피드백**: Toast 알림으로 각 단계 완료 확인
4. **데이터 손실 방지**: 취소 시 2단계 확인
5. **모든 주문 처리 완료 시**: Inbound 페이지 유지 + 데이터 초기화 (새 명세서 업로드 가능)

---

## 🧪 테스트 시나리오

### 시나리오 1: 정상 플로우 (3개 주문 모두 처리)
1. 이미지 업로드 → OCR 분석
2. "다중 주문 감지" Modal → "확인" 클릭
3. Pending Orders List 표시
4. 첫 번째 주문 "추가" 클릭 → 확인 Dialog → "확인" 클릭
5. API 호출 → 성공 Toast → 리스트에서 삭제
6. 두 번째, 세 번째 주문 반복
7. 모든 주문 처리 완료 → "모든 주문 처리 완료" Toast → 데이터 초기화

### 시나리오 2: 일부만 처리 (나머지 보류)
1. 이미지 업로드 → OCR 분석
2. "다중 주문 감지" Modal → "확인" 클릭
3. 첫 번째 주문만 처리
4. 리스트에 2개 주문 남음 (나중에 처리 가능)

### 시나리오 3: 취소
1. 이미지 업로드 → OCR 분석
2. "다중 주문 감지" Modal → "취소" 클릭
3. "작업 취소 확인" Dialog → "확인 - 작업 취소" 클릭
4. 모든 데이터 초기화 → Inbound 페이지 초기 상태

### 시나리오 4: 단일 주문 (기존 플로우)
1. 이미지 업로드 → OCR 분석
2. `has_multiple_orders === false` → 기존 플로우 정상 작동

---

## 📊 API 연동 사양

### 예상 OCR 응답 (Backend 구현 필요)

```json
{
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
      "items": [ ... ],
      "subtotal": 430000
    },
    {
      "order_number": "20250822-9533C",
      "order_date": "2025-08-22",
      "items": [ ... ],
      "subtotal": 870000
    }
  ],
  "supplier": { ... },
  "document_info": { ... },
  "amounts": {
    "total_amount": 1794000
  }
}
```

### POST /api/v1/inbound/confirm 요청

```json
{
  "items": [
    {
      "bean_name": "브라질 산토스 NY2 FC (2)",
      "quantity": 40,
      "unit_price": 12350,
      "amount": 494000,
      "order_number": "20251108-8B7C2"
    }
  ],
  "document": {
    "contract_number": "20251108-8B7C2",
    "supplier_name": "공급처명",
    "invoice_date": "2025-11-08",
    "total_amount": 494000,
    "image_url": "...",
    "original_image_path": "...",
    "webview_image_path": "...",
    "thumbnail_image_path": "..."
  },
  "supplier": { ... },
  "document_info": { ... },
  "amounts": {
    "total_amount": 494000
  }
}
```

---

## 🔧 Backend 구현 체크리스트

### Agent 3 (Backend Engineer) 작업 필요

- [ ] **DB Migration**
  - [ ] `inbound_items.order_number` 컬럼 추가 (VARCHAR 100, nullable)
  - [ ] Index 생성: `idx_inbound_items_order_number`

- [ ] **OCR 프롬프트 수정**
  - [ ] `backend/app/resources/ocr_prompt_structure.json`에 `order_number` 필드 추가
  - [ ] STEP 5-1 지시사항 추가 (다중 주문번호 추출)

- [ ] **OCR Service 개선**
  - [ ] `_post_process_ocr_result()` 함수 구현
  - [ ] `analyze_image_stream()`에서 후처리 호출
  - [ ] 주문 날짜 자동 추출 로직 (YYYYMMDD 파싱)

- [ ] **API 응답 스키마**
  - [ ] `has_multiple_orders`, `total_order_count`, `order_groups` 필드 추가

---

## 📝 코드 품질

### TypeScript 컴파일
✅ **빌드 성공**: `npm run build` 통과

```
✓ Compiled successfully
✓ Generating static pages (24/24)
Route (app)                              Size     First Load JS
├ ƒ /inventory/inbound                   27.8 kB         229 kB
```

### Lint 통과
✅ **ESLint**: 오류 없음

### 타입 안전성
✅ **TypeScript**: 모든 State 및 Props 타입 정의 완료

---

## 🎯 다음 단계

### 우선순위 1: Backend 구현 (Agent 3)
1. DB Migration 실행
2. OCR 프롬프트 수정 및 후처리 로직 구현
3. 실제 다중 주문 명세서로 테스트

### 우선순위 2: E2E 테스트 (Agent 4)
1. Playwright 테스트 작성
2. Mock OCR 데이터로 Frontend 플로우 검증

### 우선순위 3: 문서화 (Agent 1)
1. 사용자 가이드 작성
2. API 문서 업데이트

---

## 📚 참조 문서

- **설계 문서**: `/mnt/d/Ai/WslProject/Themoon/docs/Planning/Multiple_Orders_Handling_Design.md`
- **구현 파일**: `/mnt/d/Ai/WslProject/Themoon/frontend/app/inventory/inbound/page.tsx`
- **관련 컴포넌트**: `DigitalReceipt.tsx`, `ui/alert-dialog.tsx`, `ui/card.tsx`, `ui/badge.tsx`

---

**작성자**: Agent 2 (Frontend Specialist)
**검토 필요**: Agent 3 (Backend Engineer) - Backend 구현
**승인 상태**: ✅ Frontend 구현 완료, Backend 구현 대기
