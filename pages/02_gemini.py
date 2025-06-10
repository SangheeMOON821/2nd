import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

st.set_page_config(layout="wide", page_title="프랑스 관광 가이드 🇫🇷")

# --- 데이터 정의 ---
# 관광지 데이터 (위도, 경도, 설명, 방문 팁, 추천 사진 등)
tourist_spots_data = {
    "파리": [
        {"name": "에펠탑 🗼", "lat": 48.8584, "lon": 2.2945,
         "description": "파리의 상징이자 랜드마크로, 낮과 밤 언제 방문해도 아름다운 풍경을 선사합니다. 저녁에는 5분간 반짝이는 에펠탑 야경을 놓치지 마세요! 미리 온라인으로 티켓을 예매하면 대기 시간을 줄일 수 있습니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Eiffel_Tower_from_Champs_de_Mars.jpg/800px-Eiffel_Tower_from_Champs_de_Mars.jpg"},
        {"name": "루브르 박물관 🖼️", "lat": 48.8606, "lon": 2.3376,
         "description": "세계에서 가장 큰 박물관 중 하나로, 레오나르도 다빈치의 '모나리자', 밀로의 '비너스' 등 수많은 예술 작품을 소장하고 있습니다. 워낙 넓으니 미리 보고 싶은 작품을 정해서 효율적인 동선을 계획하는 것이 좋습니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Pyramide_du_Louvre_et_aile_Richelieu.jpg/800px-Pyramide_du_Louvre_et_aile_Richelieu.jpg"},
        {"name": "노트르담 대성당 ⛪", "lat": 48.8530, "lon": 2.3499,
         "description": "고딕 건축의 걸작으로, 파리의 역사와 문화를 상징하는 중요한 유적지입니다. (현재 복원 중) 외관만으로도 그 웅장함에 압도될 것입니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Notre_Dame_de_Paris_frontal_view_at_sunset.jpg/800px-Notre_Dame_de_Paris_frontal_view_at_sunset.jpg"},
        {"name": "개선문 🏛️", "lat": 48.8738, "lon": 2.2950,
         "description": "나폴레옹 1세가 프랑스군의 승리를 기념하기 위해 세운 거대한 건축물입니다. 정상에 오르면 파리 시내를 한눈에 조망할 수 있습니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Arc_de_Triomphe_de_l%27%C3%89toile%2C_Paris_2016.jpg/800px-Arc_de_Triomphe_de_l%27%C3%89toile%2C_Paris_2016.jpg"},
        {"name": "몽마르뜨 언덕 & 사크레쾨르 대성당 🎨", "lat": 48.8867, "lon": 2.3431,
         "description": "파리에서 가장 높은 언덕으로, 아름다운 사크레쾨르 대성당과 예술가들의 거리인 테르트르 광장이 있습니다. 낭만적인 분위기를 느끼기에 좋습니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Sacre-Coeur_Basilica_Montmartre_Paris.jpg/800px-Sacre-Coeur_Basilica_Montmartre_Paris.jpg"},
        {"name": "세느 강 유람선 🛳️", "lat": 48.8600, "lon": 2.3100, # 대략적인 위치
         "description": "파리의 주요 명소들을 강 위에서 감상할 수 있는 특별한 경험을 선사합니다. 특히 저녁에 탑승하면 에펠탑 야경과 함께 로맨틱한 시간을 보낼 수 있습니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Pont_Alexandre_III_on_the_Seine_River_at_sunset.jpg/800px-Pont_Alexandre_III_on_the_Seine_River_at_sunset.jpg"},
    ],
    "남프랑스": [
        {"name": "니스 - 프롬나드 데 장글레 🏖️", "lat": 43.6960, "lon": 7.2659,
         "description": "아름다운 해변을 따라 펼쳐진 산책로로, 지중해의 에메랄드빛 바다를 감상하며 여유로운 시간을 보낼 수 있습니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Nice_Promenade_des_Anglais.jpg/800px-Nice_Promenade_des_Anglais.jpg"},
        {"name": "칸 - 라 크루아제트 🎬", "lat": 43.5492, "lon": 7.0223,
         "description": "세계적으로 유명한 칸 영화제가 열리는 도시로, 해변을 따라 고급 호텔과 상점들이 늘어서 있습니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Cannes_-_La_Croisette_et_Palais_des_Festivals.jpg/800px-Cannes_-_La_Croisette_et_Palais_des_Festivals.jpg"},
        {"name": "마르세유 - 구 항구 & 노트르담 드 라 가르드 대성당 ⚓", "lat": 43.2965, "lon": 5.3700, # 구 항구
         "description": "프랑스에서 가장 오래된 항구 도시로, 활기찬 분위기와 신선한 해산물 요리를 즐길 수 있습니다. 노트르담 드 라 가르드 대성당에서 도시 전경을 조망해 보세요.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Marseille_Notre_Dame_de_la_Garde.jpg/800px-Marseille_Notre_Dame_de_la_Garde.jpg"},
        {"name": "아비뇽 - 교황청 📜", "lat": 43.9500, "lon": 4.8077,
         "description": "중세 시대 교황들이 거주했던 웅장한 궁전으로, 유네스코 세계문화유산으로 지정되어 있습니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Palais_des_Papes_%28Avignon%29.jpg/800px-Palais_des_Papes_%28Avignon%29.jpg"},
    ],
    "프랑스 서부": [
        {"name": "몽생미셸 🌊", "lat": 48.6361, "lon": -1.5118,
         "description": "신비로운 섬 위에 지어진 수도원으로, 조수 간만의 차에 따라 섬으로 변하는 독특한 풍경을 자랑합니다. 유네스코 세계문화유산이자 프랑스 여행의 하이라이트 중 하나입니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Mont_Saint-Michel_and_its_Bay_at_Sunset.jpg/800px-Mont_Saint-Michel_and_its_Bay_at_Sunset.jpg"},
        {"name": "보르도 🍷", "lat": 44.8378, "lon": -0.5792,
         "description": "세계적으로 유명한 와인 산지로, 아름다운 와인 샤또와 함께 와인 투어를 즐길 수 있습니다. '물의 거울' 광장은 사진 찍기 좋은 명소입니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Bordeaux_Miroir_d%27eau_et_Place_de_la_Bourse.jpg/800px-Bordeaux_Miroir_d%27eau_et_Place_de_la_Bourse.jpg"},
    ],
    "기타 주요 도시/지역": [
        {"name": "스트라스부르 - 대성당 & 쁘띠 프랑스 🎄", "lat": 48.5835, "lon": 7.7452,
         "description": "독일 국경에 위치하여 독특한 문화와 건축 양식을 자랑하는 도시입니다. 쁘띠 프랑스의 아름다운 운하와 목조 가옥, 그리고 웅장한 대성당이 인상적입니다. 특히 크리스마스 마켓 시즌에는 더욱 환상적인 분위기를 즐길 수 있습니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Petite_France%2C_Strasbourg.jpg/800px-Petite_France%2C_Strasbourg.jpg"},
        {"name": "리옹 - 구시가지 & 푸르비에르 언덕 🍽️", "lat": 45.7578, "lon": 4.8320,
         "description": "프랑스의 미식 수도로 불리는 도시입니다. 중세 시대의 좁은 골목과 트라불(Traboule)이라는 비밀 통로들이 얽혀 있는 구시가지, 그리고 리옹 시내를 한눈에 조망할 수 있는 푸르비에르 언덕이 매력적입니다.",
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Lyon_-_vue_de_la_Fourvi%C3%A8re.jpg/800px-Lyon_-_vue_de_la_Fourvi%C3%A8re.jpg"},
    ]
}

# 과학자 데이터
scientists_data = {
    "파리": [
        {"name": "마리 퀴리 (Marie Curie, 1867-1934)",
         "description": "폴란드 태생이지만 파리에서 주로 활동했으며, 방사능 연구와 폴로늄, 라듐의 발견으로 노벨 물리학상과 화학상을 수상한 인류 최초의 여성 노벨상 수상자이자 유일하게 두 분야에서 노벨상을 받은 과학자입니다."},
        {"name": "루이 파스퇴르 (Louis Pasteur, 1822-1895)",
         "description": "미생물학의 아버지로 불리며, 파스퇴르 연구소에서 광견병 백신 개발과 저온 살균법을 확립했습니다."},
    ],
    "남프랑스": [
        {"name": "앙드레 마리 앙페르 (André-Marie Ampère, 1775-1836)",
         "description": "리옹 출신으로, 전기 역학 분야에 큰 공헌을 했으며 전류의 단위인 '암페어(Ampere)'가 그의 이름을 따서 명명되었습니다. (리옹은 지리적으로 남프랑스와 가깝지만 엄밀히는 중동부 프랑스에 해당합니다.)"},
    ],
    "프랑스 서부": [
        {"name": "르네 데카르트 (René Descartes, 1596-1650)",
         "description": "투렌(Touraine) 지방의 라 에이(La Haye) 출신으로, 근대 철학의 아버지이자 수학자이며 '나는 생각한다. 고로 존재한다'라는 명언으로 유명합니다."},
    ],
    "기타 주요 도시/지역": [
         {"name": "앙드레 마리 앙페르 (André-Marie Ampère, 1775-1836)", # 리옹에 다시 언급
         "description": "리옹 출신으로, 전기 역학 분야에 큰 공헌을 했으며 전류의 단위인 '암페어(Ampere)'가 그의 이름을 따서 명명되었습니다."},
    ]
}

# 영화 데이터
movie_data = {
    "파리": [
        {"title": "미드나잇 인 파리 (Midnight in Paris, 2011)",
         "description": "낭만적인 파리의 밤거리와 과거 예술가들과의 만남을 그린 판타지 로맨스 영화."},
        {"title": "아멜리에 (Amélie, 2001)",
         "description": "몽마르뜨를 배경으로 평범한 사람들의 삶에 작은 행복을 선물하는 아멜리의 이야기를 담은 영화."},
        {"title": "레 미제라블 (Les Misérables, 2012)",
         "description": "19세기 파리를 배경으로 한 빅토르 위고의 명작 소설을 각색한 뮤지컬 영화."},
    ],
    "남프랑스": [
        {"title": "투 캐치 어 씨프 (To Catch a Thief, 1955)",
         "description": "히치콕 감독의 작품으로, 프랑스 리비에라의 아름다운 풍경을 배경으로 한 로맨틱 스릴러 영화."},
        {"title": "미스터 빈의 홀리데이 (Mr. Bean's Holiday, 2007)",
         "description": "미스터 빈이 칸 영화제로 가는 여정을 유쾌하게 그린 영화."},
        {"title": "레옹 (Léon: The Professional, 1994)",
         "description": "일부 장면이 마르세유에서 촬영되었으며, 느와르적 분위기의 액션 스릴러."},
    ],
    "프랑스 서부": [
        {"title": "해리 포터와 죽음의 성물 1부 (Harry Potter and the Deathly Hallows – Part 1, 2010)",
         "description": "일부 장면이 몽생미셸과 유사한 분위기의 배경으로 촬영되었습니다."},
        {"title": "와인 미라클 (Bottle Shock, 2008)",
         "description": "1976년 파리 심판에서 캘리포니아 와인이 프랑스 와인을 이기는 실화를 다룬 영화로, 보르도 와인과의 경쟁 구도를 보여줍니다."},
    ],
    "기타 주요 도시/지역": [
        {"title": "유로트립 (EuroTrip, 2004) - 스트라스부르",
         "description": "친구들이 유럽을 여행하며 겪는 코믹한 이야기를 그린 영화로, 스트라스부르의 일부 장면이 등장합니다."},
        {"title": "뤼미에르! (Lumière!, 2017) - 리옹",
         "description": "영화의 발명가인 뤼미에르 형제가 리옹 출신이므로, 그들의 초기 영화들을 모아 만든 다큐멘터리 영화를 추천합니다."},
    ]
}

# --- 앱 시작 ---
st.title("🇫🇷 프랑스 주요 관광지 친절 가이드 🥖")
st.write("프랑스 여행을 위한 최고의 가이드입니다. 프랑스의 아름다운 명소들을 함께 탐험해 보세요! 예술, 역사, 미식, 그리고 낭만이 가득한 프랑스로 떠날 준비되셨나요? ✈️")

# --- 전체 지도 섹션 ---
st.header("✨ 프랑스 주요 관광지 지도 🗺️")
st.write("아래 지도에서 프랑스의 주요 관광지들을 한눈에 확인하고, 각 명소의 위치를 파악해 보세요. 마커를 클릭하면 간략한 설명을 볼 수 있습니다.")

m = folium.Map(location=[46.603354, 1.888334], zoom_start=6) # 프랑스 중심 좌표

for region, spots in tourist_spots_data.items():
    for spot in spots:
        folium.Marker(
            location=[spot["lat"], spot["lon"]],
            popup=f"<b>{spot['name']}</b><br>{spot['description'].split('.')[0]}", # 팝업은 간략하게 첫 문장만
            tooltip=spot["name"],
            icon=folium.Icon(color="red" if region == "파리" else "blue" if region == "남프랑스" else "green" if region == "프랑스 서부" else "purple")
        ).add_to(m)

folium_static(m, width=1000, height=600)

st.write("---")

# --- 지역별 정보 탭 ---
tabs = st.tabs(["🗼 파리", "☀️ 남프랑스", "🌊 프랑스 서부", "🎨 기타 주요 도시/지역"])

with tabs[0]: # 파리 탭
    st.header("🗼 파리 (Paris)")
    st.write("세계에서 가장 로맨틱하고 예술적인 도시, 파리입니다. 💖")

    st.subheader("🔬 파리 출신 또는 주요 활동 과학자")
    for sci in scientists_data["파리"]:
        st.markdown(f"**{sci['name']}**")
        st.write(sci["description"])

    st.subheader("🏛️ 파리의 유명 유적지")
    for spot in tourist_spots_data["파리"]:
        st.markdown(f"**{spot['name']}**")
        st.image(spot["image"], caption=spot["name"].replace(' ', '').split('(')[0], width=400)
        st.write(spot["description"])
        st.markdown("---")

    st.subheader("🎬 파리가 배경인 영화 추천")
    for movie in movie_data["파리"]:
        st.markdown(f"**{movie['title']}**")
        st.write(movie["description"])
        st.markdown("---")

with tabs[1]: # 남프랑스 탭
    st.header("☀️ 남프랑스 (South of France)")
    st.write("눈부신 햇살과 지중해의 푸른 바다가 매력적인 남프랑스입니다. 🏖️")

    st.subheader("🔬 남프랑스 출신 또는 주요 활동 과학자")
    for sci in scientists_data["남프랑스"]:
        st.markdown(f"**{sci['name']}**")
        st.write(sci["description"])

    st.subheader("🏛️ 남프랑스의 유명 유적지")
    for spot in tourist_spots_data["남프랑스"]:
        st.markdown(f"**{spot['name']}**")
        st.image(spot["image"], caption=spot["name"].replace(' ', '').split('(')[0], width=400)
        st.write(spot["description"])
        st.markdown("---")

    st.subheader("🎬 남프랑스가 배경인 영화 추천")
    for movie in movie_data["남프랑스"]:
        st.markdown(f"**{movie['title']}**")
        st.write(movie["description"])
        st.markdown("---")

with tabs[2]: # 프랑스 서부 탭
    st.header("🌊 프랑스 서부 (Western France)")
    st.write("대서양의 거친 파도와 신비로운 경관을 자랑하는 프랑스 서부입니다. 🏰")

    st.subheader("🔬 프랑스 서부 출신 또는 주요 활동 과학자")
    for sci in scientists_data["프랑스 서부"]:
        st.markdown(f"**{sci['name']}**")
        st.write(sci["description"])

    st.subheader("🏛️ 프랑스 서부의 유명 유적지")
    for spot in tourist_spots_data["프랑스 서부"]:
        st.markdown(f"**{spot['name']}**")
        st.image(spot["image"], caption=spot["name"].replace(' ', '').split('(')[0], width=400)
        st.write(spot["description"])
        st.markdown("---")

    st.subheader("🎬 프랑스 서부가 배경인 영화 추천")
    for movie in movie_data["프랑스 서부"]:
        st.markdown(f"**{movie['title']}**")
        st.write(movie["description"])
        st.markdown("---")

with tabs[3]: # 기타 주요 도시/지역 탭
    st.header("🎨 기타 주요 도시/지역")
    st.write("프랑스 곳곳에 숨겨진 매력적인 도시들을 만나보세요.")

    st.subheader("🔬 기타 주요 도시/지역 출신 또는 주요 활동 과학자")
    for sci in scientists_data["기타 주요 도시/지역"]:
        st.markdown(f"**{sci['name']}**")
        st.write(sci["description"])

    st.subheader("🏛️ 기타 주요 도시/지역의 유명 유적지")
    for spot in tourist_spots_data["기타 주요 도시/지역"]:
        st.markdown(f"**{spot['name']}**")
        st.image(spot["image"], caption=spot["name"].replace(' ', '').split('(')[0], width=400)
        st.write(spot["description"])
        st.markdown("---")

    st.subheader("🎬 기타 주요 도시/지역이 배경인 영화 추천")
    for movie in movie_data["기타 주요 도시/지역"]:
        st.markdown(f"**{movie['title']}**")
        st.write(movie["description"])
        st.markdown("---")

st.write("---")

st.header("🇫🇷 즐거운 프랑스 여행 되세요!")
st.write("이 가이드가 여러분의 프랑스 여행 계획에 도움이 되기를 바랍니다. 궁금한 점이 있다면 언제든지 문의해주세요! 😊")
