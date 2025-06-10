import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 페이지 설정 ---
st.set_page_config(page_title="글로벌 주가 분석", layout="wide", initial_sidebar_state="expanded")

# --- 데이터 캐싱 및 로딩 함수 (오류 수정) ---
@st.cache_data
def load_data(tickers, start, end):
    """
    선택된 티커들의 주가 데이터를 yfinance를 통해 다운로드하고, 수익률을 계산합니다.
    KeyError를 해결하기 위해 데이터 다운로드 후 'Adj Close' 컬럼을 안전하게 추출합니다.
    """
    # 1. 모든 티커의 데이터를 한번에 다운로드합니다.
    full_data = yf.download(tickers, start=start, end=end)
    
    if full_data.empty:
        st.error(f"선택된 기간에 '{', '.join(tickers)}'에 대한 데이터를 가져올 수 없습니다.")
        return None, None

    # 2. 'Adj Close' 데이터만 안전하게 선택합니다.
    # 여러 티커: 컬럼이 MultiIndex -> ('Adj Close', 'MSFT'), ('Close', 'MSFT'), ...
    # 단일 티커: 컬럼이 평탄화 -> 'Open', 'High', 'Close', 'Adj Close', ...
    if isinstance(full_data.columns, pd.MultiIndex):
        adj_close_data = full_data['Adj Close']
    else:
        # 단일 티커일 경우, 일관된 처리를 위해 DataFrame 형태로 유지합니다.
        adj_close_data = full_data[['Adj Close']]
        # 컬럼 이름을 티커로 변경합니다.
        adj_close_data.columns = tickers if isinstance(tickers, list) and len(tickers) == 1 else [tickers]


    # 데이터가 없는 티커(컬럼)는 제거합니다.
    adj_close_data = adj_close_data.dropna(axis=1, how='all')

    if adj_close_data.empty:
        st.error(f"유효한 'Adj Close' 데이터를 찾을 수 없습니다.")
        return None, None

    # 3. 수익률 계산 (첫 날 가격을 100으로 정규화)
    # 계산 전, 휴일 등으로 인한 NaN 값을 바로 앞 데이터로 채웁니다 (forward fill).
    normalized_data = (adj_close_data.ffill() / adj_close_data.ffill().iloc[0] * 100)
    
    return adj_close_data, normalized_data

# --- 사이드바 설정 ---
with st.sidebar:
    st.title("⚙️ 분석 설정")
    
    # 최신 시가총액 순위 (2024년 기준)
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
    
    selected_companies = st.multiselect(
        "📌 기업 선택:",
        options=list(companies.keys()),
        default=["Microsoft (MSFT)", "Apple (AAPL)", "Nvidia (NVDA)", "Alphabet (GOOGL)", "Amazon (AMZN)"]
    )
    
    st.markdown("---")
    st.markdown("#### 🗓️ 기간 선택")
    col1, col2 = st.columns(2)
    start_date = col1.date_input("시작일", datetime.today() - timedelta(days=3*365))
    end_date = col2.date_input("종료일", datetime.today())

    st.markdown("---")
    chart_type = st.radio(
        "📊 차트 타입 선택",
        ('수익률(%) 비교', '실제 주가(USD) 보기'),
        horizontal=True,
        key='chart_type_radio'
    )

# --- 메인 페이지 ---
st.title("🚀 글로벌 Top 10 기업 주가 대시보드")
st.markdown(f"**선택된 기간:** `{start_date}` ~ `{end_date}`")

if not selected_companies:
    st.warning("사이드바에서 최소 한 개 이상의 기업을 선택해주세요.")
else:
    selected_tickers = [companies[name] for name in selected_companies]
    raw_data, normalized_data = load_data(selected_tickers, start_date, end_date)

    if raw_data is not None and not raw_data.empty:
        chart_data = normalized_data if chart_type == '수익률(%) 비교' else raw_data
        y_axis_title = f"수익률 (%, {start_date} 기준 100)" if chart_type == '수익률(%) 비교' else "조정 종가 (USD)"
        title = "기간별 주가 수익률 변화" if chart_type == '수익률(%) 비교' else "기간별 실제 주가(Adj Close) 변화"

        fig = go.Figure()
        
        # 실제 데이터가 있는 기업만 차트에 추가
        valid_companies = {name: ticker for name, ticker in companies.items() if ticker in chart_data.columns}

        for name, ticker in valid_companies.items():
             if name in selected_companies: # 사용자가 선택한 기업인지 다시 확인
                fig.add_trace(go.Scatter(
                    x=chart_data.index, 
                    y=chart_data[ticker], 
                    mode='lines', 
                    name=name
                ))
        
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

        st.markdown("---")
        st.subheader("📈 요약 및 데이터")

        summary_data = []
        for name, ticker in valid_companies.items():
            if name in selected_companies and not raw_data[ticker].dropna().empty:
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
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data).set_index("기업명")
            st.dataframe(summary_df, use_container_width=True)

        tab1, tab2 = st.tabs(["실제 주가 데이터 (USD)", "수익률 데이터 (%)"])
        with tab1:
            st.dataframe(raw_data.style.format("${:,.2f}", na_rep="-"), use_container_width=True)
        with tab2:
            st.dataframe(normalized_data.style.format("{:,.2f}", na_rep="-"), use_container_width=True)
