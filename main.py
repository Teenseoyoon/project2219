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

import streamlit as st
from db import init_db, get_user, add_user

init_db()

st.title("🎮 SQLite 로그인 시스템")

mode = st.radio("모드 선택", ["로그인", "회원가입"])
name = st.text_input("이름:")
password = st.text_input("비밀번호:", type="password")

# 로그인
if mode == "로그인":
    if st.button("로그인"):
        user = get_user(name)
        if user and user[1] == password:  # user = (name, password, job, hp, atk)
            st.success("로그인 성공!")
            st.session_state.player = {
                "name": user[0],
                "job": user[2],
                "hp": user[3],
                "atk": user[4]
            }
            st.experimental_rerun()
        else:
            st.error("이름 또는 비밀번호가 올바르지 않습니다.")

# 회원가입
else:
    job = st.selectbox("직업 선택:", ["검사", "마법사", "거지"])
    if st.button("회원가입"):
        if get_user(name):
            st.warning("이미 존재하는 사용자입니다.")
        else:
            if job == "검사":
                hp, atk = 120, 15
            elif job == "마법사":
                hp, atk = 90, 20
            else:
                hp, atk = 70, 5
            add_user(name, password, job, hp, atk)
            st.success("회원가입 완료! 로그인해주세요.")

# 로그인된 사용자 표시
if "player" in st.session_state:
    st.markdown("---")
    p = st.session_state["player"]
    st.markdown(
        f"<div style='text-align:center; font-size:18px;'>"
        f"🧍‍♂️ {p['name']} | 🪪 {p['job']} | ❤️ HP: {p['hp']} | ⚔️ ATK: {p['atk']}"
        f"</div>",
        unsafe_allow_html=True
    )

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

