# Feature-Sliced Design (FSD) 적용 타당성 분석 보고서

> **문서 목적**: 'Themoon' 프로젝트에 FSD 아키텍처 도입 시 장단점을 분석하고, 현재 프로젝트 상황에 맞는 최적의 아키텍처 방향을 제언함.

---

## 1. Feature-Sliced Design (FSD) 요약

FSD는 프론트엔드 애플리케이션을 기능(Feature)과 비즈니스 가치에 따라 계층적으로 분리하는 아키텍처 방법론입니다.

### 핵심 계층 (Layers)
1.  **App**: 전역 설정 (Provider, Router, CSS)
2.  **Processes**: 복잡한 다단계 프로세스 (예: 회원가입, 결제) - *최근에는 선택적*
3.  **Pages**: 라우팅 페이지 (Next.js의 `app/` 또는 `pages/`)
4.  **Widgets**: 독립적인 기능을 수행하는 큰 UI 블록 (예: Header, RoastingDashboard)
5.  **Features**: 사용자 상호작용이 포함된 기능 단위 (예: AddBeanToCart, FilterRoastingLogs)
6.  **Entities**: 비즈니스 도메인 데이터와 UI (예: Bean, RoastLog)
7.  **Shared**: 재사용 가능한 로직, UI 컴포넌트, 유틸리티 (특정 도메인 종속 없음)

---

## 2. 'Themoon' 프로젝트 현황 분석

*   **현재 구조**: Next.js App Router 기반 + Feature-based Component 구조 (`frontend/components/roasting` 등)
*   **팀 규모**: 1인 개발자 (AI Assistant 활용)
*   **복잡도**: 중간 (Middle). 도메인(로스팅, 재고, 블렌딩)이 명확하지만, 엔터프라이즈급 대규모 서비스는 아님.
*   **기술 스택**: Next.js 14 (App Router), Shadcn UI, Tailwind CSS

---

## 3. FSD 적용 시 장단점 (Pros & Cons)

### 👍 장점 (Pros)
1.  **명확한 경계**: '로스팅'과 '재고' 기능이 엄격히 분리되어, 한쪽을 수정해도 다른 쪽에 영향을 줄 가능성이 줄어듭니다.
2.  **순환 참조 방지**: 엄격한 단방향 의존성 규칙(Layer Rule)으로 스파게티 코드를 방지합니다.
3.  **확장성**: 프로젝트가 10배 이상 커지고 개발자가 10명 이상으로 늘어날 때 강력한 위력을 발휘합니다.
4.  **유지보수 가이드**: "이 컴포넌트를 어디에 둬야 하지?"에 대한 명확한 답을 줍니다.

### 👎 단점 (Cons) - 솔직한 의견
1.  **과도한 복잡성 (Over-engineering)**:
    *   현재 프로젝트 규모에 비해 폴더 깊이가 너무 깊어집니다.
    *   간단한 버튼 하나를 수정하려 해도 `src/shared/ui/button` -> `src/features/roasting/...` -> `src/widgets/...` 을 오가야 합니다.
2.  **Next.js App Router와의 충돌**:
    *   Next.js App Router는 이미 `app/` 디렉토리를 통해 **File-system based Routing**을 강제합니다.
    *   FSD를 적용하려면 `app/` 폴더를 껍데기로 만들고 실질적인 페이지 로직을 `src/pages/` 등으로 빼내야 하는데, 이는 Next.js의 의도와 약간 엇박자가 납니다.
3.  **보일러플레이트 증가**:
    *   각 Slice마다 `index.ts` (Public API)를 만들어야 하고, 폴더 구조를 잡는 데 많은 시간이 소요됩니다.
4.  **AI 협업 효율 저하**:
    *   AI는 컨텍스트 윈도우 한계가 있습니다. 파일 경로가 길어지고 파일이 잘게 쪼개질수록 AI가 전체 맥락을 파악하고 수정하는 데 비용이 더 듭니다. 현재 구조(`components/roasting/RoastingHistory.tsx`)가 AI에게는 훨씬 직관적입니다.

---

## 4. 솔직한 제언 (Recommendation)

### 🚫 "FSD 전체 도입은 비추천합니다."
현재 단계에서 엄격한 FSD(Strict FSD)를 도입하는 것은 **"닭 잡는 데 소 잡는 칼을 쓰는 격"**입니다. 득보다 실(개발 피로도, 복잡성)이 더 큽니다.

### ✅ "대안: Pragmatic Feature-based Design (실용적 기능 중심 설계)"
현재 사용 중인 구조를 조금 더 다듬는 방향을 추천합니다. 이는 FSD의 철학(기능별 응집)은 가져오되, 복잡한 계층 구조는 버리는 방식입니다.

**구조 비교 (Current vs Recommended)**:

| 구분          | 현재 (Themoon Project)     | 추천 (Pragmatic Feature-based) | 상태   |
| :------------ | :------------------------- | :----------------------------- | :----- |
| **Page**      | `app/roasting/page.tsx`    | `app/roasting/page.tsx`        | ✅ 일치 |
| **Shared UI** | `components/ui/*` (Shadcn) | `components/ui/*`              | ✅ 일치 |
| **Domain UI** | `components/roasting/*`    | `components/roasting/*`        | ✅ 일치 |
| **Api**       | `lib/api.ts`               | `lib/api.ts`                   | ✅ 일치 |

**상세 디렉토리 구조 비교**:

```text
frontend/
├── app/                  # ✅ App Router 유지
│   ├── roasting/
│   └── inventory/
├── components/           # ✅ 기능별 폴더링 (FSD의 철학만 계승)
│   ├── ui/               # Widget/Shared (Shadcn UI)
│   ├── layouts/          # Widget (Navbar, Sidebar)
│   ├── roasting/         # 🔥 Feature: 로스팅 관련 모든 컴포넌트
│   │   ├── RoastingForm.tsx
│   │   ├── RoastingList.tsx
│   │   └── hooks/
│   ├── inventory/        # 📦 Feature: 재고 관련
│   └── dashboard/        # 📊 Feature: 대시보드 관련
├── lib/
│   └── api.ts            # Shared Logic
└── store/                # Shared State
```

**이유**:
1.  **이미 잘하고 계십니다**: 현재 `components/roasting`, `components/inventory`로 나누신 것이 바로 이 방향입니다.
2.  **직관성**: "로스팅 고쳐야지" -> `components/roasting`으로 가면 끝입니다.
3.  **Next.js 친화적**: App Router 구조와 자연스럽게 어우러집니다.

### 결론
FSD는 훌륭한 아키텍처지만, **현재 프로젝트 규모와 팀 구성(1인+AI)에서는 생산성을 저하시킬 위험**이 큽니다. 현재의 **기능별 폴더 구조(Feature Folders)**를 유지하면서, 컴포넌트가 너무 커지면 그때 분리하는 리팩토링 전략을 유지하세요.
