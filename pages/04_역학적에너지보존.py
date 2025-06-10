import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide", page_title="Mechanical Energy Conservation")

st.title("역학적 에너지 보존 시뮬레이션")
st.subheader("위치 에너지와 운동 에너지 변화 확인")

# --- 사용자 입력 ---
st.sidebar.header("시뮬레이션 설정")
mass = st.sidebar.slider("질량 (kg)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
initial_height = st.sidebar.slider("초기 높이 (m)", min_value=1.0, max_value=100.0, value=50.0, step=1.0)
g = st.sidebar.slider("중력 가속도 (m/s²)", min_value=1.0, max_value=20.0, value=9.81, step=0.01)
time_duration = st.sidebar.slider("시뮬레이션 시간 (s)", min_value=1.0, max_value=10.0, value=5.0, step=0.1)
time_steps = st.sidebar.slider("시간 단계 수", min_value=50, max_value=500, value=200, step=10)

# --- 계산 ---
dt = time_duration / time_steps
time = np.linspace(0, time_duration, time_steps)

heights = []
velocities = []
potential_energies = []
kinetic_energies = []
total_energies = []

current_height = initial_height
current_velocity = 0.0 # 초기 속도 0

for t in time:
    # 물체가 땅에 닿으면 멈춤
    if current_height <= 0:
        current_height = 0
        current_velocity = 0
    else:
        # 중력 가속도에 의한 속도 변화 (v = v0 + at)
        current_velocity = g * t # 자유 낙하 공식 (h = 0.5 * g * t^2 -> v = g*t)

        # 높이 변화 (h = h0 - 0.5 * g * t^2)
        # 여기서의 't'는 각 시간 단계의 시작부터의 상대적인 시간
        # 조금 더 정확하게는 각 시간 스텝마다 계산
        # 높이 계산은 이전 높이에서 v*dt 또는 0.5*g*dt^2를 빼는 방식이 더 정확
        # 여기서는 단순화를 위해 자유낙하 공식을 활용
        fall_distance = 0.5 * g * t**2
        current_height = initial_height - fall_distance
        if current_height < 0:
            current_height = 0
            # 땅에 닿는 순간의 속도로 고정
            current_velocity = np.sqrt(2 * g * initial_height)


    pe = mass * g * current_height
    ke = 0.5 * mass * current_velocity**2
    me = pe + ke

    heights.append(current_height)
    velocities.append(current_velocity)
    potential_energies.append(pe)
    kinetic_energies.append(ke)
    total_energies.append(me)

# 데이터를 DataFrame으로 변환
df = pd.DataFrame({
    "시간 (s)": time,
    "높이 (m)": heights,
    "속도 (m/s)": velocities,
    "위치 에너지 (J)": potential_energies,
    "운동 에너지 (J)": kinetic_energies,
    "총 역학 에너지 (J)": total_energies
})

# --- 그래프 시각화 ---
st.header("에너지 변화 그래프")

# 에너지 그래프
fig_energy = px.line(df, x="시간 (s)", y=["위치 에너지 (J)", "운동 에너지 (J)", "총 역학 에너지 (J)"],
                     title="시간에 따른 에너지 변화",
                     labels={"value": "에너지 (J)", "variable": "에너지 종류"},
                     height=500)
fig_energy.update_layout(hovermode="x unified")
st.plotly_chart(fig_energy, use_container_width=True)

# 높이 및 속도 그래프
st.header("높이 및 속도 변화 그래프")
fig_height_velocity = px.line(df, x="시간 (s)", y=["높이 (m)", "속도 (m/s)"],
                              title="시간에 따른 높이 및 속도 변화",
                              labels={"value": "값", "variable": "측정량"},
                              height=400)
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
