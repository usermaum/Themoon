# 📚 TheMoon 프로젝트 문서 인덱스

> **마지막 업데이트**: 2025-12-08
> **프로젝트 버전**: 0.0.6

이 폴더는 TheMoon 프로젝트의 모든 기술 문서를 체계적으로 관리합니다.

---

## 📁 폴더 구조

```
docs/
├── Architecture/     # 시스템 아키텍처 및 설계 문서
├── Guides/           # 개발/배포/사용 가이드
├── Planning/         # 기획 및 계획 문서
├── Progress/         # 세션 진행 상황 및 체크리스트
├── Reports/          # 분석 및 테스트 보고서
└── Resources/        # 참고 자료 및 리소스
```

---

## 📐 Architecture (아키텍처)

시스템 설계, 컴포넌트 구조, 파일 구조 등 기술적 아키텍처 문서

| 파일명                                                                | 설명                                                     |
| --------------------------------------------------------------------- | -------------------------------------------------------- |
| **시스템 설계**                                                       |                                                          |
| [SYSTEM_OVERVIEW.md](Architecture/SYSTEM_OVERVIEW.md)                 | 시스템 전체 개요 및 핵심 기능 정의 ✅                     |
| [SYSTEM_ARCHITECTURE.md](Architecture/SYSTEM_ARCHITECTURE.md)         | 전체 시스템 아키텍처 (Frontend/Backend/DB)               |
| [DATA_FLOW.md](Architecture/DATA_FLOW.md)                             | 데이터 흐름도 및 프로세스 간 상호작용 ✅                  |
| [DATABASE_SCHEMA.md](Architecture/DATABASE_SCHEMA.md)                 | PostgreSQL 데이터베이스 스키마 (ERD, 테이블 정의) ✅      |
| **API & 기술 스택**                                                   |                                                          |
| [API_SPECIFICATION.md](Architecture/API_SPECIFICATION.md)             | RESTful API 엔드포인트 명세 (요청/응답/에러 코드) ✅ NEW! |
| [TECHNOLOGY_STACK.md](Architecture/TECHNOLOGY_STACK.md)               | 기술 스택 선정 이유 및 버전 정보 ✅ NEW!                  |
| [DEPLOYMENT_ARCHITECTURE.md](Architecture/DEPLOYMENT_ARCHITECTURE.md) | Render.com 배포 구조, CI/CD 파이프라인 ✅ NEW!            |
| **개발 가이드**                                                       |                                                          |
| [FILE_STRUCTURE.md](Architecture/FILE_STRUCTURE.md)                   | 프로젝트 파일/폴더 구조 설명                             |
| [COMPONENT_DESIGN.md](Architecture/COMPONENT_DESIGN.md)               | UI 컴포넌트 설계 문서                                    |
| [COMPONENT_USAGE_GUIDE.md](Architecture/COMPONENT_USAGE_GUIDE.md)     | 컴포넌트 사용 가이드                                     |
| [DEVELOPMENT_GUIDE.md](Architecture/DEVELOPMENT_GUIDE.md)             | 개발 환경 및 규칙 가이드                                 |
| [PROJECT_SETUP_GUIDE.md](Architecture/PROJECT_SETUP_GUIDE.md)         | 프로젝트 초기 설정 가이드                                |
| [COMMON_TASKS.md](Architecture/COMMON_TASKS.md)                       | 자주 사용하는 개발 작업                                  |
| [TROUBLESHOOTING.md](Architecture/TROUBLESHOOTING.md)                 | 문제 해결 가이드                                         |

---

## 📖 Guides (가이드)

개발, 배포, API 사용 등 실용적인 가이드 문서

| 파일명                                                                    | 설명                             |
| ------------------------------------------------------------------------- | -------------------------------- |
| [PROGRAMMING_RULES.md](Guides/PROGRAMMING_RULES.md)                       | 프로젝트 코딩 규칙 및 컨벤션     |
| [DEPLOYMENT.md](Guides/DEPLOYMENT.md)                                     | Railway + Cloudflare 배포 가이드 |
| [DEPLOYMENT_FREE.md](Guides/DEPLOYMENT_FREE.md)                           | 무료 배포 옵션 가이드            |
| [GEMINI_OCR_GUIDE.md](Guides/GEMINI_OCR_GUIDE.md)                         | Google Gemini OCR 통합 가이드    |
| [CLAUDE_API_INTEGRATION_GUIDE.md](Guides/CLAUDE_API_INTEGRATION_GUIDE.md) | Claude API 통합 가이드           |

---

## 📋 Planning (기획)

기능 기획, 마이그레이션 계획, 이미지 프롬프트 등 계획 문서

| 파일명                                                                                  | 설명                                  |
| --------------------------------------------------------------------------------------- | ------------------------------------- |
| **마스터 문서**                                                                         |                                       |
| [Themoon_Rostings_v2.md](Planning/Themoon_Rostings_v2.md)                               | 로스팅 및 재고 관리 운영 계획안 v2.0  |
| [Themoon_Inbound_History.md](Planning/Themoon_Inbound_History.md)                       | 상세 입고 이력                        |
| [Themoon_System_Implementation_Plan.md](Planning/Themoon_System_Implementation_Plan.md) | 시스템 구현 계획                      |
| **이미지 프롬프트**                                                                     |                                       |
| [Bean_Image_Prompts.md](Planning/Bean_Image_Prompts.md)                                 | 원두 이미지 프롬프트 V1 (생두)        |
| [Bean_Image_Prompts_V2.md](Planning/Bean_Image_Prompts_V2.md)                           | 원두 이미지 프롬프트 V2               |
| [Bean_Image_Prompts_V3.md](Planning/Bean_Image_Prompts_V3.md)                           | 원두 이미지 프롬프트 V3 (로스팅 원두) |
| **기능 계획**                                                                           |                                       |
| [Single_Origin_Roasting_Refactor.md](Planning/Single_Origin_Roasting_Refactor.md)       | 싱글 오리진 로스팅 리팩토링 계획      |
| [Blending_Loss_logic_Plan.md](Planning/Blending_Loss_logic_Plan.md)                     | 블렌딩 손실률 로직 계획               |
| [COST_CALCULATOR_ENHANCEMENT_PLAN.md](Planning/COST_CALCULATOR_ENHANCEMENT_PLAN.md)     | 원가 계산기 개선 계획                 |
| **마이그레이션**                                                                        |                                       |
| [MIGRATION_TO_MODERN_STACK.md](Planning/MIGRATION_TO_MODERN_STACK.md)                   | 모던 스택 마이그레이션 계획           |
| [CLEAN_SLATE_STRATEGY.md](Planning/CLEAN_SLATE_STRATEGY.md)                             | 클린 슬레이트 전략                    |
| **기타**                                                                                |                                       |
| [Theme_Concepts_v2.md](Planning/Theme_Concepts_v2.md)                                   | UI 테마 컨셉                          |
| [GSC 커피 리스트.md](Planning/GSC%20커피%20리스트.md)                                   | GSC 커피 원두 목록                    |
| [로스팅_플랜_2025.md](Planning/로스팅_플랜_2025.md)                                     | 2025년 로스팅 계획                    |
| [성능최적화_가이드.md](Planning/성능최적화_가이드.md)                                   | 성능 최적화 방법                      |
| [통합_웹사이트_구현_마스터플랜_v2.md](Planning/통합_웹사이트_구현_마스터플랜_v2.md)     | 웹사이트 통합 마스터플랜              |
| [실행계획_v0.9.1_to_v1.0.0.md](Planning/실행계획_v0.9.1_to_v1.0.0.md)                   | 버전 업그레이드 계획                  |

---

## 📊 Progress (진행 상황)

세션별 작업 요약 및 체크리스트

| 파일명                                                            | 설명                  |
| ----------------------------------------------------------------- | --------------------- |
| [SESSION_START_CHECKLIST.md](Progress/SESSION_START_CHECKLIST.md) | 세션 시작 체크리스트  |
| [SESSION_END_CHECKLIST.md](Progress/SESSION_END_CHECKLIST.md)     | 세션 종료 체크리스트  |
| `SESSION_SUMMARY_YYYY-MM-DD.md`                                   | 날짜별 세션 작업 요약 |

### 최근 세션 요약

- [SESSION_SUMMARY_2025-12-08.md](Progress/SESSION_SUMMARY_2025-12-08.md) - 최신
- [SESSION_SUMMARY_2025-12-07.md](Progress/SESSION_SUMMARY_2025-12-07.md)
- [SESSION_SUMMARY_2025-12-06.md](Progress/SESSION_SUMMARY_2025-12-06.md)
- [SESSION_SUMMARY_2025-12-05.md](Progress/SESSION_SUMMARY_2025-12-05.md)
- [SESSION_SUMMARY_2025-11-30.md](Progress/SESSION_SUMMARY_2025-11-30.md)
- ... (이전 세션들)

---

## 📈 Reports (보고서)

분석, 테스트, 구현 결과 보고서

| 파일명                                                                           | 설명                             |
| -------------------------------------------------------------------------------- | -------------------------------- |
| [TEST_REPORT.md](Reports/TEST_REPORT.md)                                         | 로스팅 원가 계산기 테스트 보고서 |
| [ANIMATION_IMPLEMENTATION_REPORT.md](Reports/ANIMATION_IMPLEMENTATION_REPORT.md) | 애니메이션 구현 보고서           |

---

## 📦 Resources (리소스)

참고 자료, 대화 기록, 원두 정보 등 보조 자료

| 파일명                                                       | 설명                  |
| ------------------------------------------------------------ | --------------------- |
| [원두_종류별_설명.md](Resources/원두_종류별_설명.md)         | 원두 품종별 상세 설명 |
| [프롬프트 정리 노트.md](Resources/프롬프트%20정리%20노트.md) | AI 프롬프트 작성 노트 |
| [마지막 대화.md](Resources/마지막%20대화.md)                 | 참고용 대화 기록      |
| [마지막 대화_2.md](Resources/마지막%20대화_2.md)             | 참고용 대화 기록 2    |

### PDF 리소스 (docs 루트)

- `[지에스씨] 생두 단가표.pdf` - GSC 생두 가격표
- `[지에스씨]플레이버맵ver3_다운로드.pdf` - GSC 플레이버 맵

---

## 🔍 문서 검색 가이드

### 카테고리별 빠른 찾기

| 찾고 싶은 내용         | 참조할 폴더/문서                                                                          |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| **시스템 이해**        |                                                                                           |
| 시스템 전체 개요       | [Architecture/SYSTEM_OVERVIEW.md](Architecture/SYSTEM_OVERVIEW.md)                        |
| 데이터 흐름            | [Architecture/DATA_FLOW.md](Architecture/DATA_FLOW.md)                                    |
| 데이터베이스 스키마    | [Architecture/DATABASE_SCHEMA.md](Architecture/DATABASE_SCHEMA.md)                        |
| **API & 배포**         |                                                                                           |
| API 사용법             | [Architecture/API_SPECIFICATION.md](Architecture/API_SPECIFICATION.md) ✅ NEW!             |
| 기술 스택 정보         | [Architecture/TECHNOLOGY_STACK.md](Architecture/TECHNOLOGY_STACK.md) ✅ NEW!               |
| 배포 방법 (Render.com) | [Architecture/DEPLOYMENT_ARCHITECTURE.md](Architecture/DEPLOYMENT_ARCHITECTURE.md) ✅ NEW! |
| 배포 방법 (기타)       | [Guides/DEPLOYMENT.md](Guides/DEPLOYMENT.md)                                              |
| **개발**               |                                                                                           |
| 프로젝트 구조          | [Architecture/FILE_STRUCTURE.md](Architecture/FILE_STRUCTURE.md)                          |
| 코딩 규칙              | [Guides/PROGRAMMING_RULES.md](Guides/PROGRAMMING_RULES.md)                                |
| 개발 가이드            | [Architecture/DEVELOPMENT_GUIDE.md](Architecture/DEVELOPMENT_GUIDE.md)                    |
| **데이터 & 리소스**    |                                                                                           |
| 원두 마스터 데이터     | [Planning/Themoon_Rostings_v2.md](Planning/Themoon_Rostings_v2.md)                        |
| 이미지 생성            | [Planning/Bean_Image_Prompts_V3.md](Planning/Bean_Image_Prompts_V3.md)                    |
| **진행 상황**          |                                                                                           |
| 오늘 작업 내용         | [Progress/SESSION_SUMMARY_2025-12-08.md](Progress/SESSION_SUMMARY_2025-12-08.md)          |
| 테스트 결과            | [Reports/TEST_REPORT.md](Reports/TEST_REPORT.md)                                          |

---

## ✍️ 문서 작성 규칙

1. **파일명**: 영문 대문자 + 언더스코어 (`EXAMPLE_DOCUMENT.md`)
2. **한글 파일명**: 기획/리소스 문서에 한해 허용
3. **날짜 포함 파일**: `YYYY-MM-DD` 형식 사용
4. **버전 포함 파일**: `_v2`, `_V3` 등 suffix 사용

---

## 🔗 관련 문서

**← 상위**: [프로젝트 루트](../README.md)

**README 모음**:
- [Backend README](../backend/README.md) - Backend 개발 가이드
- [Frontend README](../frontend/README.md) - Frontend 개발 가이드

**핵심 아키텍처 문서** (빠른 접근):
- [시스템 개요](Architecture/SYSTEM_OVERVIEW.md) - 전체 시스템 개요 및 핵심 기능
- [데이터 흐름도](Architecture/DATA_FLOW.md) - 시스템 내 데이터 흐름 상세 분석
- [데이터베이스 스키마](Architecture/DATABASE_SCHEMA.md) - 테이블 구조 및 관계도
- [API 명세](Architecture/API_SPECIFICATION.md) ⭐ - 모든 API 엔드포인트 상세 문서
- [기술 스택](Architecture/TECHNOLOGY_STACK.md) ⭐ - 사용 기술 상세 설명
- [배포 아키텍처](Architecture/DEPLOYMENT_ARCHITECTURE.md) ⭐ - 배포 환경 상세 구조

---

**문서 관리자**: AI Assistant
**마지막 정리**: 2025-12-08
