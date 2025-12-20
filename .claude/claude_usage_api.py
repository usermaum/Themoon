#!/usr/bin/env python3
"""
Claude Pro 사용량 API 모듈
history.jsonl 파일을 분석하여 실시간 사용량 정보 자동 추적
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path


class ClaudeUsageAPI:
    """Claude Pro 사용량 조회 클래스"""

    def __init__(self):
        """API 클라이언트 초기화"""
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.base_url = "https://api.anthropic.com/v1"
        self.cache_file = Path.home() / ".cache" / "claude_usage.json"
        self.baseline_file = Path.home() / ".cache" / "claude_usage_baseline.json"
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)

        # Claude Code history 파일 경로
        self.history_file = Path.home() / ".claude" / "history.jsonl"

        # Claude Pro 플랜 설정 (5시간 윈도우, 100 메시지 제한)
        self.window_hours = 5
        self.message_limit = 100

    def _load_cache(self):
        """캐시된 사용량 데이터 로드"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, "r") as f:
                    cache_data = json.load(f)

                # 캐시가 60초 이내라면 사용
                cache_time = datetime.fromisoformat(cache_data.get("timestamp", ""))
                if (datetime.now() - cache_time).seconds < 60:
                    return cache_data.get("usage")
        except Exception:
            pass
        return None

    def _save_cache(self, usage_data):
        """사용량 데이터 캐시 저장"""
        try:
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "usage": usage_data
            }
            with open(self.cache_file, "w") as f:
                json.dump(cache_data, f, indent=2)
        except Exception:
            pass

    def _load_baseline(self):
        """저장된 baseline 데이터 로드"""
        try:
            if self.baseline_file.exists():
                with open(self.baseline_file, "r") as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    def _save_baseline(self, baseline_data):
        """baseline 데이터 저장"""
        try:
            with open(self.baseline_file, "w") as f:
                json.dump(baseline_data, f, indent=2)
        except Exception:
            pass

    def _parse_time_remaining(self, time_str):
        """'2시간 21분' 같은 문자열을 파싱해서 datetime으로 변환"""
        try:
            hours = 0
            minutes = 0

            # "2시간 21분", "1시간", "30분" 등 다양한 형식 지원
            time_str = time_str.strip()

            # 시간 파싱
            if "시간" in time_str:
                hour_part = time_str.split("시간")[0].strip()
                hours = int(hour_part.split()[-1])

            # 분 파싱
            if "분" in time_str:
                min_part = time_str.split("분")[0].strip()
                if "시간" in min_part:
                    min_part = min_part.split("시간")[-1].strip()
                minutes = int(min_part.split()[-1])

            # 현재 시간 + 남은 시간 = 리셋 시간
            reset_time = datetime.now() + timedelta(hours=hours, minutes=minutes)
            return reset_time

        except Exception:
            # 파싱 실패 시 기본값 (5시간 후)
            return datetime.now() + timedelta(hours=self.window_hours)

    def _count_recent_messages(self):
        """최근 5시간 내 메시지 수 카운트"""
        try:
            if not self.history_file.exists():
                return 0, None, None

            # 현재 시간
            now = datetime.now()
            window_start = now - timedelta(hours=self.window_hours)
            window_start_ms = int(window_start.timestamp() * 1000)

            # history.jsonl 역순으로 읽기 (최신부터)
            message_count = 0
            oldest_message_time = None
            newest_message_time = None

            with open(self.history_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 역순으로 읽기
            for line in reversed(lines):
                try:
                    entry = json.loads(line.strip())
                    timestamp = entry.get('timestamp', 0)

                    # 윈도우 밖이면 중단
                    if timestamp < window_start_ms:
                        break

                    # 메시지 카운트
                    message_count += 1

                    # 시간 기록
                    if oldest_message_time is None:
                        oldest_message_time = timestamp
                    newest_message_time = timestamp

                except (json.JSONDecodeError, KeyError):
                    continue

            return message_count, oldest_message_time, newest_message_time

        except Exception:
            return 0, None, None

    def _calculate_reset_time(self, oldest_message_time):
        """다음 리셋 시간 계산"""
        try:
            if oldest_message_time is None:
                # 메시지가 없으면 현재 시간 기준
                return datetime.now() + timedelta(hours=self.window_hours)

            # 가장 오래된 메시지 시간 + 5시간
            oldest_dt = datetime.fromtimestamp(oldest_message_time / 1000)
            reset_time = oldest_dt + timedelta(hours=self.window_hours)

            return reset_time

        except Exception:
            return datetime.now() + timedelta(hours=self.window_hours)

    def _format_time_remaining(self, reset_time):
        """리셋까지 남은 시간 포맷"""
        try:
            now = datetime.now()
            if reset_time <= now:
                return "곧 리셋"

            delta = reset_time - now
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60

            if hours > 0:
                return f"{hours}시간 {minutes}분 후"
            else:
                return f"{minutes}분 후"

        except Exception:
            return "N/A"

    def sync_baseline(self, current_usage, time_remaining_str):
        """웹/앱에서 확인한 현재 상태를 baseline으로 저장"""
        try:
            # 현재 history.jsonl의 전체 메시지 수 카운트
            total_cli_messages = 0
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    total_cli_messages = sum(1 for _ in f)

            # 리셋 시간 파싱
            reset_time = self._parse_time_remaining(time_remaining_str)

            # baseline 데이터 저장
            baseline_data = {
                "baseline_used": current_usage,
                "baseline_timestamp": datetime.now().isoformat(),
                "baseline_cli_messages": total_cli_messages,
                "reset_time": reset_time.isoformat(),
                "sync_method": "manual"
            }

            self._save_baseline(baseline_data)

            # 캐시 클리어 (다음 조회 시 새로 계산)
            if self.cache_file.exists():
                self.cache_file.unlink()

            return {
                "success": True,
                "message": f"✅ Baseline 동기화 완료: {current_usage}% 사용 중, {time_remaining_str} 후 리셋",
                "baseline": baseline_data
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"❌ 동기화 실패: {str(e)}"
            }

    def get_usage(self):
        """Claude Pro 사용량 정보 가져오기 (baseline + 자동 추적)"""
        # 캐시된 데이터 확인
        cached = self._load_cache()
        if cached:
            return cached

        try:
            # baseline 데이터 로드
            baseline = self._load_baseline()

            if baseline:
                # === Baseline 기반 계산 ===
                # 리셋 시간 체크
                reset_time = datetime.fromisoformat(baseline['reset_time'])
                now = datetime.now()

                if now >= reset_time:
                    # 리셋 시간 지남 -> baseline 삭제하고 0%부터 시작
                    self.baseline_file.unlink()
                    baseline = None
                else:
                    # 현재 CLI 메시지 수
                    total_cli_messages = 0
                    if self.history_file.exists():
                        with open(self.history_file, 'r', encoding='utf-8') as f:
                            total_cli_messages = sum(1 for _ in f)

                    # CLI 증가분 계산
                    cli_increase = max(total_cli_messages - baseline['baseline_cli_messages'], 0)

                    # 총 사용량 = baseline + CLI 증가분
                    total_used = baseline['baseline_used'] + cli_increase

                    # 100을 초과할 수 없음
                    total_used = min(total_used, self.message_limit)

                    # 사용 퍼센트
                    percentage = min(int((total_used / self.message_limit) * 100), 100)

                    # 남은 메시지
                    remaining = max(self.message_limit - total_used, 0)

                    # 리셋까지 남은 시간
                    time_remaining = self._format_time_remaining(reset_time)

                    # 사용량 데이터 구성
                    usage_data = {
                        "daily_limit": self.message_limit,
                        "used": total_used,
                        "remaining": remaining,
                        "percentage": percentage,
                        "reset_time": reset_time.isoformat(),
                        "time_remaining": time_remaining,
                        "status": "baseline",
                        "cli_increase": cli_increase
                    }

                    # 캐시 저장
                    self._save_cache(usage_data)
                    return usage_data

            # === Baseline 없음 -> 자동 추적 (기존 로직) ===
            # history.jsonl에서 최근 5시간 메시지 카운트
            message_count, oldest_time, newest_time = self._count_recent_messages()

            # 사용 퍼센트 계산
            percentage = min(int((message_count / self.message_limit) * 100), 100)

            # 남은 메시지 수
            remaining = max(self.message_limit - message_count, 0)

            # 다음 리셋 시간 계산
            reset_time = self._calculate_reset_time(oldest_time)
            time_remaining = self._format_time_remaining(reset_time)

            # 사용량 데이터 구성
            usage_data = {
                "daily_limit": self.message_limit,
                "used": message_count,
                "remaining": remaining,
                "percentage": percentage,
                "reset_time": reset_time.isoformat(),
                "time_remaining": time_remaining,
                "status": "auto"
            }

            # 캐시 저장
            self._save_cache(usage_data)
            return usage_data

        except Exception as e:
            # 에러 발생 시 기본값 반환
            return {
                "daily_limit": self.message_limit,
                "used": 0,
                "remaining": self.message_limit,
                "percentage": 0,
                "time_remaining": "N/A",
                "status": f"error: {str(e)}"
            }

    def get_usage_bar(self, width=10):
        """사용량을 프로그레스 바로 표시"""
        usage = self.get_usage()

        try:
            percentage = usage.get("percentage", 0)
            filled = int(width * percentage / 100)
            empty = width - filled

            # 이모지 프로그레스 바
            bar = "🟩" * filled + "⬜" * empty

            return f"{bar} {percentage}%"
        except Exception:
            return "⬜" * width + " N/A"


# 싱글톤 인스턴스
_usage_api = None


def get_claude_usage_api():
    """Claude 사용량 API 싱글톤 인스턴스 반환"""
    global _usage_api
    if _usage_api is None:
        _usage_api = ClaudeUsageAPI()
    return _usage_api


if __name__ == "__main__":
    # 테스트
    api = get_claude_usage_api()
    usage = api.get_usage()
    print(json.dumps(usage, indent=2))
    print(f"\n사용량 바: {api.get_usage_bar()}")
