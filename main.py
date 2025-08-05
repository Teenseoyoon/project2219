import streamlit as st
import json
import os

# Player 클래스 포함
class Player:
    def __init__(self, name, job):
        self.name = name
        self.job = job
        if job == "검사":
            self.hp = 120
            self.atk = 15
        elif job == "마법사":
            self.hp = 90
            self.atk = 20
        elif job == "거지":
            self.hp = 70
            self.atk = 5
        else:
            self.hp = 100
            self.atk = 10

    def to_dict(self):
        return {"name": self.name, "job": self.job, "hp": self.hp, "atk": self.atk}

# 사용자 정보 저장
def save_player(player):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{player.name}.json", "w", encoding="utf-8") as f:
        json.dump(player.to_dict(), f, ensure_ascii=False, indent=2)

# --- UI 시작 ---
st.set_page_config(page_title="모험 게임", layout="centered")
st.title("🎮 나만의 게임")

# 세션 상태 초기화
if "player" not in st.session_state:
    st.session_state.player = None

# 1단계: 이름 + 직업 선택
if st.session_state.player is None:
    name = st.text_input("플레이어 이름:")
    job = st.selectbox("직업 선택:", ["검사", "마법사", "거지"])

    if st.button("게임 시작"):
        if not name:
            st.warning("이름을 입력해주세요!")
        else:
            player = Player(name, job)
            st.session_state.player = player.to_dict()
            save_player(player)
            st.rerun()

# 2단계: 게임 화면
else:
    player = st.session_state.player
    st.subheader("🗺️ 맵 선택")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍜 식당"):
            st.success("식당으로 이동 중... (기능 예정)")
    with col2:
        if st.button("🏫 학교"):
            st.success("학교로 이동 중... (기능 예정)")
    with col3:
        if st.button("🗡️ 던전"):
            st.success("던전으로 이동 중... (기능 예정)")

    # 플레이어 정보 하단 표시
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; font-size: 18px;'>"
        f"🧍‍♂️ {player['name']} | 🪪 {player['job']} | ❤️ HP: {player['hp']} | ⚔️ ATK: {player['atk']}"
        f"</div>",
        unsafe_allow_html=True
    )

