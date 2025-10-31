#!/usr/bin/env python3
"""
다중 언어 지원 시스템 테스트
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from i18n import Translator

def test_translator():
    """번역 시스템 테스트"""
    print("=" * 60)
    print("🌍 다중 언어 지원 시스템 테스트")
    print("=" * 60)

    # Translator 초기화
    translator = Translator(default_language="ko")
    print(f"\n✅ Translator 초기화 완료: {translator}")

    # 지원하는 언어 확인
    print(f"\n📋 지원하는 언어: {translator.available_languages}")

    # 한글 테스트
    print("\n🇰🇷 한글 테스트:")
    translator.set_language("ko")
    print(f"  - 앱 제목: {translator.get('app.title')}")
    print(f"  - 앱 부제목: {translator.get('app.subtitle')}")
    print(f"  - 메뉴 (원두관리): {translator.get('menu.bean_management.name')}")
    print(f"  - 메뉴 (블렌딩관리): {translator.get('menu.blend_management.name')}")
    print(f"  - 메뉴 (분석): {translator.get('menu.analysis.name')}")
    print(f"  - 메뉴 (재고관리): {translator.get('menu.inventory_management.name')}")
    print(f"  - 메뉴 (대시보드): {translator.get('menu.dashboard.name')}")
    print(f"  - 언어 라벨: {translator.get('sidebar.language_label')}")

    # 영문 테스트
    print("\n🇬🇧 English Test:")
    translator.set_language("en")
    print(f"  - App Title: {translator.get('app.title')}")
    print(f"  - App Subtitle: {translator.get('app.subtitle')}")
    print(f"  - Menu (Bean Management): {translator.get('menu.bean_management.name')}")
    print(f"  - Menu (Blend Management): {translator.get('menu.blend_management.name')}")
    print(f"  - Menu (Analysis): {translator.get('menu.analysis.name')}")
    print(f"  - Menu (Inventory Management): {translator.get('menu.inventory_management.name')}")
    print(f"  - Menu (Dashboard): {translator.get('menu.dashboard.name')}")
    print(f"  - Language Label: {translator.get('sidebar.language_label')}")

    # 메뉴 목록 테스트
    print("\n📋 메뉴 목록 (한글):")
    translator.set_language("ko")
    menu_list = translator.get_menu_list()
    for i, (key, name, icon) in enumerate(menu_list, 1):
        print(f"  {i}. {icon} {name}")

    print("\n📋 Menu List (English):")
    translator.set_language("en")
    menu_list = translator.get_menu_list()
    for i, (key, name, icon) in enumerate(menu_list, 1):
        print(f"  {i}. {icon} {name}")

    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료!")
    print("=" * 60)

if __name__ == "__main__":
    test_translator()
