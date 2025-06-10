import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 페이지 설정 ---
st.set_page_config(page_title="글로벌 주가 분석", layout="wide", initial_sidebar_state="expanded")

# --- 데이터 캐싱을 위한 함수 ---
# st.cache_data: 데이터 로딩 함수를 캐싱하여 성능 향상
@st.cache_data
def load_data(tickers, start, end):
    """
    선택된 티커들의 주가 데이터를 yfinance를 통해 다운로드하고, 수익률을 계산합니다.
    """
    # yfinance는 여러 티커를 한번에 다운로드 가능
    data = yf.download(tickers, start=start, end=end)['Adj Close']
    if data.empty:
        return None, None
    
    # 데이터가 단일 티커에 대한 Series일 경우 DataFrame으로 변환
    if isinstance(data, pd.Series):
        data = data.to_frame(tickers[0])

    # 수익률 계산 (첫 날 가격을 100으로 정규화)
    normalized_data = (data / data.iloc[0] * 100)
    return data, normalized_data

# --- 사이드바 설정 ---
with st.sidebar:
    st.title("⚙️ 분석 설정")
    
    # 최신 시가총액 순위 (2024년 6월 기준)
    # 사우디 아람코(2222.SR)는 데이터 접근성 문제로 제외하고, 대안으로 Eli Lilly(LLY) 포함
    companies = {
        "Microsoft (MSFT)": "MSFT",
        "Apple (AAPL)": "AAPL",
        "Nvidia (NVDA)": "NVDA",
        "Alphabet (GOOGL)": "GOOGL",
        "Amazon (AMZN)": "AMZN",
        "Meta (META)": "META",
        "TSMC (TSM)": "TSM",
        "Berkshire Hathaway (BRK-B)": "BRK-B",
        "Eli Lilly (LLY)": "LLY",
        "Broadcom (AVGO)": "AVGO"
    }
    
    # 멀티셀렉트 박스
    selected_companies = st.multiselect(
        "📌 기업 선택:",
        options=list(companies.keys()),
        default=["Microsoft (MSFT)", "Apple (AAPL)", "Nvidia (NVDA)", "Alphabet (GOOGL)", "Amazon (AMZN)"]
    )
    
    # 날짜 범위 선택
    st.markdown("---")
    st.markdown("#### 🗓️ 기간 선택")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("시작일", datetime.today() - timedelta(days=3*365))
    with col2:
        end_date = st.date_input("종료일", datetime.today())

    # 차트 타입 선택
    st.markdown("---")
    chart_type = st.radio(
        "📊 차트 타입 선택",
        ('수익률(%) 비교', '실제 주가(USD) 보기'),
        horizontal=True
    )

# --- 메인 페이지 ---
st.title("🚀 글로벌 Top 10 기업 주가 대시보드")
st.markdown(f"**선택된 기간:** `{start_date}` ~ `{end_date}`")

if not selected_companies:
    st.warning("사이드바에서 최소 한 개 이상의 기업을 선택해주세요.")
else:
    # 선택된 회사의 티커 목록 생성
    selected_tickers = [companies[name] for name in selected_companies]
    
    # 데이터 로딩
    raw_data, normalized_data = load_data(selected_tickers, start_date, end_date)

    if raw_data is None:
        st.error("데이터를 불러오는 데 실패했습니다. 티커나 기간을 다시 확인해주세요.")
    else:
        # 선택된 차트 타입에 따라 데이터와 제목, y축 레이블 결정
        if chart_type == '수익률(%) 비교':
            chart_data = normalized_data
            y_axis_title = f"수익률 (%, {start_date} 기준 100)"
            title = "기간별 주가 수익률 변화"
        else:
            chart_data = raw_data
            y_axis_title = "조정 종가 (USD)"
            title = "기간별 실제 주가(Adj Close) 변화"

        # Plotly 차트 생성
        fig = go.Figure()
        for company_name in selected_companies:
            ticker = companies[company_name]
            # 컬럼 이름이 MultiIndex일 경우와 단일 인덱스일 경우 모두 처리
            if ticker in chart_data.columns:
                fig.add_trace(go.Scatter(
                    x=chart_data.index, 
                    y=chart_data[ticker], 
                    mode='lines', 
                    name=company_name
                ))
        
        # 차트 레이아웃 업데이트
        fig.update_layout(
            title={'text': f'<b>{title}</b>', 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
            xaxis_title="날짜",
            yaxis_title=y_axis_title,
            legend_title="기업명",
            hovermode="x unified",
            template="plotly_dark",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- 요약 지표 및 데이터 테이블 ---
        st.markdown("---")
        st.subheader("📈 요약 및 데이터")

        # 기간 내 수익률 및 주요 지표 계산
        summary_data = []
        for name in selected_companies:
            ticker = companies[name]
            if ticker in raw_data.columns:
                start_price = raw_data[ticker].dropna().iloc[0]
                end_price = raw_data[ticker].dropna().iloc[-1]
                period_return = (end_price / start_price - 1) * 100
                max_price = raw_data[ticker].max()
                min_price = raw_data[ticker].min()
                summary_data.append({
                    "기업명": name,
                    "기간 내 수익률(%)": f"{period_return:.2f}%",
                    "시작 가격(USD)": f"${start_price:.2f}",
                    "종료 가격(USD)": f"${end_price:.2f}",
                    "최고가(USD)": f"${max_price:.2f}",
                    "최저가(USD)": f"${min_price:.2f}"
                })
        
        summary_df = pd.DataFrame(summary_data).set_index("기업명")
        st.dataframe(summary_df, use_container_width=True)

        # 탭을 사용하여 원본 데이터와 정규화된 데이터 표시
        tab1, tab2 = st.tabs(["실제 주가 데이터 (USD)", "수익률 데이터 (%)"])
        with tab1:
            st.dataframe(raw_data.style.format("{:.2f}"), use_container_width=True)
        with tab2:
            st.dataframe(normalized_data.style.format("{:.2f}"), use_container_width=True)
