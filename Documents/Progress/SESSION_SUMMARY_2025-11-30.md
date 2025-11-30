# 세션 요약 - 2025-11-30

## 📋 세션 정보
- **날짜**: 2025-11-30
- **작업 시간**: 약 3시간
- **주요 작업**: 사이드바 툴팁 기능 구현 및 표시 문제 해결

## ✅ 완료된 작업

### 1. .gitignore 수정 - logs/ 폴더 표시 문제 해결
- **문제**: logs/ 폴더가 탐색기에서 보이지 않음
- **원인**: .gitignore에서 logs/ 전체 폴더 제외
- **해결**: logs/ → logs/*.log로 변경 (로그 파일만 제외)
- **커밋**: `cdbc189`

### 2. 사이드바 토글 버튼 툴팁 추가
- **기능**: 사이드바 펼치기/접기 버튼에 툴팁 추가
- **구현**:
  - 펼쳐진 상태: "사이드바 접기" (버튼 아래 표시)
  - 접힌 상태: "사이드바 펼치기" (버튼 오른쪽 표시)
  - CSS group-hover를 이용한 애니메이션
- **커밋**: `430da9d`

### 3. 메뉴 아이템 툴팁 스타일 통일
- **작업**: Home, Beans, Blends, Inventory, Settings 버튼에 툴팁 적용
- **변경**: HTML title 속성 → CSS 기반 커스텀 툴팁
- **개선**: 토글 버튼과 동일한 디자인 및 애니메이션
- **커밋**: `eb707a9`

### 4. 툴팁 표시 문제 해결 (9개 커밋)

#### 4.1 초기 시도: 조건 및 z-index 조정
- 펼쳐진 상태에서도 툴팁 표시 시도 → 되돌림
- z-index를 z-50 → z-[9999]로 상향
- **커밋**: `f8e0d3a`, `6a52914`

#### 4.2 z-index 계층 구조 재설계
- Sidebar: z-50 → z-[100]
- Backdrop: z-40 → z-[90]
- Tooltips: z-[9999] → z-[200]
- **커밋**: `9b9a7bf`

#### 4.3 PageHero 컴포넌트 z-index 조정
- PageHero가 Sidebar보다 높아서 툴팁 가림
- PageHero 컨테이너: z-0 명시
- 배경 이미지: -z-10으로 변경
- **커밋**: `d4884c8`

#### 4.4 메뉴 아이템 구조 개선
- **문제**: li에 group 클래스, Link가 hover 영역 차지
- **해결**: li 내부에 div.relative.group 추가
- 토글 버튼과 동일한 구조로 변경
- **커밋**: `d307b68`

#### 4.5 overflow 및 z-index 개선
- ul, User Profile Area에 overflow: visible 추가
- main 요소에 z-0 설정 (Sidebar보다 낮게)
- **커밋**: `bfdbc19`

#### 4.6 nav 태그 overflow 버그 수정 ⭐
- **문제**: overflowY: auto와 overflowX: visible 동시 사용 불가
- **원인**: CSS 스펙상 visible이 자동으로 auto로 변경됨
- **해결**: nav에 overflow-visible, 내부 div에 overflow-y-auto
- **커밋**: `ed20e1c`

#### 4.7 nav 태그를 div로 교체
- nav + 내부 div 2중 구조 → 단일 div 구조로 단순화
- 의미론적 HTML보다 실용성 우선
- **커밋**: `a75dfd3`

#### 4.8 ul/li 태그를 div로 교체
- ul/li가 overflow 처리 방해
- 완전히 div로 교체하여 구조 단순화
- **커밋**: `c5918ee`

#### 4.9 overflow-y-auto 완전 제거 (최종 해결) ⭐⭐⭐
- **분석**: 메뉴 4개만 있어 스크롤 불필요
- **해결**: overflow-y-auto 완전 제거
- **결과**: 모든 overflow 제약 제거, 툴팁 완벽 표시
- **커밋**: `891a741`

## 📊 통계

### 커밋 통계
- **총 커밋 수**: 13개
- **기능 추가**: 2개 (feat)
- **버그 수정**: 10개 (fix)
- **리팩토링**: 1개 (refactor)

### 파일 변경
- **수정된 파일**: 5개
  - `.gitignore`
  - `frontend/components/layout/Sidebar.tsx`
  - `frontend/components/layout/AppLayout.tsx`
  - `frontend/components/ui/PageHero.tsx`

## 🎯 주요 성과

### 1. 사이드바 툴팁 시스템 완성
- 모든 메뉴 아이템에 일관된 툴팁 적용
- 토글 버튼, 네비게이션, Settings 모두 동일한 스타일
- 다크모드 완벽 대응

### 2. 복잡한 overflow 문제 해결
- 9번의 시도 끝에 근본 원인 파악
- overflow-y-auto가 툴팁을 가리는 핵심 문제
- 불필요한 스크롤 기능 제거로 간결한 구조 확립

### 3. z-index 계층 구조 정립
```
main 콘텐츠:          z-0     (가장 낮음)
PageHero:             z-0
Backdrop (모바일):    z-[90]
Sidebar:              z-[100]
Tooltips:             z-[200] (가장 높음)
```

### 4. 코드 구조 단순화
- nav/ul/li 태그 → div 태그로 완전 교체
- 3중 구조 → 2중 구조로 단순화
- 의미론적 HTML보다 실용성 우선 결정

## 🔍 학습한 내용

### CSS overflow의 함정
1. `overflowY: auto`와 `overflowX: visible`을 동시에 사용할 수 없음
2. 한 축이 auto/scroll이면 다른 축의 visible은 자동으로 auto로 변경
3. absolute 포지션 툴팁은 부모의 overflow에 영향받음

### z-index 관리
1. 전체 애플리케이션의 z-index 계층 구조가 중요
2. Sidebar, main, tooltip 각각의 레벨을 명확히 정의
3. 컴포넌트 간 z-index 충돌 주의

### HTML 구조 선택
1. 의미론적 HTML이 항상 정답은 아님
2. 실용성과 기능성을 우선할 때도 있음
3. nav/ul/li보다 div가 더 나은 경우 존재

## 🐛 알려진 이슈

### Next.js 개발 모드 경고
- `Extra attributes from the server: data-jetski-tab-id`
- 브라우저 확장 프로그램(Jetski)이 HTML에 속성 추가
- 실제 기능에는 영향 없음 (무시 가능)

## 📝 미완료 작업

### 추가되었으나 커밋되지 않은 파일
- `.coffee_bean_receiving_Specification/`
- `Documents/Planning/Themoon_System_Implementation_Plan.md`
- `clean_cache.sh`
- `frontend/components/layout/ClientLayout.tsx`
- `frontend/public/inventory_hero_bg.png`
- `frontend/public/inventory_hero_bg2.png`
- `images/` (스크린샷)
- `kill_servers.sh`

## 💡 다음 세션 제안

### 1. 미커밋 파일 정리
- 불필요한 파일 삭제
- 필요한 파일 커밋

### 2. 사이드바 기능 개선
- User Profile 클릭 시 프로필 메뉴 표시
- Settings 페이지 구현
- 모바일 반응형 개선

### 3. 페이지 개발 진행
- Beans 페이지 완성
- Blends 페이지 완성
- Inventory 페이지 개선

## 🎓 배운 교훈

1. **문제 해결 과정**
   - 표면적 증상보다 근본 원인 파악이 중요
   - 9번의 시도 끝에 overflow-y-auto가 진짜 원인임을 발견
   - 단계적 접근보다 때로는 근본적 제거가 답

2. **CSS 디버깅**
   - 브라우저 개발자 도구의 Computed 탭 활용
   - overflow 속성의 상호작용 이해 필요
   - z-index는 전체 구조를 고려해야 함

3. **실용주의**
   - 의미론적 HTML도 중요하지만 기능이 우선
   - 과도한 구조보다 단순함이 더 나을 수 있음
   - 불필요한 기능(스크롤)은 과감히 제거

## 📌 참고 링크
- [CSS overflow 스펙](https://www.w3.org/TR/css-overflow-3/)
- [z-index 관리 가이드](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Understanding_z-index)

---

**세션 종료 시각**: 2025-11-30 23:00 (예상)
**다음 세션**: 2025-12-01
