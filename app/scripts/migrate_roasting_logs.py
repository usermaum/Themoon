#!/usr/bin/env python3
"""
T1-1 마이그레이션: Excel → RoastingLog 데이터 이전

Excel "문드립바 로스팅 일지.xlsx" Sheet1(2)의 로스팅 기록을
RoastingLog 테이블로 마이그레이션합니다.

실행 방법:
./venv/bin/python3 app/scripts/migrate_roasting_logs.py
"""

import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import logging
import sys
import os

# 프로젝트 루트 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.models.database import SessionLocal, RoastingLog, Bean

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def migrate_roasting_logs():
    """Excel 로스팅 기록을 DB로 마이그레이션"""

    excel_path = "Documents/Resources/문드립바 로스팅 일지.xlsx"

    if not os.path.exists(excel_path):
        logger.error(f"❌ Excel 파일을 찾을 수 없습니다: {excel_path}")
        return False

    try:
        # Excel 데이터 읽기
        logger.info(f"📄 Excel 파일 읽기: {excel_path}")
        df = pd.read_excel(excel_path, sheet_name="Sheet1 (2)")

        logger.info(f"✅ Excel 읽음: {len(df)} 행, {len(df.columns)} 컬럼")
        print(f"\n{'=' * 60}")
        print("📊 Excel 원본 데이터")
        print(f"{'=' * 60}")
        print(df.to_string())

        # 두 개의 블렌드 섹션 추출
        # 좌측: 풀문 (Full Moon) - 컬럼 0,1,2
        # 우측: 뉴문 (New Moon) - 컬럼 10,11,12
        data_list = []

        # 풀문 데이터 (마사이, 안티구아, 모모라, g4)
        for idx in range(4):
            bean_name = df.iloc[idx, 0]
            raw_weight = df.iloc[idx, 1]
            roasted_weight = df.iloc[idx, 2]

            if pd.notna(bean_name) and pd.notna(raw_weight) and pd.notna(roasted_weight):
                data_list.append({
                    'bean_name': str(bean_name).strip(),
                    'raw_weight_kg': float(raw_weight),
                    'roasted_weight_kg': float(roasted_weight),
                    'blend_type': '풀문'
                })

        # 뉴문 데이터 (브라질, 콜롬비아, g4)
        for idx in range(3):
            bean_name = df.iloc[idx, 10]
            raw_weight = df.iloc[idx, 11]
            roasted_weight = df.iloc[idx, 12]

            if pd.notna(bean_name) and pd.notna(raw_weight) and pd.notna(roasted_weight):
                data_list.append({
                    'bean_name': str(bean_name).strip(),
                    'raw_weight_kg': float(raw_weight),
                    'roasted_weight_kg': float(roasted_weight),
                    'blend_type': '뉴문'
                })

        # DB 세션
        db = SessionLocal()

        # 기존 로스팅 로그 조회 (중복 방지)
        existing_count = db.query(RoastingLog).count()
        logger.info(f"기존 로스팅 로그: {existing_count}건")

        # 마이그레이션 실행
        inserted_count = 0
        errors = []

        print(f"\n{'=' * 60}")
        print("📥 마이그레이션 시작")
        print(f"{'=' * 60}")

        # 날짜 가정: 2025-10-24부터 시작 (각 원두별로 1일씩 간격)
        base_date = datetime(2025, 10, 24).date()

        for idx, row in enumerate(data_list):
            try:
                bean_name = row['bean_name']
                raw_weight = row['raw_weight_kg']
                roasted_weight = row['roasted_weight_kg']
                blend_type = row['blend_type']

                # 손실률 계산
                loss_rate = ((raw_weight - roasted_weight) / raw_weight) * 100

                # 날짜: 인덱스별로 1일씩 증가
                roasting_date = base_date + timedelta(days=idx)
                roasting_month = roasting_date.strftime('%Y-%m')

                # 손실률 편차 (예상 17% 대비)
                expected_loss = 17.0
                loss_variance = loss_rate - expected_loss

                # 로그 생성
                roasting_log = RoastingLog(
                    raw_weight_kg=round(raw_weight, 2),
                    roasted_weight_kg=round(roasted_weight, 2),
                    loss_rate_percent=round(loss_rate, 2),
                    expected_loss_rate_percent=expected_loss,
                    loss_variance_percent=round(loss_variance, 2),
                    roasting_date=roasting_date,
                    roasting_month=roasting_month,
                    notes=f"자동 마이그레이션 - {bean_name}"
                )

                db.add(roasting_log)
                db.commit()
                db.refresh(roasting_log)

                logger.info(f"✓ {bean_name} ({roasting_date}): {raw_weight}kg → {roasted_weight}kg ({loss_rate:.1f}% 손실)")
                inserted_count += 1

            except Exception as e:
                db.rollback()
                error_msg = f"행 {idx}: {str(e)}"
                logger.warning(f"⚠️ {error_msg}")
                errors.append(error_msg)

        db.close()

        # 결과 출력
        print(f"\n{'=' * 60}")
        print("📈 마이그레이션 결과")
        print(f"{'=' * 60}")
        print(f"✅ 삽입됨: {inserted_count}건")
        print(f"⚠️  오류: {len(errors)}건")

        if errors:
            print("\n오류 상세:")
            for error in errors:
                print(f"  • {error}")

        # 검증
        db = SessionLocal()
        total_logs = db.query(RoastingLog).count()
        print(f"\n💾 DB 확인: 총 {total_logs}건 로스팅 로그")

        if total_logs > 0:
            logs = db.query(RoastingLog).all()
            print("\n📋 마이그레이션된 데이터 (처음 5건):")
            for log in logs[:5]:
                print(f"  • {log.roasting_date}: {log.raw_weight_kg}kg → {log.roasted_weight_kg}kg ({log.loss_rate_percent}% 손실)")

        db.close()

        return len(errors) == 0

    except Exception as e:
        logger.error(f"❌ 마이그레이션 실패: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    success = migrate_roasting_logs()
    sys.exit(0 if success else 1)
