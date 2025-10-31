"""
언어 관리 클래스
Streamlit session_state를 사용하여 언어 선택을 관리합니다.
"""

import streamlit as st
from .translator import Translator


class LanguageManager:
    """언어 선택 및 상태 관리 클래스"""

    SESSION_KEY = "app_language"
    DEFAULT_LANGUAGE = "ko"

    def __init__(self, translator: Translator):
        """
        언어 관리자 초기화

        Args:
            translator: Translator 인스턴스
        """
        self.translator = translator
        self._init_session_state()

    def _init_session_state(self) -> None:
        """세션 상태 초기화"""
        if self.SESSION_KEY not in st.session_state:
            st.session_state[self.SESSION_KEY] = self.DEFAULT_LANGUAGE
            self.translator.set_language(self.DEFAULT_LANGUAGE)

    def get_current_language(self) -> str:
        """
        현재 언어 코드 가져오기

        Returns:
            현재 언어 코드
        """
        return st.session_state.get(self.SESSION_KEY, self.DEFAULT_LANGUAGE)

    def set_current_language(self, language_code: str) -> bool:
        """
        언어 변경

        Args:
            language_code: 변경할 언어 코드

        Returns:
            성공 여부
        """
        if self.translator.set_language(language_code):
            st.session_state[self.SESSION_KEY] = language_code
            return True
        return False

    def render_language_selector(self, position: str = "sidebar") -> None:
        """
        언어 선택 UI 렌더링

        Args:
            position: "sidebar" 또는 "main" (렌더링 위치)
        """
        # 렌더링 위치 결정
        if position == "sidebar":
            container = st.sidebar
        else:
            container = st

        with container:
            st.markdown("---")
            col1, col2, col3 = st.columns(3)

            languages = self.translator.get_languages()
            current_lang = self.get_current_language()

            with col1:
                if st.button("🇰🇷 한글", use_container_width=True):
                    if self.set_current_language("ko"):
                        st.rerun()

            with col3:
                if st.button("🇬🇧 English", use_container_width=True):
                    if self.set_current_language("en"):
                        st.rerun()

    def get_text(self, key: str, default: str = "") -> str:
        """
        번역된 텍스트 가져오기

        Args:
            key: 번역 키 (점으로 구분된 중첩 경로)
            default: 기본값

        Returns:
            번역된 텍스트
        """
        return self.translator.get(key, default)

    def get_menu_items(self) -> dict:
        """현재 언어의 메뉴 항목 가져오기"""
        return self.translator.get_menu_items()

    def get_menu_list(self) -> list:
        """메뉴 항목을 리스트로 가져오기"""
        return self.translator.get_menu_list()

    def __str__(self) -> str:
        """현재 언어 정보"""
        return f"LanguageManager(current={self.get_current_language()})"
