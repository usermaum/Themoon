#!/usr/bin/env python3
"""
버전 관리 도구

기능:
- VERSION 파일 업데이트
- CHANGELOG.md에 변경사항 자동 추가
- Semantic Versioning 적용

사용법:
  python logs/update_version.py --type patch --summary "버그 수정"
  python logs/update_version.py --type minor --summary "새 기능 추가"
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import argparse
from enum import Enum

class VersionType(Enum):
    PATCH = "patch"
    MINOR = "minor"
    MAJOR = "major"

class VersionManager:
    def __init__(self, project_root=None):
        """버전 관리자 초기화"""
        if project_root is None:
            # 현재 스크립트 위치를 기준으로 프로젝트 루트 파악
            current_file = os.path.abspath(__file__)
            logs_dir = os.path.dirname(current_file)
            project_root = os.path.dirname(logs_dir)

        self.project_root = project_root
        self.logs_dir = os.path.join(project_root, "logs")
        self.version_file = os.path.join(self.logs_dir, "VERSION")
        self.changelog_file = os.path.join(self.logs_dir, "CHANGELOG.md")

    def read_version(self):
        """현재 버전 읽기"""
        try:
            with open(self.version_file, 'r') as f:
                version = f.read().strip()
            return version
        except FileNotFoundError:
            print(f"❌ VERSION 파일을 찾을 수 없습니다: {self.version_file}")
            return None

    def parse_version(self, version_str):
        """버전 문자열 파싱"""
        try:
            parts = version_str.split('.')
            return {
                'major': int(parts[0]),
                'minor': int(parts[1]),
                'patch': int(parts[2])
            }
        except (IndexError, ValueError):
            print(f"❌ 유효하지 않은 버전 형식: {version_str}")
            return None

    def increment_version(self, current_version, version_type):
        """버전 증가"""
        parts = self.parse_version(current_version)
        if parts is None:
            return None

        if version_type == VersionType.MAJOR:
            parts['major'] += 1
            parts['minor'] = 0
            parts['patch'] = 0
        elif version_type == VersionType.MINOR:
            parts['minor'] += 1
            parts['patch'] = 0
        elif version_type == VersionType.PATCH:
            parts['patch'] += 1

        new_version = f"{parts['major']}.{parts['minor']}.{parts['patch']}"
        return new_version

    def write_version(self, new_version):
        """버전 파일 업데이트"""
        try:
            with open(self.version_file, 'w') as f:
                f.write(f"{new_version}\n")
            print(f"✅ VERSION 파일 업데이트: {new_version}")
            return True
        except IOError as e:
            print(f"❌ VERSION 파일 쓰기 실패: {e}")
            return False

    def update_changelog(self, new_version, version_type, summary, changes=None):
        """CHANGELOG.md 업데이트"""
        try:
            with open(self.changelog_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 새 버전 섹션 생성
            today = datetime.now().strftime('%Y-%m-%d')
            type_emoji = {
                VersionType.MAJOR: "🚀",
                VersionType.MINOR: "✨",
                VersionType.PATCH: "🐛"
            }

            type_label = {
                VersionType.MAJOR: "주요 버전 (Major Release)",
                VersionType.MINOR: "마이너 업데이트 (Minor Update)",
                VersionType.PATCH: "패치 (Bug Fix)"
            }

            new_section = f"""## [{new_version}] - {today}

### {type_emoji[version_type]} {type_label[version_type]}: {summary}

#### 📝 변경사항
{changes if changes else '- 변경사항 상세 기록 필요'}

"""

            # 기존 버전 섹션 찾아서 그 전에 삽입
            insert_pos = content.find("## [")
            if insert_pos == -1:
                # 버전 섹션이 없으면 버전 관리 가이드 전에 삽입
                insert_pos = content.find("## 버전 관리 가이드")

            if insert_pos != -1:
                new_content = content[:insert_pos] + new_section + content[insert_pos:]
            else:
                new_content = content + "\n" + new_section

            with open(self.changelog_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ CHANGELOG.md 업데이트: [{new_version}]")
            return True
        except IOError as e:
            print(f"❌ CHANGELOG.md 업데이트 실패: {e}")
            return False

    def show_current_version(self):
        """현재 버전 표시"""
        version = self.read_version()
        if version:
            print(f"📦 현재 버전: {version}")
        return version

def main():
    parser = argparse.ArgumentParser(
        description="버전 관리 도구 - 자동으로 버전과 변경로그 관리"
    )
    parser.add_argument(
        '--type',
        choices=['patch', 'minor', 'major'],
        required=False,
        help='버전 타입 (patch, minor, major)'
    )
    parser.add_argument(
        '--summary',
        required=False,
        help='변경사항 요약'
    )
    parser.add_argument(
        '--changes',
        required=False,
        help='상세한 변경사항 (여러 줄 가능)'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='현재 버전 표시'
    )

    args = parser.parse_args()

    # 버전 관리자 초기화
    manager = VersionManager()

    # 현재 버전만 표시
    if args.show or (args.type is None and args.summary is None):
        manager.show_current_version()
        return

    # 버전 업데이트
    if args.type and args.summary:
        current_version = manager.read_version()
        if current_version is None:
            return

        version_type = VersionType(args.type)
        new_version = manager.increment_version(current_version, version_type)

        if new_version is None:
            return

        print(f"\n📊 버전 업데이트 정보:")
        print(f"  이전 버전: {current_version}")
        print(f"  새로운 버전: {new_version}")
        print(f"  타입: {version_type.value}")
        print(f"  요약: {args.summary}\n")

        # 파일 업데이트
        if manager.write_version(new_version):
            manager.update_changelog(new_version, version_type, args.summary, args.changes)
            print(f"\n✅ 버전 관리 완료!")
    else:
        print("❌ --type과 --summary 옵션이 필요합니다")
        parser.print_help()

if __name__ == "__main__":
    main()
