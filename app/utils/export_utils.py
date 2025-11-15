"""
Export Utilities
Excel/CSV 변환 유틸리티
"""

import pandas as pd
from io import BytesIO
from typing import Dict, List
import xlsxwriter
from datetime import datetime


def dataframe_to_excel(df: pd.DataFrame, sheet_name: str = "Sheet1") -> BytesIO:
    """
    DataFrame을 Excel 파일로 변환 (단일 시트)

    Args:
        df: 변환할 DataFrame
        sheet_name: 시트 이름

    Returns:
        BytesIO: 메모리 내 Excel 파일
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        # 워크북과 워크시트 가져오기
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        # 헤더 스타일
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4F81BD',
            'font_color': 'white',
            'border': 1
        })

        # 헤더 행에 스타일 적용
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # 컬럼 너비 자동 조정
        for i, col in enumerate(df.columns):
            max_len = max(
                df[col].astype(str).map(len).max(),
                len(str(col))
            ) + 2
            worksheet.set_column(i, i, max_len)

    output.seek(0)
    return output


def dataframe_to_csv(df: pd.DataFrame) -> bytes:
    """
    DataFrame을 CSV 파일로 변환

    Args:
        df: 변환할 DataFrame

    Returns:
        bytes: CSV 파일 바이트
    """
    return df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')


def create_multi_sheet_excel(data_dict: Dict[str, pd.DataFrame]) -> BytesIO:
    """
    여러 시트를 가진 Excel 파일 생성

    Args:
        data_dict: {시트이름: DataFrame} 딕셔너리

    Returns:
        BytesIO: 메모리 내 Excel 파일

    Example:
        data = {
            "요약": summary_df,
            "거래내역": transactions_df,
            "통계": stats_df
        }
        excel_file = create_multi_sheet_excel(data)
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book

        # 공통 스타일 정의
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4F81BD',
            'font_color': 'white',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })

        number_format = workbook.add_format({
            'num_format': '#,##0.00',
            'border': 1
        })

        # 각 시트 생성
        for sheet_name, df in data_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, header=False)
            worksheet = writer.sheets[sheet_name]

            # 헤더 행 작성
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # 컬럼 너비 자동 조정
            for i, col in enumerate(df.columns):
                max_len = max(
                    df[col].astype(str).map(len).max() if len(df) > 0 else 0,
                    len(str(col))
                ) + 2
                worksheet.set_column(i, i, min(max_len, 50))  # 최대 50

            # 숫자 컬럼에 포맷 적용
            for col_idx, col in enumerate(df.columns):
                if pd.api.types.is_numeric_dtype(df[col]):
                    for row_idx in range(1, len(df) + 1):
                        worksheet.write(row_idx, col_idx, df.iloc[row_idx - 1, col_idx], number_format)

    output.seek(0)
    return output


def create_monthly_report_excel(
    summary_data: Dict,
    daily_trend_df: pd.DataFrame,
    transaction_type_df: pd.DataFrame,
    transactions_df: pd.DataFrame,
    year: int,
    month: int
) -> BytesIO:
    """
    월별 종합 리포트 Excel 파일 생성

    Args:
        summary_data: 요약 통계 딕셔너리
        daily_trend_df: 일별 추이 DataFrame
        transaction_type_df: 거래 유형별 통계 DataFrame
        transactions_df: 전체 거래 내역 DataFrame
        year: 년도
        month: 월

    Returns:
        BytesIO: 메모리 내 Excel 파일
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book

        # 스타일 정의
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#366092',
            'font_color': 'white'
        })

        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4F81BD',
            'font_color': 'white',
            'border': 1,
            'align': 'center'
        })

        metric_label_format = workbook.add_format({
            'bold': True,
            'bg_color': '#DCE6F1',
            'border': 1
        })

        metric_value_format = workbook.add_format({
            'num_format': '#,##0.00',
            'border': 1,
            'align': 'right'
        })

        # Sheet 1: 요약
        summary_sheet = workbook.add_worksheet('요약')

        # 제목
        summary_sheet.merge_range('A1:D1', f'{year}년 {month}월 로스팅 리포트', title_format)
        summary_sheet.write('A2', f'생성일: {datetime.now().strftime("%Y-%m-%d %H:%M")}')

        # 요약 통계
        summary_sheet.write('A4', '항목', header_format)
        summary_sheet.write('B4', '값', header_format)

        row = 4
        for label, value in summary_data.items():
            summary_sheet.write(row, 0, label, metric_label_format)
            summary_sheet.write(row, 1, value, metric_value_format)
            row += 1

        # 컬럼 너비 설정
        summary_sheet.set_column('A:A', 25)
        summary_sheet.set_column('B:B', 20)

        # Sheet 2: 일별 추이
        if not daily_trend_df.empty:
            daily_trend_df.to_excel(writer, sheet_name='일별 추이', index=False, startrow=1, header=False)
            worksheet = writer.sheets['일별 추이']

            # 헤더
            for col_num, value in enumerate(daily_trend_df.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # 컬럼 너비
            for i, col in enumerate(daily_trend_df.columns):
                max_len = max(
                    daily_trend_df[col].astype(str).map(len).max(),
                    len(str(col))
                ) + 2
                worksheet.set_column(i, i, max_len)

        # Sheet 3: 거래 유형별 통계
        if not transaction_type_df.empty:
            transaction_type_df.to_excel(writer, sheet_name='거래 유형별', index=False, startrow=1, header=False)
            worksheet = writer.sheets['거래 유형별']

            # 헤더
            for col_num, value in enumerate(transaction_type_df.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # 컬럼 너비
            for i, col in enumerate(transaction_type_df.columns):
                max_len = max(
                    transaction_type_df[col].astype(str).map(len).max(),
                    len(str(col))
                ) + 2
                worksheet.set_column(i, i, max_len)

        # Sheet 4: 전체 거래 내역
        if not transactions_df.empty:
            transactions_df.to_excel(writer, sheet_name='거래 내역', index=False, startrow=1, header=False)
            worksheet = writer.sheets['거래 내역']

            # 헤더
            for col_num, value in enumerate(transactions_df.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # 컬럼 너비
            for i, col in enumerate(transactions_df.columns):
                max_len = max(
                    transactions_df[col].astype(str).map(len).max(),
                    len(str(col))
                ) + 2
                worksheet.set_column(i, i, min(max_len, 40))

    output.seek(0)
    return output
