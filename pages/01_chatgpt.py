import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="프랑스 관광지 가이드", layout="wide")

st.title("🇫🇷 프랑스 주요 관광지 가이드")
st.markdown("""
프랑스는 예술, 역사, 미식 등 다양한 매력을 가진 나라입니다.  
아래에서 프랑스의 대표적인 관광지를 살펴보고, 지도에서 위치도 확인해보세요!
""")

# 관광지 데이터
tourist_spots = [
    {
        "name": "에펠탑 (Eiffel Tower)",
        "location": [48.8584, 2.2945],
        "description": """
파리의 상징이자 프랑스를 대표하는 랜드마크입니다.  
밤에는 조명이 반짝이며 로맨틱한 분위기를 연출하고, 전망대에서는 파리 시내가 한눈에 내려다보입니다.
        """
    },
    {
        "name": "루브르 박물관 (Louvre Museum)",
        "location": [48.8606, 2.3376],
        "description": """
세계 최대의 미술관 중 하나로, 모나리자, 밀로의 비너스 등을 소장하고 있습니다.  
고대 유물부터 근대 회화까지 다양한 예술작품을 감상할 수 있습니다.
        """
    },
    {
        "name": "베르사유 궁전 (Palace of Versailles)",
        "location": [48.8049, 2.1204],
        "description": """
프랑스 절대왕정의 상징으로 루이 14세가 건설한 궁전입니다.  
화려한 거울의 방(Hall of Mirrors)과 광대한 정원이 유명합니다.
        """
    },
    {
        "name": "니스 해변 (Nice)",
        "location": [43.7102, 7.2620],
        "description": """
지중해 연안의 프랑스 남부 도시로, 아름다운 해변과 푸른 바다가 유명합니다.  
아트갤러리, 해산물 요리, 유럽 특유의 여유로운 분위기를 만끽할 수 있습니다.
        """
    },
    {
        "name": "리옹 구시가지 (Lyon Old Town)",
        "location": [45.7640, 4.8357],
        "description": """
유네스코 세계유산에 등록된 중세도시로, 미로 같은 골목과 고딕 건축이 매력적입니다.  
프랑스 요리의 중심지로도 유명하며 미식가들에게 사랑받는 도시입니다.
        """
    },
    {
        "name": "마르세유 항구 (Marseille)",
        "location": [43.2965, 5.3698],
        "description": """
프랑스 제2의 도시이자 지중해 최대의 항구 도시입니다.  
이국적인 분위기와 함께 항구 주변의 해산물 식당, 노트르담 드 라 가르드 성당 등이 인기입니다.
        """
    },
]

# Folium 지도 생성
m = folium.Map(location=[46.6031, 1.8883], zoom_start=6, tiles='OpenStreetMap')

# 마커 추가
for spot in tourist_spots:
    folium.Marker(
        location=spot["location"],
        popup=f"<strong>{spot['name']}</strong><br>{spot['description']}",
        tooltip=spot["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

st.subheader("🗺️ 관광지 지도 보기")
st.markdown("아래 지도에서 관광지를 클릭하면 자세한 설명을 확인할 수 있어요.")

# 지도 표시
st_data = st_folium(m, width=1000, height=600)

# 선택한 관광지 정보 보여주기
if st_data and st_data.get("last_object_clicked"):
    clicked_coords = st_data["last_object_clicked"]["lat"], st_data["last_object_clicked"]["lng"]
    for spot in tourist_spots:
        if abs(spot["location"][0] - clicked_coords[0]) < 0.01 and abs(spot["location"][1] - clicked_coords[1]) < 0.01:
            st.markdown(f"### 📍 {spot['name']}")
            st.write(spot["description"])
            break
