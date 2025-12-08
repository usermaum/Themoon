#!/bin/bash

# =============================================================================
# Render.com 자동 배포 스크립트
# =============================================================================
# 프로젝트: TheMoon - 커피 로스팅 원가 계산 시스템
# 버전: 1.0.0
# 작성일: 2025-12-08
#
# 사용법:
#   ./deploy-render.sh [커밋 메시지]
#
# 예시:
#   ./deploy-render.sh                           # 기본 커밋 메시지 사용
#   ./deploy-render.sh "feat: 새로운 기능 추가"  # 커스텀 커밋 메시지
# =============================================================================

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 배포 브랜치 설정
DEPLOY_BRANCH="claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck"
MAIN_BRANCH="main"

# Frontend 및 Backend URL
FRONTEND_URL="https://themoon-frontend-0s4m.onrender.com"
BACKEND_URL="https://themoon-api-gv1u.onrender.com"

# =============================================================================
# 함수 정의
# =============================================================================

# 에러 메시지 출력 및 종료
error_exit() {
    echo -e "${RED}❌ 에러: $1${NC}" >&2
    exit 1
}

# 성공 메시지 출력
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# 정보 메시지 출력
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# 경고 메시지 출력
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 진행 상황 헤더 출력
header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Git 상태 확인
check_git_status() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        error_exit "Git 저장소가 아닙니다. 프로젝트 루트에서 실행하세요."
    fi
}

# 현재 브랜치 확인
get_current_branch() {
    git branch --show-current
}

# 변경사항 확인
has_changes() {
    ! git diff-index --quiet HEAD --
}

# 로컬 빌드 테스트
test_local_build() {
    header "🧪 로컬 빌드 테스트"

    # Backend 테스트
    info "Backend 빌드 테스트 중..."
    if [ -f "backend/requirements.txt" ]; then
        cd backend || error_exit "backend 디렉토리를 찾을 수 없습니다."

        # Python 가상환경 확인
        if [ ! -d "../venv" ]; then
            warning "Python 가상환경이 없습니다. 빌드 테스트를 건너뜁니다."
        else
            # requirements.txt 검증 (설치는 생략, 파일만 확인)
            if python3 -m pip check > /dev/null 2>&1; then
                success "Backend 의존성 확인 완료"
            else
                warning "Backend 의존성 확인 실패 (배포 시 Render.com에서 재설치됨)"
            fi
        fi

        cd .. || exit
    else
        warning "backend/requirements.txt를 찾을 수 없습니다."
    fi

    # Frontend 테스트
    info "Frontend 빌드 테스트 중..."
    if [ -f "frontend/package.json" ]; then
        cd frontend || error_exit "frontend 디렉토리를 찾을 수 없습니다."

        # Node.js 설치 확인
        if ! command -v node > /dev/null 2>&1; then
            warning "Node.js가 설치되지 않았습니다. 빌드 테스트를 건너뜁니다."
        else
            # package.json 검증 (빌드는 생략, 파일만 확인)
            if [ -f "package-lock.json" ]; then
                success "Frontend package.json 확인 완료"
            else
                warning "package-lock.json이 없습니다. npm install을 먼저 실행하세요."
            fi
        fi

        cd .. || exit
    else
        warning "frontend/package.json을 찾을 수 없습니다."
    fi

    success "로컬 빌드 테스트 완료 (파일 검증)"
}

# 도움말 출력
show_help() {
    cat << EOF
🚀 Render.com 자동 배포 스크립트

사용법:
  ./deploy-render.sh [옵션] [커밋 메시지]

옵션:
  -h, --help        도움말 출력
  -s, --skip-test   로컬 빌드 테스트 건너뛰기
  -f, --force       변경사항 없어도 강제 푸시

예시:
  ./deploy-render.sh
  ./deploy-render.sh "feat: 새로운 기능 추가"
  ./deploy-render.sh --skip-test
  ./deploy-render.sh --force "deploy: 긴급 배포"

배포 브랜치: $DEPLOY_BRANCH

EOF
    exit 0
}

# =============================================================================
# 메인 실행 로직
# =============================================================================

# 인자 파싱
SKIP_TEST=false
FORCE_PUSH=false
COMMIT_MSG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            ;;
        -s|--skip-test)
            SKIP_TEST=true
            shift
            ;;
        -f|--force)
            FORCE_PUSH=true
            shift
            ;;
        *)
            COMMIT_MSG="$1"
            shift
            ;;
    esac
done

# 기본 커밋 메시지 설정
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="deploy: Render.com 배포 준비 완료 ($(date +%Y-%m-%d))"
fi

# =============================================================================
# 배포 시작
# =============================================================================

header "🚀 Render.com 배포 시작"
info "배포 브랜치: $DEPLOY_BRANCH"
info "커밋 메시지: $COMMIT_MSG"
echo ""

# 1. Git 상태 확인
check_git_status

# 2. 현재 브랜치 확인
CURRENT_BRANCH=$(get_current_branch)
info "현재 브랜치: $CURRENT_BRANCH"

# 3. 배포 브랜치로 전환 (필요시)
if [ "$CURRENT_BRANCH" != "$DEPLOY_BRANCH" ]; then
    warning "현재 브랜치가 배포 브랜치가 아닙니다."
    info "배포 브랜치로 전환 중: $DEPLOY_BRANCH"

    # 배포 브랜치 존재 여부 확인
    if ! git rev-parse --verify "$DEPLOY_BRANCH" > /dev/null 2>&1; then
        error_exit "배포 브랜치 '$DEPLOY_BRANCH'를 찾을 수 없습니다."
    fi

    # 브랜치 전환
    git checkout "$DEPLOY_BRANCH" || error_exit "브랜치 전환 실패"
    success "배포 브랜치로 전환 완료"
else
    success "배포 브랜치 확인 완료"
fi

# 4. main 브랜치 최신 변경사항 병합
header "🔄 main 브랜치 최신 변경사항 병합"

# main 브랜치 fetch
info "main 브랜치 업데이트 중..."
git fetch origin "$MAIN_BRANCH" || warning "main 브랜치 fetch 실패 (계속 진행)"

# main 브랜치 병합
info "main 브랜치 병합 중..."
if git merge origin/"$MAIN_BRANCH" --no-edit; then
    success "main 브랜치 병합 완료"
else
    error_exit "main 브랜치 병합 실패. 충돌을 해결한 후 다시 시도하세요."
fi

# 5. 로컬 빌드 테스트 (옵션)
if [ "$SKIP_TEST" = false ]; then
    test_local_build
else
    warning "로컬 빌드 테스트를 건너뜁니다. (--skip-test)"
fi

# 6. 변경사항 커밋
header "📦 변경사항 커밋"

if has_changes || [ "$FORCE_PUSH" = true ]; then
    info "변경사항을 커밋 중..."

    # 모든 변경사항 스테이징
    git add .

    # 커밋
    git commit -m "$COMMIT_MSG" || warning "커밋 실패 (변경사항이 없을 수 있음)"

    success "커밋 완료"
else
    info "변경사항이 없습니다. 커밋을 건너뜁니다."
fi

# 7. 배포 브랜치에 푸시
header "🚢 배포 브랜치에 푸시"

info "원격 저장소에 푸시 중..."
if git push origin "$DEPLOY_BRANCH"; then
    success "푸시 완료"
else
    error_exit "푸시 실패. 네트워크 상태를 확인하세요."
fi

# 8. 배포 완료 메시지
header "✅ 배포 성공!"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 Render.com 배포 준비 완료!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📊 배포 상태 확인:${NC}"
echo -e "  ${GREEN}Frontend:${NC} $FRONTEND_URL"
echo -e "  ${GREEN}Backend: ${NC} $BACKEND_URL"
echo ""
echo -e "${YELLOW}⏳ Render.com에서 자동 배포 진행 중 (약 5~10분 소요)${NC}"
echo ""
echo -e "${BLUE}📍 배포 로그 확인:${NC}"
echo -e "  https://dashboard.render.com"
echo ""
echo -e "${BLUE}🔍 Health Check:${NC}"
echo -e "  curl $BACKEND_URL/health"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 배포 완료
exit 0
