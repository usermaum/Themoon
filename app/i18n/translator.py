"""
번역 관리 클래스
JSON 파일에서 다국어 텍스트를 로드하고 관리합니다.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class Translator:
    """다국어 번역 관리 클래스"""

    def __init__(self, default_language: str = "ko"):
        """
        번역기 초기화

        Args:
            default_language: 기본 언어 (기본값: "ko")
        """
        self.default_language = default_language
        self.current_language = default_language
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.available_languages = []

        # 언어 파일 로드
        self._load_languages()

    def _load_languages(self) -> None:
        """locales 폴더에서 모든 언어 파일 로드"""
        locales_path = Path(__file__).parent / "locales"

        if not locales_path.exists():
            raise FileNotFoundError(f"Locales folder not found: {locales_path}")

        # 모든 JSON 파일 찾기
        for locale_file in locales_path.glob("*.json"):
            language_code = locale_file.stem  # 파일명에서 확장자 제외
            try:
                with open(locale_file, "r", encoding="utf-8") as f:
                    self.translations[language_code] = json.load(f)
                self.available_languages.append(language_code)
            except (json.JSONDecodeError, IOError) as e:
                raise ValueError(f"Failed to load language file {locale_file}: {e}")

        if not self.translations:
            raise ValueError("No language files found in locales folder")

    def set_language(self, language_code: str) -> bool:
        """
        언어 설정

        Args:
            language_code: 언어 코드 (예: "ko", "en")

        Returns:
            성공 여부
        """
        if language_code not in self.translations:
            return False

        self.current_language = language_code
        return True

    def get(self, key: str, default: Optional[str] = None) -> str:
        """
        중첩 키로 번역 텍스트 가져오기

        Args:
            key: 번역 키 (점으로 구분된 중첩 경로, 예: "menu.home.name")
            default: 키를 찾을 수 없을 때 반환할 기본값

        Returns:
            번역된 텍스트 또는 기본값
        """
        keys = key.split(".")
        value = self.translations.get(self.current_language, {})

        # 중첩된 키 따라가기
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                # 키를 찾을 수 없음
                if default is not None:
                    return default
                # 폴백: 기본 언어에서 찾기
                return self._get_from_default(key, key)

        if value is None:
            if default is not None:
                return default
            # 폴백: 기본 언어에서 찾기
            return self._get_from_default(key, key)

        return str(value)

    def _get_from_default(self, key: str, fallback: str) -> str:
        """
        기본 언어에서 번역 텍스트 가져오기

        Args:
            key: 번역 키
            fallback: 못 찾을 경우 반환할 값

        Returns:
            기본 언어의 번역 텍스트 또는 폴백값
        """
        keys = key.split(".")
        value = self.translations.get(self.default_language, {})

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return fallback

        return str(value) if value is not None else fallback

    def get_menu_items(self) -> Dict[str, Dict[str, str]]:
        """
        현재 언어의 메뉴 항목 모두 가져오기

        Returns:
            메뉴 항목 딕셔너리
        """
        return self.translations.get(self.current_language, {}).get("menu", {})

    def get_menu_list(self) -> list:
        """
        메뉴 항목을 리스트로 가져오기 (순서 유지)

        Returns:
            (key, name, icon) 튜플 리스트
        """
        menu_items = self.get_menu_items()
        result = []

        # 순서 유지를 위해 정의된 순서대로 반환
        menu_order = [
            "home",
            "bean_management",
            "blend_management",
            "analysis",
            "inventory_management",
            "dashboard",
            "settings",
            "report",
            "excel_sync",
            "advanced_analysis",
        ]

        for menu_key in menu_order:
            if menu_key in menu_items:
                item = menu_items[menu_key]
                result.append(
                    (menu_key, item.get("name", ""), item.get("icon", ""))
                )

        return result

    def get_languages(self) -> Dict[str, str]:
        """
        사용 가능한 언어 목록 가져오기

        Returns:
            {언어코드: 언어이름} 딕셔너리
        """
        languages = {}
        for lang_code in self.available_languages:
            # 각 언어의 이름을 언어 파일에서 가져오기
            lang_name = self.get(
                "app.title", fallback="Unknown"
            )  # 임시로 앱 제목 사용

            # 더 나은 방법: 각 언어의 "language_name" 키 추가
            if lang_code == "ko":
                languages[lang_code] = "🇰🇷 한글"
            elif lang_code == "en":
                languages[lang_code] = "🇬🇧 English"
            else:
                languages[lang_code] = lang_code.upper()

        return languages

    def __str__(self) -> str:
        """현재 언어 정보"""
        return f"Translator(language={self.current_language}, available={self.available_languages})"
