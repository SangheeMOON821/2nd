import streamlit as st
import yfinance as yf
import datetime
import pandas as pd

# 페이지 제목
st.title("🌐 글로벌 시가총액 Top 10 기업 - 3년간 주가 비교")

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

# 사용자 선택 (다중)
selected = st.multiselect("📌 비교할 기업을 선택하세요:", list(top10_tickers.keys()), default=list(top10_tickers.keys())[:5])

# 날짜 범위: 최근 3년
end = datetime.date.today()
start = end - datetime.timedelta(days=365*3)

# 주가 데이터 로딩
@st.cache_data(ttl=3600)
def load_data(ticker):
    return yf.Ticker(ticker).history(start=start, end=end)['Close']

# 데이터프레임 병합
if selected:
    st.subheader("📈 주가 비교 차트 (최근 3년)")

    compare_df = pd.DataFrame()
    for name in selected:
        ticker = top10_tickers[name]
        series = load_data(ticker)
        compare_df[name] = series

    # 정규화 (처음 값 대비 % 변화로 비교)
    norm_df = compare_df.divide(compare_df.iloc[0]).multiply(100)

    st.line_chart(norm_df)

    st.subheader("📊 3년간 수익률 정리")
    for name in selected:
        growth = (compare_df[name].iloc[-1] - compare_df[name].iloc[0]) / compare_df[name].iloc[0] * 100
        st.write(f"**{name}**: {growth:.2f}%")
else:
    st.info("비교할 기업을 하나 이상 선택해주세요.")
