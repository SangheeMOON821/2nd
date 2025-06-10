import streamlit as st
import yfinance as yf
import datetime
import pandas as pd

st.set_page_config(page_title="글로벌 시가총액 Top10 비교", layout="wide")

st.title("🌐 글로벌 시가총액 Top10 기업 주가 분석")
st.caption("최근 3년간 주가 변화 시각화 및 성장 가능성 분석")

# 시가총액 상위 10개 기업 티커
top10_tickers = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "NVIDIA (NVDA)": "NVDA",
    "Amazon (AMZN)": "AMZN",
    "Alphabet (GOOGL)": "GOOGL",
    "Meta (META)": "META",
    "Berkshire Hathaway (BRK-B)": "BRK-B",
    "TSMC (TSM)": "TSM",
    "Eli Lilly (LLY)": "LLY",
    "JPMorgan Chase (JPM)": "JPM"
}

# 찜한 종목 저장
if "favorites" not in st.session_state:
    st.session_state.favorites = set()

# 기간 설정
end = datetime.date.today()
start = end - datetime.timedelta(days=365*3)

# 주가 데이터 가져오기
@st.cache_data(ttl=3600)
def load_data(ticker):
    return yf.Ticker(ticker).history(start=start, end=end)['Close']

# --- 1. 기업 선택 및 분석 ---
st.subheader("📌 기업 선택 및 개별 분석")

col1, col2 = st.columns([2, 1])

with col1:
    selected = st.selectbox("🔍 분석할 기업을 선택하세요:", list(top10_tickers.keys()))

with col2:
    if st.button("⭐ 찜하기"):
        st.session_state.favorites.add(selected)
        st.success(f"{selected}를 찜했습니다!")

# 주가 데이터 로드 및 시각화
if selected:
    ticker = top10_tickers[selected]
    series = load_data(ticker)

    st.line_chart(series)

    # 성장 분석
    growth = (series.iloc[-1] - series.iloc[0]) / series.iloc[0] * 100
    st.metric("📈 최근 3년 수익률", f"{growth:.2f}%")

    if growth > 150:
        st.success("✅ 매우 높은 성장률로, 강력한 성장 가능성이 보입니다!")
    elif growth > 50:
        st.info("📊 안정적인 성장세입니다.")
    else:
        st.warning("📉 성장률이 낮아, 향후 주의가 필요합니다.")

# --- 2. 찜한 주식 비교 ---
st.divider()
st.subheader("📂 찜한 주식 비교")

if st.session_state.favorites:
    selected_favs = st.multiselect("📌 비교할 찜한 주식을 선택하세요:", list(st.session_state.favorites), default=list(st.session_state.favorites))

    if selected_favs:
        compare_df = pd.DataFrame()
        for fav_name in selected_favs:
            ticker = top10_tickers[fav_name]
            series = load_data(ticker)
            compare_df[fav_name] = series

        # 정규화
        norm_df = compare_df.divide(compare_df.iloc[0]).multiply(100)
        st.line_chart(norm_df)

        # 수익률 테이블
        st.markdown("📊 **3년간 수익률 요약**")
        for name in selected_favs:
            series = compare_df[name].dropna()
            if not series.empty:
                growth = (series.iloc[-1] - series.iloc[0]) / series.iloc[0] * 100
                st.write(f"**{name}**: {growth:.2f}%")

        # 찜 제거 기능 (선택적)
        if st.button("🗑️ 찜한 종목 초기화"):
            st.session_state.favorites.clear()
            st.success("찜한 종목이 모두 삭제되었습니다.")
    else:
        st.info("비교할 종목을 하나 이상 선택해주세요.")
else:
    st.info("아직 찜한 종목이 없습니다.")
