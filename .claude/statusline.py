#!/usr/bin/env python3
"""
Claude Code 상태바 스크립트
컬러풀한 이모지와 실시간 정보를 표시하는 상태바
60초마다 자동 새로고침
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

# 같은 디렉토리의 claude_usage_api 모듈 import
sys.path.insert(0, str(Path(__file__).parent))
try:
    from claude_usage_api import get_claude_usage_api
except ImportError:
    get_claude_usage_api = None


def get_git_branch():
    """현재 Git 브랜치 이름 가져오기"""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
            cwd=Path(__file__).parent.parent
        )
        return result.stdout.strip()
    except Exception:
        return "no-branch"


def get_claude_info():
    """Claude 모델 및 세션 정보 가져오기"""
    try:
        # ccusage 명령어로 상태 정보 가져오기
        result = subprocess.run(
            ["npx", "-y", "ccusage@latest", "statusline", "--cache", "--no-offline"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=Path(__file__).parent.parent
        )

        # 기본 정보
        model_name = "Sonnet 4.5"
        context_usage = "N/A"
        session_id = "unknown"

        # ccusage 출력에서 정보 파싱
        output = result.stdout
        if "%" in output:
            # 퍼센트 표시 찾기
            for part in output.split():
                if "%" in part:
                    context_usage = part.strip().replace("%", "") + "%"
                    break

        # 세션 ID는 환경변수나 프로세스 ID로 대체
        session_id = os.environ.get("CLAUDE_SESSION_ID", str(os.getpid())[:8])

        return {
            "model": model_name,
            "context": context_usage,
            "session_id": session_id
        }
    except Exception as e:
        return {
            "model": "Sonnet 4.5",
            "context": "N/A",
            "session_id": "unknown"
        }


def get_app_version():
    """앱 버전 가져오기"""
    try:
        version_file = Path(__file__).parent.parent / "logs" / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        return "0.2.0"
    except Exception:
        return "0.2.0"


def get_claude_usage():
    """Claude Pro 사용량 정보"""
    if get_claude_usage_api is None:
        return {
            "daily_limit": 100,
            "used": "N/A",
            "remaining": "N/A",
            "percentage": 0
        }

    try:
        api = get_claude_usage_api()
        return api.get_usage()
    except Exception:
        return {
            "daily_limit": 100,
            "used": "N/A",
            "remaining": "N/A",
            "percentage": 0
        }


def format_statusline(compact=True):
    """상태바 한 줄로 포맷팅"""
    # 현재 시간/날짜
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    weekday = now.strftime("%a")

    # Git 브랜치
    branch = get_git_branch()

    # Claude 정보
    claude_info = get_claude_info()

    # 앱 버전
    version = get_app_version()

    # Claude 사용량
    usage = get_claude_usage()

    # 사용량 색상 표시 (이모지로 경고 수준 표시)
    percentage = usage.get('percentage', 0)
    if percentage >= 90:
        usage_icon = "🔴"  # 90% 이상: 위험
    elif percentage >= 70:
        usage_icon = "🟡"  # 70-89%: 경고
    else:
        usage_icon = "💎"  # 70% 미만: 정상

    if compact:
        # 컴팩트 버전 (한 줄)
        statusline_parts = [
            f"📅 {date_str}({weekday})",
            f"🕐 {time_str}",
            f"🌿 {branch}",
            f"🤖 {claude_info['model']}",
            f"📊 {claude_info['context']}",
            f"📦 v{version}",
            f"{usage_icon} {usage['used']}/{usage['daily_limit']} ({usage['percentage']}%)",
            f"⏰ {usage.get('time_remaining', 'N/A')}"
        ]
        return " • ".join(statusline_parts)
    else:
        # 상세 버전 (여러 줄)
        return f"""
╔══════════════════════════════════════════════════════════════
║ 🕐 시간: {time_str}  📅 날짜: {date_str} ({weekday})
║ 🌿 브랜치: {branch}
║ 🤖 모델: {claude_info['model']}  📊 컨텍스트: {claude_info['context']}
║ 🆔 세션: {claude_info['session_id']}  📦 버전: v{version}
║ {usage_icon} 플랜 사용량: {usage['used']}/{usage['daily_limit']} ({usage['percentage']}%)
║ ⏰ 리셋까지: {usage.get('time_remaining', 'N/A')}
╚══════════════════════════════════════════════════════════════
        """.strip()


def run_once():
    """한 번만 실행"""
    statusline = format_statusline(compact=True)
    print(statusline)


def run_continuous(interval=60):
    """연속 실행 모드 (interval초마다 새로고침)"""
    try:
        while True:
            # 상태바 출력
            statusline = format_statusline(compact=True)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {statusline}")

            # 다음 업데이트까지 대기
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n상태바 모니터링을 종료합니다.")
        sys.exit(0)


def main():
    """메인 실행 함수"""
    # 명령줄 인수 확인
    if len(sys.argv) > 1:
        if sys.argv[1] == "--sync" or sys.argv[1] == "-s":
            # 동기화 모드
            if len(sys.argv) < 4:
                print("❌ 사용법: python statusline.py --sync <사용량%> <리셋 시간>")
                print("   예시: python statusline.py --sync 100 \"2시간 21분\"")
                print("   예시: python statusline.py --sync 85 \"1시간 30분\"")
                sys.exit(1)

            try:
                usage_percent = int(sys.argv[2])
                time_remaining = sys.argv[3]

                if get_claude_usage_api is None:
                    print("❌ claude_usage_api 모듈을 불러올 수 없습니다.")
                    sys.exit(1)

                api = get_claude_usage_api()
                result = api.sync_baseline(usage_percent, time_remaining)

                if result['success']:
                    print(result['message'])
                    print(f"\n📊 동기화 정보:")
                    print(f"  - 기준 사용량: {result['baseline']['baseline_used']}%")
                    print(f"  - CLI 메시지 수: {result['baseline']['baseline_cli_messages']}")
                    print(f"  - 리셋 시간: {result['baseline']['reset_time']}")
                    print(f"\n이제 statusline이 자동으로 CLI 사용량을 추적합니다.")
                else:
                    print(result['message'])
                    sys.exit(1)

            except ValueError:
                print("❌ 사용량은 숫자로 입력해주세요. (0-100)")
                sys.exit(1)

        elif sys.argv[1] == "--continuous" or sys.argv[1] == "-c":
            # 연속 모드 (60초 간격)
            interval = 60
            if len(sys.argv) > 2:
                try:
                    interval = int(sys.argv[2])
                except ValueError:
                    pass
            print(f"상태바 모니터링 시작 (새로고침 간격: {interval}초)")
            print("종료하려면 Ctrl+C를 누르세요.\n")
            run_continuous(interval)
        elif sys.argv[1] == "--detail" or sys.argv[1] == "-d":
            # 상세 모드
            statusline = format_statusline(compact=False)
            print(statusline)
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("""
Claude Code 상태바 스크립트

사용법:
  python statusline.py              # 한 번 출력 (컴팩트)
  python statusline.py -s 100 "2시간 21분"  # 사용량 동기화
  python statusline.py -c           # 연속 모드 (60초 간격)
  python statusline.py -c 30        # 연속 모드 (30초 간격)
  python statusline.py -d           # 상세 출력
  python statusline.py -h           # 도움말

옵션:
  -s, --sync <사용량%> <리셋시간>  웹/앱 사용량 동기화
  -c, --continuous [INTERVAL]      연속 모드로 실행 (기본: 60초)
  -d, --detail                     상세 정보 출력
  -h, --help                       이 도움말 출력

동기화 예시:
  python statusline.py --sync 100 "2시간 21분"
  python statusline.py --sync 85 "1시간 30분"
  python statusline.py --sync 50 "3시간"
            """)
        else:
            run_once()
    else:
        # 기본: 한 번만 실행
        run_once()


if __name__ == "__main__":
    main()
