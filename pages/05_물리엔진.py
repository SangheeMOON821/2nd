import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.
import numpy as np
import time

# 물리 상수
g = 9.81  # 중력 가속도 (m/s^2)
m = 1.0   # 물체의 질량 (kg)

st.set_page_config(layout="wide")
st.title("역학적 에너지 보존 시뮬레이션 (자유 낙하)")

st.sidebar.header("시뮬레이션 설정")
initial_height = st.sidebar.slider("초기 높이 (m)", 1.0, 100.0, 50.0, 1.0)
# initial_velocity = st.sidebar.slider("초기 속도 (m/s)", 0.0, 30.0, 0.0, 0.1) # 자유 낙하이므로 초기 속도는 0으로 가정
time_step = st.sidebar.slider("시간 간격 (s)", 0.01, 0.1, 0.05, 0.01)
animation_speed = st.sidebar.slider("애니메이션 속도 (배속)", 0.1, 5.0, 1.0, 0.1)

start_button = st.sidebar.button("시뮬레이션 시작")

if start_button:
    st.subheader("물체 운동 및 에너지 전환")

    # 초기 조건
    h_current = initial_height
    v_current = 0.0
    t_current = 0.0

    # 데이터 저장 리스트
    time_data = []
    height_data = []
    velocity_data = []
    potential_energy_data = []
    kinetic_energy_data = []
    total_energy_data = []

    # 애니메이션을 위한 Matplotlib figure 및 axes 설정
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.tight_layout(pad=3.0)

    # 물체 위치 시각화 (ax1)
    ax1.set_xlim(-1, 1) # 물체는 수직으로만 움직이므로 X축은 고정
    ax1.set_ylim(0, initial_height * 1.1)
    ax1.set_xlabel("X (arbitrary)")
    ax1.set_ylabel("높이 (m)")
    ax1.set_title("물체의 운동")
    point, = ax1.plot(0, h_current, 'o', color='red', markersize=10)
    ax1_text = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, fontsize=10, verticalalignment='top')

    # 에너지 그래프 시각화 (ax2)
    ax2.set_xlim(0, 10) # 시간 축은 시뮬레이션 진행에 따라 동적으로 변경
    ax2.set_ylim(0, m * g * initial_height * 1.1)
    ax2.set_xlabel("시간 (s)")
    ax2.set_ylabel("에너지 (J)")
    ax2.set_title("에너지 전환")
    line_pe, = ax2.plot([], [], label="위치 에너지 (PE)", color='blue')
    line_ke, = ax2.plot([], [], label="운동 에너지 (KE)", color='green')
    line_te, = ax2.plot([], [], label="총 역학적 에너지 (TE)", color='purple', linestyle='--')
    ax2.legend()
    ax2_text = ax2.text(0.05, 0.95, '', transform=ax2.transAxes, fontsize=10, verticalalignment='top')


    # 스트림릿에 그래프를 표시할 placeholder
    st_plot = st.pyplot(fig)

    # 시뮬레이션 루프
    while h_current > 0:
        # 시간 경과에 따른 위치 및 속도 업데이트 (등가속도 운동 공식)
        # v_new = v_current + g * time_step  # 아래 방향을 양수로
        # h_new = h_current - (v_current * time_step + 0.5 * g * time_step**2)

        # 더 정확한 방법: 운동 에너지와 위치 에너지 변환
        # h_current - h_new = v_current * time_step + 0.5 * g * time_step**2
        # v_new = sqrt(v_current**2 + 2 * g * (h_current - h_new))

        # 간단하게 시간 간격 동안의 변화 계산 (미분 방정식 근사)
        v_current += g * time_step
        h_current -= v_current * time_step # 떨어진 거리만큼 높이 감소

        if h_current < 0: # 바닥에 닿으면 멈춤
            h_current = 0
            v_current = 0

        t_current += time_step

        # 에너지 계산
        potential_energy = m * g * h_current
        kinetic_energy = 0.5 * m * v_current**2
        total_energy = potential_energy + kinetic_energy

        # 데이터 저장
        time_data.append(t_current)
        height_data.append(h_current)
        velocity_data.append(v_current)
        potential_energy_data.append(potential_energy)
        kinetic_energy_data.append(kinetic_energy)
        total_energy_data.append(total_energy)

        # Matplotlib 업데이트
        point.set_ydata(h_current)
        ax1_text.set_text(f'높이: {h_current:.2f} m\n속도: {v_current:.2f} m/s')

        line_pe.set_data(time_data, potential_energy_data)
        line_ke.set_data(time_data, kinetic_energy_data)
        line_te.set_data(time_data, total_energy_data)

        # X축 범위 동적 조절
        ax2.set_xlim(0, max(time_data) * 1.1 if time_data else 10)
        ax2_text.set_text(f'PE: {potential_energy:.2f} J\nKE: {kinetic_energy:.2f} J\nTE: {total_energy:.2f} J')


        # 스트림릿에 업데이트된 그래프 표시
        st_plot.pyplot(fig)

        time.sleep(time_step / animation_speed)

    st.success("시뮬레이션이 완료되었습니다!")
