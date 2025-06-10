import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# --- 물리 상수 설정 ---
G = 9.81  # 중력 가속도 (m/s^2)
MASS = 1.0   # 물체의 질량 (kg)

# --- Streamlit 페이지 설정 ---
st.set_page_config(layout="wide", page_title="역학적 에너지 보존 시뮬레이션")
st.title("역학적 에너지 보존 시뮬레이션 (자유 낙하)")
st.markdown("---") # 구분선 추가

# --- 사이드바 설정 (사용자 입력) ---
st.sidebar.header("시뮬레이션 설정")
initial_height = st.sidebar.slider("초기 높이 (m)", 1.0, 100.0, 50.0, 1.0)
time_step = st.sidebar.slider("시간 간격 (s)", 0.01, 0.1, 0.05, 0.01)
animation_speed = st.sidebar.slider("애니메이션 속도 (배속)", 0.1, 5.0, 1.0, 0.1)

# 시뮬레이션 시작 버튼
start_button = st.sidebar.button("시뮬레이션 시작")

# --- 시뮬레이션 실행 로직 ---
if start_button:
    st.subheader("물체의 운동 및 에너지 전환 과정")

    # 초기 조건 설정
    current_height = initial_height
    current_velocity = 0.0 # 자유 낙하이므로 초기 속도는 0
    current_time = 0.0

    # 데이터 저장을 위한 리스트
    time_data = []
    height_data = []
    potential_energy_data = []
    kinetic_energy_data = []
    total_energy_data = []

    # Matplotlib Figure 및 Axes 설정
    # 두 개의 서브플롯: 물체 위치 시각화, 에너지 그래프
    fig, (ax_pos, ax_energy) = plt.subplots(2, 1, figsize=(10, 8))
    fig.tight_layout(pad=3.0) # 서브플롯 간 여백 설정

    # ax_pos: 물체 위치 시각화 (상단 플롯)
    ax_pos.set_xlim(-1, 1) # 물체는 수직으로만 움직이므로 X축은 고정
    ax_pos.set_ylim(0, initial_height * 1.1) # 초기 높이보다 약간 여유 있게 설정
    ax_pos.set_xlabel("X (임의의 좌표)")
    ax_pos.set_ylabel("높이 (m)")
    ax_pos.set_title("물체의 운동")
    # 물체를 나타내는 점 (빨간색 원)
    point, = ax_pos.plot(0, current_height, 'o', color='red', markersize=10)
    # 물체의 현재 높이와 속도를 표시할 텍스트
    pos_text = ax_pos.text(0.05, 0.95, '', transform=ax_pos.transAxes, fontsize=10, verticalalignment='top')

    # ax_energy: 에너지 그래프 시각화 (하단 플롯)
    # 초기 에너지 값의 110%까지 Y축 범위 설정
    ax_energy.set_ylim(0, MASS * G * initial_height * 1.1)
    ax_energy.set_xlabel("시간 (s)")
    ax_energy.set_ylabel("에너지 (J)")
    ax_energy.set_title("에너지 전환")
    # 각 에너지 라인 초기화
    line_pe, = ax_energy.plot([], [], label="위치 에너지 (PE)", color='blue')
    line_ke, = ax_energy.plot([], [], label="운동 에너지 (KE)", color='green')
    line_te, = ax_energy.plot([], [], label="총 역학적 에너지 (TE)", color='purple', linestyle='--')
    ax_energy.legend()
    # 각 에너지 값을 표시할 텍스트
    energy_text = ax_energy.text(0.05, 0.95, '', transform=ax_energy.transAxes, fontsize=10, verticalalignment='top')


    # Streamlit에 Matplotlib 그래프를 표시할 Placeholder
    st_plot_placeholder = st.pyplot(fig)

    # --- 시뮬레이션 루프 ---
    while current_height > 0:
        # 시간 경과에 따른 속도 업데이트 (중력 가속도 G 적용)
        current_velocity += G * time_step
        # 업데이트된 속도에 따라 높이 감소
        current_height -= current_velocity * time_step

        # 물체가 바닥(높이 0)에 닿으면 멈춤
        if current_height < 0:
            current_height = 0
            current_velocity = 0 # 바닥에 닿으면 속도도 0이 됨

        current_time += time_step

        # 에너지 계산
        potential_energy = MASS * G * current_height
        kinetic_energy = 0.5 * MASS * current_velocity**2
        total_energy = potential_energy + kinetic_energy

        # 데이터 추가
        time_data.append(current_time)
        height_data.append(current_height)
        potential_energy_data.append(potential_energy)
        kinetic_energy_data.append(kinetic_energy)
        total_energy_data.append(total_energy)

        # Matplotlib 플롯 데이터 업데이트
        point.set_ydata(current_height) # 물체 위치 업데이트
        pos_text.set_text(f'높이: {current_height:.2f} m\n속도: {current_velocity:.2f} m/s')

        line_pe.set_data(time_data, potential_energy_data)
        line_ke.set_data(time_data, kinetic_energy_data)
        line_te.set_data(time_data, total_energy_data)

        # 에너지 그래프의 X축 (시간) 범위 동적 조절
        ax_energy.set_xlim(0, max(time_data) * 1.1 if time_data else 10)
        energy_text.set_text(f'PE: {potential_energy:.2f} J\nKE: {kinetic_energy:.2f} J\nTE: {total_energy:.2f} J')

        # Streamlit에 업데이트된 그래프 다시 그리기
        st_plot_placeholder.pyplot(fig)

        # 애니메이션 속도 조절을 위한 딜레이
        time.sleep(time_step / animation_speed)

    st.success("시뮬레이션이 완료되었습니다! 물체가 바닥에 도달했습니다.")
    st.markdown("---")
    st.info(f"최종 높이: {current_height:.2f} m, 최종 속도: {current_velocity:.2f} m/s")
    st.info(f"총 시뮬레이션 시간: {current_time:.2f} 초")

    # 시뮬레이션 결과 요약 그래프 (선택 사항)
    st.subheader("최종 에너지 변화 요약")
    fig_summary, ax_summary = plt.subplots(figsize=(10, 5))
    ax_summary.plot(time_data, potential_energy_data, label="위치 에너지 (PE)", color='blue')
    ax_summary.plot(time_data, kinetic_energy_data, label="운동 에너지 (KE)", color='green')
    ax_summary.plot(time_data, total_energy_data, label="총 역학적 에너지 (TE)", color='purple', linestyle='--')
    ax_summary.set_xlabel("시간 (s)")
    ax_summary.set_ylabel("에너지 (J)")
    ax_summary.set_title("시간에 따른 에너지 변화")
    ax_summary.legend()
    ax_summary.grid(True)
    st.pyplot(fig_summary)
