import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
from streamlit_elements import elements, html

st.set_page_config(layout="wide", page_title="역학적 에너지 보존 시뮬레이션")

st.title("🚀 움직이는 물체 시뮬레이션: 역학적 에너지 보존")
st.subheader("물체의 낙하 운동과 함께 위치 에너지, 운동 에너지의 변화를 확인해 보세요!")

# --- 운동 에너지 및 위치 에너지 공식 설명 ---
st.markdown("""
### 💡 역학적 에너지의 기본 공식
* **위치 에너지 (Potential Energy, PE)**: 물체가 어떤 위치에 있을 때 가지는 에너지. 중력장 내에서는 다음과 같습니다.
    $$ PE = mgh $$
    여기서 $m$은 질량 (kg), $g$는 중력 가속도 (m/s²), $h$는 높이 (m) 입니다.

* **운동 에너지 (Kinetic Energy, KE)**: 물체가 움직일 때 가지는 에너지.
    $$ KE = \\frac{1}{2}mv^2 $$
    여기서 $m$은 질량 (kg), $v$는 속도 (m/s) 입니다.

* **총 역학 에너지 (Mechanical Energy, ME)**: 위치 에너지와 운동 에너지의 합입니다.
    $$ ME = PE + KE $$
    공기 저항과 같은 외부 방해 요소가 없다면, 총 역학 에너지는 항상 보존됩니다.
""")

st.markdown("---")

# --- 사용자 입력 ---
st.sidebar.header("시뮬레이션 설정")
mass = st.sidebar.slider("질량 (kg)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
initial_height = st.sidebar.slider("초기 높이 (m)", min_value=1.0, max_value=100.0, value=50.0, step=1.0)
g = st.sidebar.slider("중력 가속도 (m/s²)", min_value=1.0, max_value=20.0, value=9.81, step=0.01)
time_duration = st.sidebar.slider("시뮬레이션 시간 (s)", min_value=1.0, max_value=10.0, value=5.0, step=0.1)
time_steps = st.sidebar.slider("시간 단계 수", min_value=50, max_value=500, value=200, step=10)
ball_diameter = st.sidebar.slider("물체 지름 (px)", min_value=10, max_value=50, value=30, step=1)


# --- 계산 ---
dt = time_duration / time_steps
time_points = np.linspace(0, time_duration, time_steps)

heights = []
velocities = []
potential_energies = []
kinetic_energies = []
total_energies = []

# 각 시간 단계에서의 높이와 속도 계산
for t in time_points:
    # 자유 낙하 공식: h = h0 - 0.5 * g * t^2
    # v = g * t
    h = initial_height - 0.5 * g * t**2
    v = g * t

    # 물체가 땅에 닿으면 멈춤
    if h < 0:
        h = 0
        # 땅에 닿는 순간의 최종 속도 계산 (vf = sqrt(2gh0))
        v = np.sqrt(2 * g * initial_height)

    heights.append(h)
    velocities.append(v)
    potential_energies.append(mass * g * h)
    kinetic_energies.append(0.5 * mass * v**2)
    total_energies.append(mass * g * h + 0.5 * mass * v**2) # PE + KE

# 데이터를 DataFrame으로 변환
df = pd.DataFrame({
    "시간 (s)": time_points,
    "높이 (m)": heights,
    "속도 (m/s)": velocities,
    "위치 에너지 (J)": potential_energies,
    "운동 에너지 (J)": kinetic_energies,
    "총 역학 에너지 (J)": total_energies
})

# --- 시뮬레이션 화면 및 그래프 배치 ---
st.markdown("---")
st.header("시뮬레이션 화면 및 에너지 변화 그래프")

col1, col2 = st.columns([1, 2]) # 1:2 비율로 컬럼 분할

with col1:
    st.subheader("물체 낙하 시뮬레이션")
    # Streamlit Elements를 사용하여 HTML, CSS, JavaScript 삽입
    with elements("simulation_area"):
        # CSS 스타일 (물체, 배경)
        st.markdown(
            f"""
            <style>
                .simulation-container {{
                    position: relative;
                    width: 100%;
                    height: 400px; /* 시뮬레이션 높이 */
                    background-color: #e0f2f7;
                    border: 2px solid #333;
                    overflow: hidden; /* 물체가 컨테이너 밖으로 나가지 않게 */
                    margin-bottom: 20px;
                }}
                .ball {{
                    position: absolute;
                    width: {ball_diameter}px; /* 동적으로 조절 */
                    height: {ball_diameter}px; /* 동적으로 조절 */
                    background-color: #ff4b4b;
                    border-radius: 50%;
                    left: calc(50% - {ball_diameter/2}px); /* 중앙 정렬 */
                    top: 0px; /* 초기 위치 */
                    transform: translateY(0%); /* 높이에 따라 조절 */
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
                }}
                .ground {{
                    position: absolute;
                    bottom: 0;
                    width: 100%;
                    height: 20px;
                    background-color: #6d4c41;
                    color: white;
                    text-align: center;
                    line-height: 20px;
                    font-size: 0.8em;
                }}
            </style>
            """,
            unsafe_allow_html=True
        )

        # HTML 구조
        html.div(
            [
                html.div(id="ball", className="ball"),
                html.div("GROUND", className="ground")
            ],
            className="simulation-container"
        )

        # JavaScript 애니메이션 로직
        js_code = f"""
            const ball = document.getElementById('ball');
            const container = document.querySelector('.simulation-container');
            const containerHeight = container.clientHeight; // 컨테이너 높이 (px)
            const ballDiameterPx = {ball_diameter}; // 물체 지름 (px)
            const groundHeightPx = 20; // 땅 높이 (px)

            const initialHeightMeters = {initial_height}; // 사용자 설정 초기 높이 (m)
            const g = {g}; // 중력 가속도 (m/s^2)
            const simulationDuration = {time_duration}; // 시뮬레이션 전체 시간 (s)

            let startTime = null;
            let animationFrameId = null;

            function animateBall(timestamp) {{
                if (startTime === null) startTime = timestamp;
                const elapsed = (timestamp - startTime) / 1000; // 경과 시간 (초)

                // 자유 낙하 공식: h = 0.5 * g * t^2
                let fallDistanceMeters = 0.5 * g * elapsed * elapsed;

                // 물체가 실제 초기 높이 (m)를 넘어가지 않도록
                if (fallDistanceMeters > initialHeightMeters) {{
                    fallDistanceMeters = initialHeightMeters;
                }}

                // 시뮬레이션 컨테이너 내에서의 픽셀 위치로 변환
                // (낙하 거리 / 총 높이) * (컨테이너 내부의 실제 낙하 가능한 높이)
                const maxFallPixels = containerHeight - ballDiameterPx - groundHeightPx;
                const fallDistancePixels = (fallDistanceMeters / initialHeightMeters) * maxFallPixels;
                
                let currentTop = fallDistancePixels;

                // 물체가 땅에 닿으면 멈춤
                if (currentTop >= maxFallPixels) {{
                    currentTop = maxFallPixels;
                }}
                ball.style.top = currentTop + 'px';

                // 시뮬레이션 시간 종료 또는 물체가 땅에 닿으면 애니메이션 중지
                if (elapsed < simulationDuration && currentTop < maxFallPixels) {{
                    animationFrameId = requestAnimationFrame(animateBall);
                }} else {{
                    cancelAnimationFrame(animationFrameId);
                }}
            }}
            
            // 앱이 다시 로드될 때마다 애니메이션을 재시작
            // 이전 애니메이션이 있다면 취소하고 새로 시작
            if (animationFrameId) {{
                cancelAnimationFrame(animationFrameId);
            }}
            requestAnimationFrame(animateBall);
        """
        html.script(js_code)

with col2:
    # 에너지 그래프
    st.subheader("시간에 따른 에너지 변화")
    fig_energy = px.line(df, x="시간 (s)", y=["위치 에너지 (J)", "운동 에너지 (J)", "총 역학 에너지 (J)"],
                     title="시간에 따른 에너지 변화",
                     labels={"value": "에너지 (J)", "variable": "에너지 종류"},
                     height=500)
    fig_energy.update_layout(hovermode="x unified")
    st.plotly_chart(fig_energy, use_container_width=True)

# 높이 및 속도 그래프 (추가 정보)
st.markdown("---")
st.header("높이 및 속도 변화 그래프 (참고)")
fig_height_velocity = px.line(df, x="시간 (s)", y=["높이 (m)", "속도 (m/s)"],
                              title="시간에 따른 높이 및 속도 변화",
                              labels={"value": "값", "variable": "측정량"},
                              height=300)
fig_height_velocity.update_layout(hovermode="x unified")
st.plotly_chart(fig_height_velocity, use_container_width=True)

st.markdown("""
---
### 시뮬레이션 설명
이 시뮬레이션은 공기 저항이 없는 이상적인 자유 낙하 상황에서의 역학적 에너지 보존을 보여줍니다.
* **위치 에너지**는 높이가 줄어듦에 따라 감소합니다.
* **운동 에너지**는 속도가 증가함에 따라 증가합니다.
* 두 에너지의 합인 **총 역학 에너지**는 거의 일정하게 유지되어 에너지 보존 법칙을 따릅니다.
""")

st.markdown("---")

# --- 간단한 퀴즈 ---
st.header("🤔 역학적 에너지 보존 개념 확인 퀴즈")

quiz_questions = [
    {
        "question": "물체의 높이가 높아질수록 어떤 에너지가 증가할까요?",
        "options": ["운동 에너지", "위치 에너지", "열 에너지", "화학 에너지"],
        "answer": "위치 에너지"
    },
    {
        "question": "물체의 속도가 빨라질수록 어떤 에너지가 증가할까요?",
        "options": ["위치 에너지", "탄성 에너지", "운동 에너지", "핵 에너지"],
        "answer": "운동 에너지"
    },
    {
        "question": "공기 저항이 없는 이상적인 자유 낙하 상황에서 총 역학 에너지는 어떻게 될까요?",
        "options": ["증가한다", "감소한다", "일정하게 보존된다", "0이 된다"],
        "answer": "일정하게 보존된다"
    },
    {
        "question": "질량이 $m$인 물체가 높이 $h$에 있을 때의 위치 에너지 공식은?",
        "options": ["$\\frac{1}{2}mv^2$", "$mgh$", "$mh^2$", "$mg/h$"],
        "answer": "$mgh$"
    },
    {
        "question": "질량이 $m$인 물체가 속도 $v$로 움직일 때의 운동 에너지 공식은?",
        "options": ["$mgh$", "$mv$", "$\\frac{1}{2}mv^2$", "$mgv$"],
        "answer": "$\\frac{1}{2}mv^2$"
    }
]

score = 0
for i, q in enumerate(quiz_questions):
    st.subheader(f"Q{i+1}. {q['question']}")
    user_answer = st.radio("정답을 선택하세요:", q['options'], key=f"q{i}")

    if st.button("정답 확인", key=f"check{i}"):
        if user_answer == q['answer']:
            st.success("✅ 정답입니다!")
            score += 1
        else:
            st.error(f"❌ 오답입니다. 정답은 '{q['answer']}' 입니다.")
    st.markdown("---")

if st.button("최종 점수 확인"):
    st.info(f"총 {len(quiz_questions)}문제 중 {score}문제를 맞추셨습니다.")
    if score == len(quiz_questions):
        st.balloons()
        st.success("🎉 완벽합니다! 역학적 에너지 보존 개념을 정확히 이해하고 계시네요!")
    elif score >= len(quiz_questions) * 0.7:
        st.info("👍 잘하셨습니다! 대부분의 개념을 이해하고 계시네요.")
    else:
        st.warning("🧐 다시 한번 시뮬레이션과 설명을 살펴보세요.")
