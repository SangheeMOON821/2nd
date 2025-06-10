import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="프랑스 지역별 관광 가이드", layout="wide")

st.title("🇫🇷 프랑스 지역별 관광 가이드")

tabs = st.tabs(["🏖️ 프랑스 남부", "🏙️ 주요 도시", "📚 문화 & 유적지"])

# ---------- 프랑스 남부 ----------
with tabs[0]:
    st.header("프랑스 남부 명소")
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6f/Nice_vue_generale.jpg", caption="니스 해변", use_column_width=True)
    st.markdown("""
**니스 (Nice)**  
지중해 연안의 프랑스 리비에라 대표 도시. 맑은 해변과 아기자기한 구시가지, 마티스 미술관이 인기.

**아비뇽 (Avignon)**  
교황청이 한때 옮겨졌던 역사적 도시로, 고딕양식의 교황궁(Palais des Papes)으로 유명함.

**엑상프로방스 (Aix-en-Provence)**  
세잔(Cézanne)의 고향으로 고즈넉한 골목과 라벤더 향이 인상적인 도시.

**마르세유 (Marseille)**  
프랑스 최대의 항구도시이자 다문화 도시. 노트르담 드 라 가르드 성당, 깔레뜨 섬이 관광 포인트.
    """)

# ---------- 주요 도시 ----------
with tabs[1]:
    st.header("프랑스 주요 도시와 위대한 과학자들")

    cities = {
        "파리": {
            "image": "https://upload.wikimedia.org/wikipedia/commons/a/af/Tour_Eiffel_Wikimedia_Commons.jpg",
            "scientist": "앙리 푸앵카레 (Henri Poincaré)",
            "achievement": "수학자이자 물리학자로 상대성 이론의 수학적 기반을 다졌습니다."
        },
        "리옹": {
            "image": "https://upload.wikimedia.org/wikipedia/commons/6/60/Lyon-Vieux-Lyon.jpg",
            "scientist": "앙드레 마리 앙페르 (André-Marie Ampère)",
            "achievement": "전류 단위인 '암페어'의 유래로, 전자기학의 기초를 마련했습니다."
        },
        "툴루즈": {
            "image": "https://upload.wikimedia.org/wikipedia/commons/2/29/Toulouse_Garonne.jpg",
            "scientist": "폴 사바티에 (Paul Sabatier)",
            "achievement": "촉매 화학으로 노벨 화학상 수상. 유기수소화 반응 개발."
        },
    }

    city_choice = st.selectbox("도시를 선택하세요", list(cities.keys()))

    st.image(cities[city_choice]["image"], use_column_width=True)
    st.markdown(f"""
### {city_choice}
- **출신 과학자**: {cities[city_choice]["scientist"]}
- **업적**: {cities[city_choice]["achievement"]}
    """)

# ---------- 문화와 유적지 ----------
with tabs[2]:
    st.header("문화 유산과 예술의 도시")

    places = {
        "몽생미셸": {
            "description": "해안에 우뚝 솟은 수도원으로 유네스코 세계유산. 밀물과 썰물의 경계에서 신비로운 풍경을 자랑함.",
            "image": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Mont_St_Michel_3%2C_Brittany%2C_France_-_July_2011.jpg",
            "media": ["『몽생미셸의 비밀』", "영화 『마법의 성』 영감"]
        },
        "지베르니": {
            "description": "모네의 집과 정원이 있는 곳. 인상주의 탄생의 중심지로 예술가들의 성지.",
            "image": "https://upload.wikimedia.org/wikipedia/commons/3/38/Giverny_house_and_garden.jpg",
            "media": ["모네의 수련 연작", "다큐멘터리 『빛의 화가 모네』"]
        },
        "아를 (Arles)": {
            "description": "빈센트 반 고흐가 머문 도시로, 고대 로마 원형극장과 함께 예술과 역사가 공존.",
            "image": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Arles_Amphithéâtre.jpg",
            "media": ["고흐 작품 『아를의 별이 빛나는 밤』", "책 『반 고흐의 편지들』"]
        }
    }

    pick = st.selectbox("도시를 선택하세요", list(places.keys()))
    st.image(places[pick]["image"], caption=pick, use_column_width=True)
    st.markdown(f"""
**{pick}**  
{places[pick]["description"]}
""")

    if st.button("🎬 이 지역이 배경이 된 영화나 책을 추천해드릴까요?"):
        st.markdown("**추천 작품:**")
        for work in places[pick]["media"]:
            st.write(f"📘 {work}")
