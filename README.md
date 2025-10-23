# 🎰 Lotto AI WebApp Project

AI 기반 로또 6/45 번호 예측 시스템

## 🚀 주요 기능

### AI 예측 모델
- **LSTM**: 시계열 패턴 학습을 통한 번호 예측
- **Transformer**: 어텐션 메커니즘 기반 딥러닝 예측
- **Prophet**: Facebook의 시계열 예측 라이브러리
- **Ensemble**: 3개 모델의 앙상블 예측

### 데이터 분석
- 1,193회차 실제 로또 데이터 분석
- Hot/Cold 번호 분석
- 홀짝 분포, 구간별 통계
- Chart.js 기반 인터랙티브 시각화

### 고급 기능
- **성능 모니터링**: 모델 예측 정확도 추적
- **A/B 테스트**: 다양한 모델 조합 비교
- **실시간 학습**: 새로운 데이터로 모델 자동 업데이트
- **사용자 피드백**: 평점 및 코멘트 시스템
- **하이퍼파라미터 튜닝**: 자동 모델 최적화

## 🏗️ 아키텍처

### 디자인 시스템
- **Linear Design System** 기반 UI 컴포넌트
- 반응형 디자인 지원
- 다크/라이트 테마

### 기술 스택
- **Frontend**: Streamlit + Linear Design System
- **Backend**: Python + SQLite
- **AI/ML**: TensorFlow, PyTorch, Prophet
- **Visualization**: Chart.js
- **Database**: SQLite

## 📁 프로젝트 구조

```
Lotto_AI_WebApp_ProJect/
├── app/
│   ├── main.py                 # 메인 애플리케이션
│   └── data/
│       └── lotto.db           # SQLite 데이터베이스
├── components/
│   ├── linear_design/         # Linear Design System 컴포넌트
│   │   ├── __init__.py
│   │   ├── container.py
│   │   ├── section.py
│   │   ├── panel.py
│   │   ├── button.py
│   │   ├── grid.py
│   │   ├── spacer.py
│   │   ├── divider.py
│   │   ├── card.py
│   │   ├── badge.py
│   │   └── alert.py
│   └── chart_js.py            # Chart.js 컴포넌트
├── modules/
│   ├── lotto/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── lstm_predictor.py
│   │   │   ├── transformer_predictor.py
│   │   │   ├── prophet_predictor.py
│   │   │   └── ensemble_predictor.py
│   │   ├── model_manager.py
│   │   ├── performance_monitor.py
│   │   ├── hyperparameter_tuner.py
│   │   ├── realtime_learner.py
│   │   ├── ab_testing.py
│   │   └── user_feedback.py
│   └── settings/
│       ├── __init__.py
│       ├── auth.py
│       ├── database.py
│       └── admin.py
├── requirements.txt
├── .cursorrules              # Cursor IDE 규칙
└── README.md
```

## 🛠️ 설치 및 실행

### 1. 가상환경 설정
```bash
# 가상환경 활성화 (WSL/Linux)
source ~/venv/bin/activate

# 가상환경 활성화 (Windows Git Bash)
source ~/venv/Scripts/activate
```

### 2. 의존성 설치
```bash
# 프로젝트 디렉토리로 이동
cd Lotto_AI_WebApp_ProJect

# 의존성 설치
pip install -r requirements.txt
```

### 3. 애플리케이션 실행
```bash
# Streamlit 서버 실행
streamlit run app/main.py --server.port 8501
```

### 4. 브라우저에서 접속
```
http://localhost:8501
```

### 5. Git 업데이트 후 실행
```bash
# 가상환경 활성화
source ~/venv/bin/activate

# 프로젝트 업데이트
git pull origin main

# 의존성 재설치 (필요시)
pip install -r requirements.txt

# 애플리케이션 실행
streamlit run app/main.py --server.port 8501
```

## 📖 컴포넌트 사용법

### Linear Design System 컴포넌트

```python
from components.linear_design import (
    Container, Section, Panel, Button, Grid, 
    Spacer, Divider, Card, Badge, Alert
)

# 기본 레이아웃
with Container.render(max_width="1400px", padding="xl"):
    with Section.render("제목", "설명"):
        with Panel.render("패널 제목", padding="xl", elevation="dialog"):
            # 내용
```

### AI 모델 사용

```python
from modules.lotto import ModelManager

# 모델 매니저 생성
manager = ModelManager(db_path="app/data/lotto.db")

# 예측 실행
lstm_pred = manager.predict_lstm(top_k=6)
transformer_pred = manager.predict_transformer(top_k=6)
prophet_pred = manager.predict_prophet(top_k=6)
ensemble_pred = manager.predict_ensemble(top_k=6)
```

### 차트 컴포넌트

```python
from components.chart_js import (
    render_frequency_chart,
    render_odd_even_chart,
    render_sum_trend_chart
)

# 빈도 분석 차트
chart_html = render_frequency_chart(freq_dist, "번호별 출현 빈도")
st.components.v1.html(chart_html, height=500)
```

### 성능 모니터링

```python
from modules.lotto.performance_monitor import PerformanceMonitor

# 성능 모니터 생성
monitor = PerformanceMonitor(db_path="app/data/lotto.db")

# 예측 결과 기록
record_id = monitor.record_prediction('LSTM', predicted_numbers)

# 실제 결과 업데이트
monitor.update_actual_results(record_id, actual_numbers)

# 성능 조회
performance = monitor.get_model_performance('LSTM', days=30)
```

### A/B 테스트

```python
from modules.lotto.ab_testing import ABTestManager, create_ensemble_weight_test

# A/B 테스트 매니저 생성
ab_manager = ABTestManager(db_path="app/data/lotto.db")

# 앙상블 가중치 테스트 생성
test = create_ensemble_weight_test(db_path="app/data/lotto.db")
test.start_test(duration_days=7)

# 사용자 할당
variant = test.assign_user_to_variant(user_id)
config = test.get_variant_config(user_id)
```

### 사용자 피드백

```python
from modules.lotto.user_feedback import UserFeedbackManager, FeedbackType

# 피드백 매니저 생성
feedback_manager = UserFeedbackManager(db_path="app/data/lotto.db")

# 평점 제출
feedback_manager.submit_feedback(
    user_id="user123",
    model_name="LSTM",
    feedback_type=FeedbackType.RATING,
    rating_value=4
)

# 코멘트 제출
feedback_manager.submit_feedback(
    user_id="user123",
    model_name="LSTM",
    feedback_type=FeedbackType.COMMENT,
    text_content="예측이 정확해서 좋습니다!"
)
```

## 🎯 주요 페이지

### 1. 홈페이지
- 프로젝트 소개
- 실시간 통계
- 주요 기능 안내

### 2. AI 예측
- 4가지 AI 모델 예측
- 예측 결과 저장
- 사용자 피드백

### 3. 데이터 분석
- Hot/Cold 번호 분석
- 통계 시각화
- Chart.js 차트

### 4. 통계
- 종합 통계 보고서
- 데이터 다운로드

### 5. 관리자 페이지 (관리자만)
- 사용자 관리
- 데이터 관리
- 시스템 설정

### 6. 성능 모니터링 (관리자만)
- 모델 성능 추적
- 성능 순위
- 보고서 생성

### 7. A/B 테스트 (관리자만)
- 테스트 생성 및 관리
- 통계적 유의성 분석
- 승자 결정

### 8. 사용자 피드백 (관리자만)
- 피드백 분석
- 감정 분석
- 인사이트 생성

## 🔧 개발 가이드

### 코딩 규칙
- `.cursorrules` 파일 참조
- Linear Design System 컴포넌트 필수 사용
- 적절한 에러 처리 및 로깅
- 사용자 인증 확인

### 데이터베이스 스키마
```sql
-- 사용자 테이블
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(20) DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 로또 당첨 번호 테이블
CREATE TABLE lotto_draws (
    draw_no INTEGER PRIMARY KEY,
    draw_date DATE,
    num1 INTEGER, num2 INTEGER, num3 INTEGER,
    num4 INTEGER, num5 INTEGER, num6 INTEGER,
    bonus INTEGER
);

-- AI 모델 테이블
CREATE TABLE ai_models (
    id INTEGER PRIMARY KEY,
    model_name VARCHAR(50),
    model_type VARCHAR(20),
    model_weights BLOB,
    model_config TEXT,
    training_metrics TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

## 📊 성능 지표

### 모델 성능
- **LSTM**: 시계열 패턴 학습 특화
- **Transformer**: 어텐션 메커니즘 기반 예측
- **Prophet**: 시계열 트렌드 분석
- **Ensemble**: 3개 모델 앙상블 (LSTM: 0.4, Transformer: 0.4, Prophet: 0.2)

### 데이터 규모
- **총 회차**: 1,193회차
- **데이터 기간**: 2002년 12월 ~ 2024년 12월
- **데이터베이스 크기**: 약 2MB

## 🚀 향후 계획

1. **모델 개선**
   - 새로운 AI 모델 추가
   - 앙상블 가중치 최적화
   - 실시간 학습 강화

2. **기능 확장**
   - 개인화된 추천 시스템
   - 모바일 앱 개발
   - API 서비스 제공

3. **성능 최적화**
   - 모델 학습 속도 개선
   - 예측 정확도 향상
   - 사용자 경험 개선

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 문의

- **Email**: support@lotto-ai.com
- **Version**: 2.0.0
- **Last Updated**: 2025년 1월

---

**🎰 Lotto AI Prediction System | Made with Linear Design System & Streamlit**