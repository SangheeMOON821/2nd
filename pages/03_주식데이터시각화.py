import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="글로벌 시총 Top10 주가 추이", layout="wide")
st.title("📈 글로벌 시총 Top10 기업의 최근 3년 주가 변화")

# 시가총액 기준 글로벌 Top 10 기업 (2025년 기준 추정)
companies = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Saudi Aramco (2222.SR)": "2222.SR",
    "Alphabet (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Nvidia (NVDA)": "NVDA",
    "Meta (META)": "META",
    "Berkshire Hathaway (BRK-B)": "BRK-B",
    "TSMC (TSM)": "TSM",
    "Tesla (TSLA)": "TSLA"
}

# 기간 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=3*365)

# 사용자 선택
selected_companies = st.multiselect(
    "📌 비교할 회사를 선택하세요:",
    list(companies.keys()),
    default=list(companies.keys())[:5]
)

if selected_companies:
    fig = go.Figure()

    for name in selected_companies:
        ticker = companies[name]
        data = yf.download(ticker, start=start_date, end=end_date)
        fig.add_trace(go.Scatter(x=data.index, y=data["Adj Close"], mode="lines", name=name))

    fig.update_layout(
        title="최근 3년간 주가(Adjusted Close) 추이",
        xaxis_title="날짜",
        yaxis_title="주가 (USD)",
        hovermode="x unified",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("최소 한 개의 회사를 선택해주세요.")
