#!/usr/bin/env python3
"""
Claude Code Statusline Script
Display colorful status bar with emojis and real-time info
Auto-refresh every 60 seconds
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

# Import claude_usage_api module from same directory
sys.path.insert(0, str(Path(__file__).parent))
try:
    from claude_usage_api import get_claude_usage_api
except ImportError:
    get_claude_usage_api = None


def get_git_branch():
    """Get current Git branch name"""
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
    """Get Claude model and session information"""
    try:
        # Get status info via ccusage command
        result = subprocess.run(
            ["npx", "-y", "ccusage@latest", "statusline", "--cache", "--no-offline"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=Path(__file__).parent.parent
        )

        # Default info
        model_name = "Sonnet 4.5"
        context_usage = "N/A"
        session_id = "unknown"

        # Parse info from ccusage output
        output = result.stdout
        if "%" in output:
            # Find percentage indicator
            for part in output.split():
                if "%" in part:
                    context_usage = part.strip().replace("%", "") + "%"
                    break

        # Replace session ID with env var or process ID
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
    """Get application version"""
    try:
        version_file = Path(__file__).parent.parent / "logs" / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        return "0.2.0"
    except Exception:
        return "0.2.0"


def get_claude_usage():
    """Get Claude Pro usage information"""
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


def format_usage_bar(percentage, width=50):
    """Create Settings-style progress bar"""
    filled = int(width * percentage / 100)
    empty = width - filled

    # Use block character (same as Settings)
    bar = "█" * filled

    # Fill partial block (using partial block chars)
    remainder = (width * percentage / 100) - filled
    if remainder > 0 and empty > 0:
        if remainder < 0.25:
            bar += "▏"
        elif remainder < 0.50:
            bar += "▎"
        elif remainder < 0.75:
            bar += "▌"
        else:
            bar += "▋"
        empty -= 1

    bar += " " * empty
    return bar


def format_statusline(compact=True):
    """Format statusline in one line (Settings Usage style)"""
    # Current time/date
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    weekday = now.strftime("%a")

    # Git branch
    branch = get_git_branch()

    # Claude info
    claude_info = get_claude_info()

    # App version
    version = get_app_version()

    # Claude usage
    usage = get_claude_usage()

    # Usage color indicator (emoji for warning level)
    percentage = usage.get('percentage', 0)
    if percentage >= 90:
        usage_icon = "🔴"  # 90%+: Critical
    elif percentage >= 70:
        usage_icon = "🟡"  # 70-89%: Warning
    else:
        usage_icon = "💎"  # <70%: Normal

    if compact:
        # Compact version (one line) - English to prevent UTF-8 boundary errors
        statusline_parts = [
            f"{date_str}({weekday})",
            f"{time_str}",
            f"br:{branch}",
            f"{claude_info['model']}",
            f"ctx:{claude_info['context']}",
            f"v{version}",
            f"{usage_icon}{usage['used']}/{usage['daily_limit']}({usage['percentage']}%)",
            f"reset:{usage.get('time_remaining', 'N/A')}"
        ]
        return " | ".join(statusline_parts)
    else:
        # Settings Usage style (multi-line)
        session_bar = format_usage_bar(percentage, width=50)

        # Session reset time (Asia/Seoul timezone)
        from datetime import timezone
        import pytz

        try:
            reset_time = datetime.fromisoformat(usage.get('reset_time', ''))
            kst = pytz.timezone('Asia/Seoul')
            reset_time_kst = reset_time.astimezone(kst)
            reset_str = reset_time_kst.strftime("%I%p (Asia/Seoul)").lstrip("0").lower()
        except:
            reset_str = "N/A"

        # Weekly usage
        if get_claude_usage_api is not None:
            try:
                api = get_claude_usage_api()
                weekly = api.get_weekly_usage()
                weekly_percentage = weekly.get('percentage', 0)
                weekly_bar = format_usage_bar(weekly_percentage, width=50)
                weekly_used = weekly.get('used', 0)
                weekly_limit = weekly.get('weekly_limit', 500)

                # Parse reset time
                weekly_reset_time = datetime.fromisoformat(weekly.get('reset_time', ''))
                weekly_reset_kst = weekly_reset_time.astimezone(kst)
                weekly_reset_str = weekly_reset_kst.strftime("%b %d, %I%p (Asia/Seoul)").lstrip("0").lower()

            except:
                weekly_percentage = 0
                weekly_bar = format_usage_bar(0, width=50)
                weekly_used = 0
                weekly_limit = 500
                weekly_reset_str = "N/A"
        else:
            weekly_percentage = 0
            weekly_bar = format_usage_bar(0, width=50)
            weekly_used = 0
            weekly_limit = 500
            weekly_reset_str = "N/A"

        return f"""
╔═══════════════════════════════════════════════════════════
║ Settings: Status Config [Usage] (tab to cycle)
║
║ Current session - Resets {reset_str}
║ {session_bar}
║ {percentage}% used ({usage['used']}/{usage['daily_limit']})
║
║ Current week (all models) - Resets {weekly_reset_str}
║ {weekly_bar}
║ {weekly_percentage}% used ({weekly_used}/{weekly_limit})
║
║ Extra usage
║ Extra usage not enabled - /extra-usage to enable
║
║ Time: {time_str}  Date: {date_str} ({weekday})
║ Branch: {branch}  Model: {claude_info['model']}
║ Version: v{version}  Reset: {usage.get('time_remaining', 'N/A')}
╚═══════════════════════════════════════════════════════════
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
        print("\n\nStatusline monitoring stopped.")
        sys.exit(0)


def main():
    """메인 실행 함수"""
    # 명령줄 인수 확인
    if len(sys.argv) > 1:
        if sys.argv[1] == "--sync" or sys.argv[1] == "-s":
            # 동기화 모드
            if len(sys.argv) < 4:
                print("❌ Usage: python statusline.py --sync <usage%> <reset_time>")
                print("   Example: python statusline.py --sync 100 \"2h 21m\"")
                print("   Example: python statusline.py --sync 85 \"1h 30m\"")
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
                    print(f"\n📊 Sync Information:")
                    print(f"  - Baseline usage: {result['baseline']['baseline_used']}%")
                    print(f"  - CLI messages: {result['baseline']['baseline_cli_messages']}")
                    print(f"  - Reset time: {result['baseline']['reset_time']}")
                    print(f"\nStatusline will now automatically track CLI usage.")
                else:
                    print(result['message'])
                    sys.exit(1)

            except ValueError:
                print("❌ Usage must be a number (0-100)")
                sys.exit(1)

        elif sys.argv[1] == "--quick-sync" or sys.argv[1] == "-q":
            # 빠른 동기화 (퍼센트만 입력, 리셋 시간 자동 계산)
            if len(sys.argv) < 3:
                print("❌ Usage: python statusline.py --quick-sync <usage%>")
                print("   Example: python statusline.py --quick-sync 64")
                print("   Example: python statusline.py -q 85")
                print("\n   리셋 시간은 자동으로 5시간으로 설정됩니다.")
                sys.exit(1)

            try:
                usage_percent = int(sys.argv[2])

                if usage_percent < 0 or usage_percent > 100:
                    print("❌ 사용량은 0-100 사이의 값이어야 합니다.")
                    sys.exit(1)

                # 리셋 시간 자동 계산 (5시간 고정)
                time_remaining = "5시간 0분"

                if get_claude_usage_api is None:
                    print("❌ claude_usage_api 모듈을 불러올 수 없습니다.")
                    sys.exit(1)

                api = get_claude_usage_api()
                result = api.sync_baseline(usage_percent, time_remaining)

                if result['success']:
                    print(result['message'])
                    print(f"\n📊 빠른 동기화 완료:")
                    print(f"  - 사용량: {usage_percent}%")
                    print(f"  - 리셋: 5시간 후")
                    print(f"\n💡 더 정확한 리셋 시간을 원하면:")
                    print(f"   python statusline.py --sync {usage_percent} \"4시간 30분\"")
                else:
                    print(result['message'])
                    sys.exit(1)

            except ValueError:
                print("❌ 사용량은 숫자여야 합니다 (0-100)")
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
  python statusline.py -q 64        # 빠른 동기화 (추천!)
  python statusline.py -s 100 "2시간 21분"  # 정확한 동기화
  python statusline.py -c           # 연속 모드 (60초 간격)
  python statusline.py -d           # 상세 출력

옵션:
  -q, --quick-sync <사용량%>       빠른 동기화 (리셋 5시간 자동 설정)
  -s, --sync <사용량%> <리셋시간>  정확한 동기화 (리셋 시간 수동 지정)
  -c, --continuous [INTERVAL]      연속 모드로 실행 (기본: 60초)
  -d, --detail                     상세 정보 출력 (Settings 스타일)
  -h, --help                       이 도움말 출력

📌 빠른 동기화 (추천):
  1. Claude Code에서 /config 실행
  2. 사용량 퍼센트 확인 (예: 64%)
  3. python statusline.py -q 64

📌 정확한 동기화:
  python statusline.py -s 64 "4시간 30분"
  python statusline.py -s 85 "1시간 30분"
  python statusline.py -s 100 "5시간"
            """)
        else:
            run_once()
    else:
        # 기본: 한 번만 실행
        run_once()


if __name__ == "__main__":
    main()
