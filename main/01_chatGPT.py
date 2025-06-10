import streamlit as st
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide")

# 관광지 데이터 (예시)
tourist_spots = {
    "에펠탑": {"lat": 48.8584, "lon": 2.2945, "description": "파리의 상징, 낭만적인 야경을 자랑합니다."},
    "루브르 박물관": {"lat": 48.8606, "lon": 2.3376, "description": "세계 3대 박물관 중 하나로 모나리자가 있습니다."},
    "몽생미셸": {"lat": 48.6361, "lon": -1.5118, "description": "신비로운 섬 위에 지어진 수도원입니다."},
    # ... 더 많은 관광지 추가
}

st.title("🇫🇷 프랑스 주요 관광지 친절 가이드")
st.write("프랑스 여행을 위한 최고의 가이드입니다. 프랑스의 아름다운 명소들을 함께 탐험해 보세요!")

# 지도 생성
m = folium.Map(location=[46.603354, 1.888334], zoom_start=6) # 프랑스 중심 좌표

# 관광지 마커 추가
for spot_name, data in tourist_spots.items():
    folium.Marker(
        location=[data["lat"], data["lon"]],
        popup=f"<b>{spot_name}</b><br>{data['description']}",
        tooltip=spot_name
    ).add_to(m)

st.header("✨ 프랑스 주요 관광지 지도")
folium_static(m, width=1000, height=600)

st.header("🗼 파리 (Paris)")
st.write("세계에서 가장 로맨틱하고 예술적인 도시, 파리입니다.")

st.subheader("에펠탑 (Eiffel Tower)")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Eiffel_Tower_from_Champs_de_Mars.jpg/800px-Eiffel_Tower_from_Champs_de_Mars.jpg", caption="에펠탑의 웅장한 모습", width=600)
st.write("""
    1889년 만국 박람회를 기념하여 귀스타브 에펠이 건설한 철골 구조물입니다. 
    파리의 상징이자 랜드마크로, 낮과 밤 언제 방문해도 아름다운 풍경을 선사합니다.
    **방문 팁:** 저녁에는 5분간 반짝이는 에펠탑 야경을 놓치지 마세요! 미리 온라인으로 티켓을 예매하면 대기 시간을 줄일 수 있습니다.
""")

st.subheader("루브르 박물관 (Louvre Museum)")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Pyramide_du_Louvre_et_aile_Richelieu.jpg/800px-Pyramide_du_Louvre_et_aile_Richelieu.jpg", caption="루브르 박물관 입구의 유리 피라미드", width=600)
st.write("""
    세계에서 가장 큰 박물관 중 하나로, 레오나르도 다빈치의 '모나리자', 밀로의 '비너스' 등 
    수많은 예술 작품을 소장하고 있습니다.
    **방문 팁:** 워낙 넓으니 미리 보고 싶은 작품을 정해서 효율적인 동선을 계획하는 것이 좋습니다.
""")

# ... 다른 관광지 내용 추가

st.header("🇫🇷 즐거운 프랑스 여행 되세요!")
st.write("이 가이드가 여러분의 프랑스 여행 계획에 도움이 되기를 바랍니다. 궁금한 점이 있다면 언제든지 문의해주세요!")
