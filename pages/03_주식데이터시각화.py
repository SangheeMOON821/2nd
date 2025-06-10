import streamlit as st
import yfinance as yf
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# 찜한 주식 저장용 (세션 상태)
if "favorites" not in st.session_state:
    st.session_state.favorites = set()

st.title("🌍 글로벌 주식 분석 앱")
st.subheader("📈 최근 3년 주가 동향 및 성장 가능성 분석")

# 날짜 설정 (최근 3년)
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365 * 3)

# 주식 검색
ticker_input = st.text_input("🔍 주식 티커를 입력하세요 (예: AAPL, TSLA, MSFT, NVDA 등):")

if ticker_input:
    try:
        stock = yf.Ticker(ticker_input)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            st.warning("유효한 주식 티커를 입력해주세요.")
        else:
            # 주가 그래프
            st.line_chart(hist['Close'], use_container_width=True)

            # 성장성 간단 분석
            recent = hist['Close'][-1]
            past = hist['Close'][0]
            growth = (recent - past) / past * 100

            st.metric(label="📊 3년간 주가 성장률", value=f"{growth:.2f}%")
            if growth > 100:
                st.success("✅ 높은 성장 가능성이 있습니다!")
            elif growth > 30:
                st.info("🔄 안정적인 성장세를 보이고 있습니다.")
            else:
                st.warning("📉 성장률이 낮거나 정체 상태입니다.")

            # 찜하기
            if st.button("⭐ 찜하기"):
                st.session_state.favorites.add(ticker_input.upper())
                st.success(f"{ticker_input.upper()}가 찜 목록에 추가되었습니다!")

    except Exception as e:
        st.error(f"에러 발생: {e}")

# 찜한 주식 비교
if st.session_state.favorites:
    st.subheader("📌 찜한 주식 비교")

    selected_favs = st.multiselect("비교할 주식 선택", list(st.session_state.favorites), default=list(st.session_state.favorites))
    
    if selected_favs:
        st.write("📉 주가 비교 차트 (최근 3년)")
        compare_df = pd.DataFrame()

        for fav in selected_favs:
            fav_data = yf.Ticker(fav).history(start=start_date, end=end_date)
            compare_df[fav] = fav_data['Close']

        st.line_chart(compare_df)

        st.write("📈 각 주식의 3년 성장률")
        for fav in selected_favs:
            fav_data = compare_df[fav].dropna()
            if len(fav_data) > 1:
                growth = (fav_data.iloc[-1] - fav_data.iloc[0]) / fav_data.iloc[0] * 100
                st.write(f"**{fav}**: {growth:.2f}%")
    else:
        st.info("비교할 주식을 선택해주세요.")

else:
    st.info("아직 찜한 주식이 없습니다.")

