#!/usr/bin/env python3
"""
Claude Pro 사용량 API 모듈
Anthropic API를 통해 실시간 사용량 정보 조회
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path


class ClaudeUsageAPI:
    """Claude Pro 사용량 조회 클래스"""

    def __init__(self):
        """API 클라이언트 초기화"""
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.base_url = "https://api.anthropic.com/v1"
        self.cache_file = Path.home() / ".cache" / "claude_usage.json"
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)

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

    def get_usage(self):
        """Claude Pro 사용량 정보 가져오기"""
        # 캐시된 데이터 확인
        cached = self._load_cache()
        if cached:
            return cached

        # API 키가 없으면 placeholder 반환
        if not self.api_key:
            return {
                "daily_limit": 100,
                "used": 0,
                "remaining": 100,
                "percentage": 0,
                "status": "no_api_key"
            }

        try:
            # Anthropic API를 통한 사용량 조회
            # 주의: 실제 API 엔드포인트는 Anthropic 문서 확인 필요
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }

            # 현재 Anthropic API에는 직접적인 사용량 조회 엔드포인트가 없을 수 있음
            # 대안: 로컬에서 요청 수를 카운트하거나, 별도 추적 시스템 사용

            # Placeholder 데이터 (실제 API 연동 필요)
            usage_data = {
                "daily_limit": 100,
                "used": "API 연동 필요",
                "remaining": "API 연동 필요",
                "percentage": 0,
                "status": "api_not_available"
            }

            self._save_cache(usage_data)
            return usage_data

        except Exception as e:
            # 에러 발생 시 기본값 반환
            return {
                "daily_limit": 100,
                "used": "Error",
                "remaining": "Error",
                "percentage": 0,
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
