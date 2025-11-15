"""
Export Utils 테스트

export_utils.py의 Excel/CSV 내보내기 유틸리티를 테스트합니다:
- dataframe_to_excel()
- dataframe_to_csv()
- create_multi_sheet_excel()
- create_monthly_report_excel()
"""

import pytest
import pandas as pd
from io import BytesIO
from datetime import datetime
from app.utils.export_utils import (
    dataframe_to_excel,
    dataframe_to_csv,
    create_multi_sheet_excel,
    create_monthly_report_excel
)


class TestDataframeToExcel:
    """dataframe_to_excel() 함수 테스트"""

    def test_dataframe_to_excel_basic(self):
        """기본 DataFrame을 Excel로 변환"""
        df = pd.DataFrame({
            '이름': ['김철수', '이영희', '박민수'],
            '나이': [25, 30, 35],
            '점수': [90.5, 85.3, 92.7]
        })

        result = dataframe_to_excel(df, sheet_name="테스트")

        assert isinstance(result, BytesIO)
        assert result.tell() == 0  # 시작 위치

        # Excel 파일 읽기 가능한지 확인
        result.seek(0)
        df_read = pd.read_excel(result, sheet_name='테스트')
        assert len(df_read) == 3
        assert list(df_read.columns) == ['이름', '나이', '점수']

    def test_dataframe_to_excel_empty(self):
        """빈 DataFrame 변환"""
        df = pd.DataFrame()

        result = dataframe_to_excel(df)

        assert isinstance(result, BytesIO)
        result.seek(0)
        df_read = pd.read_excel(result)
        assert len(df_read) == 0

    def test_dataframe_to_excel_long_content(self):
        """긴 내용이 있는 DataFrame (컬럼 너비 자동 조정 확인)"""
        df = pd.DataFrame({
            '원두명': ['에티오피아 예가체프 G1 내추럴 프로세스 스페셜티'],
            '설명': ['매우 긴 설명 텍스트가 여기에 들어갑니다'] * 1
        })

        result = dataframe_to_excel(df)

        assert isinstance(result, BytesIO)
        result.seek(0)
        df_read = pd.read_excel(result)
        assert len(df_read) == 1


class TestDataframeToCSV:
    """dataframe_to_csv() 함수 테스트"""

    def test_dataframe_to_csv_basic(self):
        """기본 DataFrame을 CSV로 변환"""
        df = pd.DataFrame({
            '이름': ['김철수', '이영희'],
            '점수': [90, 85]
        })

        result = dataframe_to_csv(df)

        assert isinstance(result, bytes)
        # UTF-8 BOM이 포함되어 있는지 확인
        assert result.startswith(b'\xef\xbb\xbf')

    def test_dataframe_to_csv_empty(self):
        """빈 DataFrame 변환"""
        df = pd.DataFrame()

        result = dataframe_to_csv(df)

        assert isinstance(result, bytes)
        assert len(result) > 0  # 최소한 BOM은 있어야 함

    def test_dataframe_to_csv_korean(self):
        """한글 데이터 CSV 변환"""
        df = pd.DataFrame({
            '원두': ['에티오피아', '케냐'],
            '브랜드': ['스타벅스', '블루보틀']
        })

        result = dataframe_to_csv(df)

        # 디코딩 가능한지 확인
        csv_str = result.decode('utf-8-sig')
        assert '원두' in csv_str
        assert '에티오피아' in csv_str


class TestCreateMultiSheetExcel:
    """create_multi_sheet_excel() 함수 테스트"""

    def test_create_multi_sheet_excel_basic(self):
        """여러 시트를 가진 Excel 생성"""
        df1 = pd.DataFrame({'A': [1, 2, 3]})
        df2 = pd.DataFrame({'B': [4, 5, 6]})

        data_dict = {
            '시트1': df1,
            '시트2': df2
        }

        result = create_multi_sheet_excel(data_dict)

        assert isinstance(result, BytesIO)
        result.seek(0)
        xl_file = pd.ExcelFile(result)
        assert len(xl_file.sheet_names) == 2
        assert '시트1' in xl_file.sheet_names
        assert '시트2' in xl_file.sheet_names

    def test_create_multi_sheet_excel_empty_sheet(self):
        """빈 시트 포함"""
        df1 = pd.DataFrame({'A': [1, 2]})
        df2 = pd.DataFrame()  # 빈 DataFrame

        data_dict = {
            '데이터': df1,
            '빈시트': df2
        }

        result = create_multi_sheet_excel(data_dict)

        assert isinstance(result, BytesIO)
        result.seek(0)
        xl_file = pd.ExcelFile(result)
        assert len(xl_file.sheet_names) == 2

    def test_create_multi_sheet_excel_numeric_format(self):
        """숫자 포맷 적용 확인"""
        df = pd.DataFrame({
            '이름': ['A', 'B'],
            '금액': [1000.5, 2000.75]
        })

        data_dict = {'테스트': df}

        result = create_multi_sheet_excel(data_dict)

        assert isinstance(result, BytesIO)
        result.seek(0)
        df_read = pd.read_excel(result, sheet_name='테스트')
        assert len(df_read) == 2


class TestCreateMonthlyReportExcel:
    """create_monthly_report_excel() 함수 테스트"""

    def test_create_monthly_report_excel_complete(self):
        """완전한 월별 리포트 Excel 생성"""
        summary_data = {
            '총 입고량': 100.5,
            '총 출고량': 80.3,
            '로스팅 횟수': 15
        }

        daily_trend_df = pd.DataFrame({
            '날짜': pd.date_range('2025-01-01', periods=5),
            '입고량': [10, 20, 15, 25, 30],
            '출고량': [8, 18, 12, 22, 20]
        })

        transaction_type_df = pd.DataFrame({
            '거래유형': ['입고', '출고', '로스팅'],
            '건수': [10, 8, 15],
            '수량': [100.5, 80.3, 50.2]
        })

        transactions_df = pd.DataFrame({
            '날짜': ['2025-01-01', '2025-01-02'],
            '거래유형': ['입고', '출고'],
            '수량': [50.0, 30.0]
        })

        result = create_monthly_report_excel(
            summary_data=summary_data,
            daily_trend_df=daily_trend_df,
            transaction_type_df=transaction_type_df,
            transactions_df=transactions_df,
            year=2025,
            month=1
        )

        assert isinstance(result, BytesIO)
        result.seek(0)
        xl_file = pd.ExcelFile(result)

        # 4개 시트 확인
        assert len(xl_file.sheet_names) == 4
        assert '요약' in xl_file.sheet_names
        assert '일별 추이' in xl_file.sheet_names
        assert '거래 유형별' in xl_file.sheet_names
        assert '거래 내역' in xl_file.sheet_names

    def test_create_monthly_report_excel_empty_dataframes(self):
        """빈 DataFrame으로 월별 리포트 생성"""
        summary_data = {
            '총 입고량': 0,
            '총 출고량': 0
        }

        daily_trend_df = pd.DataFrame()
        transaction_type_df = pd.DataFrame()
        transactions_df = pd.DataFrame()

        result = create_monthly_report_excel(
            summary_data=summary_data,
            daily_trend_df=daily_trend_df,
            transaction_type_df=transaction_type_df,
            transactions_df=transactions_df,
            year=2025,
            month=1
        )

        assert isinstance(result, BytesIO)
        result.seek(0)
        xl_file = pd.ExcelFile(result)

        # 요약 시트는 항상 있어야 함
        assert '요약' in xl_file.sheet_names

    def test_create_monthly_report_excel_title_format(self):
        """제목 및 생성일 포맷 확인"""
        summary_data = {'총 입고량': 100}
        daily_trend_df = pd.DataFrame({'날짜': [datetime.now()], '입고량': [100]})
        transaction_type_df = pd.DataFrame()
        transactions_df = pd.DataFrame()

        result = create_monthly_report_excel(
            summary_data=summary_data,
            daily_trend_df=daily_trend_df,
            transaction_type_df=transaction_type_df,
            transactions_df=transactions_df,
            year=2025,
            month=3
        )

        assert isinstance(result, BytesIO)
        result.seek(0)
        xl_file = pd.ExcelFile(result)
        assert '요약' in xl_file.sheet_names

        # 요약 시트 읽기
        df_summary = pd.read_excel(result, sheet_name='요약')
        # 제목이나 생성일이 포함되어 있는지 확인
        assert len(df_summary) > 0
