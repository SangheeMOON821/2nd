import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="글로벌 주가 분석 및 찜", layout="wide", initial_sidebar_state="expanded")
st.title("📈 글로벌 주가 분석 및 찜하기")

# --- 세션 상태 초기화 ---
if 'favorite_stocks' not in st.session_state:
    st.session_state['favorite_stocks'] = []

# --- 데이터 캐싱 함수 ---
@st.cache_data(ttl=3600)
def load_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end_date=end_date)
    return data

# --- 성장 가능성 분석 (간단한 추세 분석) ---
def analyze_growth_potential(data):
    if data is None or data.empty:
        return "데이터가 없습니다."

    recent_return = (data['Adj Close'].iloc[-1] / data['Adj Close'].iloc[-30] - 1) * 100 if len(data) > 30 else 0
    one_year_return = (data['Adj Close'].iloc[-1] / data['Adj Close'].iloc[-252] - 1) * 100 if len(data) > 252 else 0
    volatility = data['Adj Close'].pct_change().rolling(window=30).std().iloc[-1] * (252**0.5) if len(data) > 30 else 0

    analysis = f"**최근 1개월 수익률:** {recent_return:.2f}%\n\n"
    analysis += f"**최근 1년 수익률:** {one_year_return:.2f}%\n\n"
    analysis += f"**최근 변동성 (30일 기준, 연율화):** {volatility:.2f}"

    if recent_return > 0 and one_year_return > 0:
        analysis += "\n\n최근 추세는 긍정적으로 보입니다."
    elif recent_return < 0 and one_year_return < 0:
        analysis += "\n\n최근 추세는 다소 약세입니다."
    else:
        analysis += "\n\n추세가 혼조세를 보이고 있습니다."

    return analysis

# --- 주가 시각화 함수 ---
def plot_stock_price(data, title):
    if data is None or data.empty:
        st.warning(f"{title}에 대한 데이터가 없습니다.")
        return

    fig = go.Figure(data=[go.Scatter(x=data.index, y=data['Adj Close'], mode='lines')])
    fig.update_layout(title=title, xaxis_title="날짜", yaxis_title="조정 종가 (USD)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- 글로벌 시총 Top 10 기업 목록 (최신 정보로 업데이트 필요) ---
top_10_companies = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Nvidia (NVDA)": "NVDA",
    "Alphabet (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Meta (META)": "META",
    "TSMC (TSM)": "TSM",
    "Berkshire Hathaway (BRK-B)": "BRK-B",
    "Eli Lilly (LLY)": "LLY",
    "Broadcom (AVGO)": "AVGO"
}

end_date = datetime.today()
start_date = end_date - timedelta(days=3 * 365)

# --- 사이드바: 기업 선택 및 검색 ---
with st.sidebar:
    st.header("⚙️ 설정")
    selected_top10 = st.multiselect("글로벌 Top 10 기업", list(top_10_companies.keys()), default=list(top_10_companies.keys())[:5])

    st.subheader("🔍 주식 검색")
    search_ticker = st.text_input("티커 심볼을 입력하세요 (예: TSLA, 삼성전자: 005930.KS)")
    search_button = st.button("검색")

    st.subheader("⭐ 찜한 주식")
    if st.session_state['favorite_stocks']:
        st.write(", ".join(st.session_state['favorite_stocks']))
        if st.button("찜 목록 비교"):
            st.session_state['compare_favorites'] = True
        else:
            st.session_state['compare_favorites'] = False
    else:
        st.write("찜한 주식이 없습니다.")

# --- 메인 영역: Top 10 기업 주가 시각화 ---
st.header("📈 글로벌 Top 10 기업 최근 3년 주가 추이")
for company_name in selected_top10:
    ticker = top_10_companies.get(company_name)
    if ticker:
        data = load_stock_data(ticker, start_date, end_date)
        plot_stock_price(data, f"{company_name} ({ticker}) 최근 3년 주가")

# --- 메인 영역: 주식 검색 및 찜 기능 ---
st.header("🔎 주식 검색 및 분석")
if search_button and search_ticker:
    ticker = search_ticker.upper()
    searched_data = load_stock_data(ticker, start_date, end_date)
    st.subheader(f"🔍 검색 결과: {ticker}")
    plot_stock_price(searched_data, f"{ticker} 최근 3년 주가")

    st.subheader("💡 성장 가능성 분석 (간단)")
    analysis_result = analyze_growth_potential(searched_data)
    st.markdown(analysis_result)

    if ticker not in st.session_state['favorite_stocks']:
        if st.button("⭐ 찜하기"):
            st.session_state['favorite_stocks'].append(ticker)
            st.toast(f"{ticker}을(를) 찜 목록에 추가했습니다.")
    else:
        if st.button("💔 찜 해제"):
            st.session_state['favorite_stocks'].remove(ticker)
            st.toast(f"{ticker}을(를) 찜 목록에서 제거했습니다.")

# --- 메인 영역: 찜한 주식 비교 ---
if st.session_state.get('compare_favorites'):
    st.header("📊 찜한 주식 비교")
    if st.session_state['favorite_stocks']:
        compare_data = {}
        for ticker in st.session_state['favorite_stocks']:
            data = load_stock_data(ticker, start_date, end_date)
            if data is not None and not data.empty:
                compare_data.update({ticker: data['Adj Close']})

        if compare_data:
            compare_df = pd.DataFrame(compare_data)
            fig_compare = go.Figure()
            for ticker, prices in compare_df.items():
                fig_compare.add_trace(go.Scatter(x=prices.index, y=prices, mode='lines', name=ticker))
            fig_compare.update_layout(title="찜한 주식 주가 비교", xaxis_title="날짜", yaxis_title="조정 종가 (USD)", template="plotly_dark")
            st.plotly_chart(fig_compare, use_container_width=True)
        else:
            st.warning("찜한 주식의 데이터를 불러올 수 없습니다.")
    else:
        st.info("찜한 주식이 없습니다.")
