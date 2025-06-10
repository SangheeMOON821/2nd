import streamlit as st
from datetime import date
import random

st.set_page_config(page_title="MBTI 동물 추천 & 오늘의 운세", page_icon="✨")

# 🎉 환영 인사
st.markdown("# 👋 만나서 반가워요!")
st.markdown("당신의 성향과 오늘의 기분을 알아보는 시간입니다 🌈")

# 사용자 입력
name = st.text_input("📝 당신의 이름(닉네임)을 입력해주세요")
birthdate = st.date_input("🎂 생일을 선택해주세요", min_value=date(1900, 1, 1), max_value=date.today())
mbti = st.selectbox("🔮 당신의 MBTI를 선택해주세요", 
                    ["ISTJ", "ISFJ", "INFJ", "INTJ", 
                     "ISTP", "ISFP", "INFP", "INTP", 
                     "ESTP", "ESFP", "ENFP", "ENTP", 
                     "ESTJ", "ESFJ", "ENFJ", "ENTJ"])

st.markdown("---")

if name and birthdate and mbti:
    # MBTI별 동물 추천
    mbti_animals = {
        "ISTJ": ("🐢 거북이", "신중하고 책임감 있는 성격과 잘 어울려요."),
        "ISFJ": ("🐑 양", "온화하고 따뜻한 마음을 가진 당신에게 잘 어울려요."),
        "INFJ": ("🦉 부엉이", "지혜롭고 통찰력 있는 성격과 찰떡궁합이에요."),
        "INTJ": ("🦊 여우", "논리적이고 전략적인 사고를 가진 당신에게 딱이에요."),
        "ISTP": ("🐍 뱀", "차분하고 독립적인 성향과 잘 맞아요."),
        "ISFP": ("🦌 사슴", "섬세하고 조용한 성격을 가진 당신과 잘 어울려요."),
        "INFP": ("🦄 유니콘", "이상주의적이고 순수한 마음을 가진 당신과 딱이에요."),
        "INTP": ("🦉 올빼미", "탐구심 많은 성향에 완벽하게 어울려요."),
        "ESTP": ("🐅 호랑이", "모험심 강하고 에너지 넘치는 성격과 잘 맞아요."),
        "ESFP": ("🐬 돌고래", "사교적이고 즐거움을 추구하는 성격에 어울려요."),
        "ENFP": ("🐦 앵무새", "창의적이고 자유로운 영혼에 찰떡이에요."),
        "ENTP": ("🐵 원숭이", "호기심 많고 재치 있는 성격에 잘 어울려요."),
        "ESTJ": ("🦁 사자", "리더십 있고 현실적인 성격에 어울리는 동물이죠."),
        "ESFJ": ("🐕 강아지", "다정하고 사람을 좋아하는 당신에게 딱이에요."),
        "ENFJ": ("🐘 코끼리", "배려심 많고 신뢰를 주는 성격과 어울려요."),
        "ENTJ": ("🦅 독수리", "당당하고 결단력 있는 성향에 잘 맞아요."),
    }

    # 운세 텍스트 예시
    fortunes = [
        "🌟 오늘은 새로운 아이디어가 떠오를 좋은 날이에요!",
        "💡 주변 사람과의 대화 속에 행운이 숨어 있어요.",
        "🍀 예상치 못한 좋은 소식이 들려올지도 몰라요!",
        "🚀 도전하는 일에 큰 성과가 따를 수 있어요.",
        "☕ 오늘은 여유를 갖고 자신을 돌보는 시간이 필요해요.",
        "🌈 작은 선택이 큰 변화를 가져올 거예요.",
    ]

    # 동물 추천
    animal, reason = mbti_animals.get(mbti, ("🐾", "당신만의 특별한 동물이 있어요!"))
    st.markdown(f"## 🐾 {name} 님에게 어울리는 동물은 {animal}입니다!")
    st.markdown(f"**이유:** {reason}")

    # 운세
    random.seed(str(birthdate) + mbti)  # 생일과 MBTI에 따라 고정된 운세
    today_fortune = random.choice(fortunes)
    st.markdown("## 🔮 오늘의 운세")
    st.markdown(today_fortune)
else:
    st.info("위의 모든 항목을 입력하시면 동물 추천과 운세가 표시됩니다 😊")
