import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="프랑스 지역별 관광 가이드", layout="wide")

st.title("🇫🇷 프랑스 지역별 관광 가이드")

# 세션 상태 초기화
if "wishlist" not in st.session_state:
    st.session_state["wishlist"] = []

# ------------------------- 🔍 검색 기능 -------------------------
search_query = st.text_input("🔍 도시 또는 관광지를 검색해보세요:")

# 관광지 데이터 (검색 및 지도용)
tourist_data = {
    "에펠탑": {"location": [48.8584, 2.2945], "region": "파리", "desc": "파리의 상징, 야경이 아름다움."},
    "루브르 박물관": {"location": [48.8606, 2.3376], "region": "파리", "desc": "모나리자, 세계 최대 미술관."},
    "마르세유": {"location": [43.2965, 5.3698], "region": "남부", "desc": "항구도시, 깔레뜨 섬이 유명."},
    "몽생미셸": {"location": [48.6361, -1.5115], "region": "노르망디", "desc": "해안 수도원, 유네스코 세계유산."},
    "리옹": {"location": [45.75, 4.85], "region": "리옹", "desc": "미식의 도시, 앙페르의 고향."},
    "지베르니": {"location": [49.0756, 1.5331], "region": "노르망디", "desc": "모네의 정원이 있는 예술마을."},
}

if search_query:
    results = {k: v for k, v in tourist_data.items() if search_query.lower() in k.lower()}
    if results:
        for name, info in results.items():
            st.subheader(f"📍 {name}")
            st.markdown(f"**지역:** {info['region']}\n\n{info['desc']}")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.map({"lat": [info["location"][0]], "lon": [info["location"][1]]})
            with col2:
                if st.button(f"🌟 찜하기 ({name})"):
                    if name not in st.session_state["wishlist"]:
                        st.session_state["wishlist"].append(name)
                        st.success(f"{name}이(가) 찜 목록에 추가되었습니다.")
    else:
        st.warning("검색 결과가 없습니다.")

# ------------------------- 🗂️ 지역별 탭 -------------------------
tabs = st.tabs(["🏖️ 프랑스 남부", "🏙️ 주요 도시", "📚 문화 & 유적지"])

# ---------- 남부 ----------
with tabs[0]:
    st.header("프랑스 남부 명소")
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6f/Nice_vue_generale.jpg", caption="니스 해변", use_column_width=True)
    st.markdown("**마르세유, 니스, 아비뇽, 엑상프로방스** 등 풍부한 자연과 문화유산이 공존하는 지역입니다.")
    if st.button("🌟 마르세유 찜하기"):
        if "마르세유" not in st.session_state["wishlist"]:
            st.session_state["wishlist"].append("마르세유")
            st.success("마르세유를 찜 목록에 추가했어요!")

# ---------- 주요 도시 ----------
with tabs[1]:
    st.header("프랑스 주요 도시 & 위대한 과학자들")

    cities = {
        "파리": {
            "image": "https://upload.wikimedia.org/wikipedia/commons/a/af/Tour_Eiffel_Wikimedia_Commons.jpg",
            "scientist": "앙리 푸앵카레",
            "achievement": "상대성이론의 수학적 기반을 마련한 수학자"
        },
        "리옹": {
            "image": "https://upload.wikimedia.org/wikipedia/commons/6/60/Lyon-Vieux-Lyon.jpg",
            "scientist": "앙드레 마리 앙페르",
            "achievement": "전자기학의 창시자, '암페어' 단위의 유래"
        },
        "툴루즈": {
            "image": "https://upload.wikimedia.org/wikipedia/commons/2/29/Toulouse_Garonne.jpg",
            "scientist": "폴 사바티에",
            "achievement": "노벨화학상 수상, 수소화 반응 개발"
        },
    }

    city_choice = st.selectbox("도시 선택", list(cities.keys()))
    st.image(cities[city_choice]["image"], use_column_width=True)
    st.markdown(f"""
**{city_choice}**
- 출신 과학자: {cities[city_choice]['scientist']}
- 주요 업적: {cities[city_choice]['achievement']}
""")
    if st.button(f"🌟 {city_choice} 찜하기"):
        if city_choice not in st.session_state["wishlist"]:
            st.session_state["wishlist"].append(city_choice)
            st.success(f"{city_choice}를 찜 목록에 추가했어요!")

# ---------- 유적지/문화 ----------
with tabs[2]:
    st.header("문화와 유적지가 살아있는 도시들")

    culture_places = {
        "몽생미셸": {
            "description": "해안 수도원, 유네스코 세계유산. 밀물 썰물 풍경이 신비롭다.",
            "image": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Mont_St_Michel_3%2C_Brittany%2C_France_-_July_2011.jpg",
            "media": ["『몽생미셸의 비밀』", "영화 『마법의 성』"]
        },
        "지베르니": {
            "description": "모네의 정원과 집이 있는 곳. 인상파의 상징.",
            "image": "https://upload.wikimedia.org/wikipedia/commons/3/38/Giverny_house_and_garden.jpg",
            "media": ["다큐 『빛의 화가 모네』", "모네의 수련 연작"]
        },
        "아를": {
            "description": "고흐가 살았던 도시. 고대 로마 유적과 예술의 만남.",
            "image": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Arles_Amphithéâtre.jpg",
            "media": ["책 『반 고흐의 편지들』", "고흐의 아를 연작"]
        }
    }

    pick = st.selectbox("도시 선택", list(culture_places.keys()))
    st.image(culture_places[pick]["image"], caption=pick, use_column_width=True)
    st.markdown(f"**{pick}**: {culture_places[pick]['description']}")

    if st.button("🎬 이 지역이 배경이 된 영화나 책을 추천해드릴까요?"):
        st.markdown("**📚 관련 작품:**")
        for media in culture_places[pick]["media"]:
            st.write(f"- {media}")

    if st.button(f"🌟 {pick} 찜하기"):
        if pick not in st.session_state["wishlist"]:
            st.session_state["wishlist"].append(pick)
            st.success(f"{pick}을(를) 찜 목록에 추가했어요!")

# ------------------------- 🌟 찜 목록 -------------------------
with st.expander("🌟 내가 찜한 관광지 보기"):
    if st.session_state["wishlist"]:
        for item in st.session_state["wishlist"]:
            st.write(f"✅ {item}")
    else:
        st.write("아직 찜한 장소가 없어요.")
