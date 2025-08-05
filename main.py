import streamlit as st
import json
import os
import streamlit as st
from db import init_db, get_user, add_user


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
st.title("🎮 SQLite 로그인 시스템")

# DB 초기화
init_db()

# 로그인/회원가입 모드 선택
mode = st.radio("모드 선택", ["로그인", "회원가입"])

# 입력창
name = st.text_input("이름:")
password = st.text_input("비밀번호:", type="password")

# ✅ 플레이어가 세션에 있으면 게임 화면 보여줌
if "player" in st.session_state:
    p = st.session_state["player"]

    st.markdown("---")
    st.markdown(
        f"<div style='text-align:center; font-size:18px;'>"
        f"🧍‍♂️ {p['name']} | 🪪 {p['job']} | ❤️ HP: {p['hp']} | ⚔️ ATK: {p['atk']}"
        f"</div>",
        unsafe_allow_html=True
    )

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

    if st.button("로그아웃"):
        st.session_state.clear()
        st.rerun()

# ✅ 세션에 플레이어가 없으면 로그인/회원가입 or 직접 생성
else:
    st.title("🎮 로그인 또는 새로 시작")

    mode = st.radio("모드 선택", ["로그인", "회원가입", "직접 생성"])
    name = st.text_input("이름:")
    password = st.text_input("비밀번호:", type="password")

    if mode == "직접 생성":
        job = st.selectbox("직업 선택:", ["검사", "마법사", "거지"])
        if st.button("게임 시작"):
            player = Player(name, job)
            st.session_state["player"] = player.to_dict()
            save_player(player)
            st.rerun()

    elif mode == "회원가입":
        job = st.selectbox("직업 선택:", ["검사", "마법사", "거지"])
        if st.button("회원가입"):
            if get_user(name):
                st.warning("이미 존재하는 이름입니다.")
            else:
                if job == "검사":
                    hp, atk = 120, 15
                elif job == "마법사":
                    hp, atk = 90, 20
                else:
                    hp, atk = 70, 5
                add_user(name, password, job, hp, atk)
                st.success("회원가입 완료! 로그인해주세요.")

    elif mode == "로그인":
        if st.button("로그인"):
            user = get_user(name)
            if user and user[1] == password:
                st.session_state["player"] = {
                    "name": user[0],
                    "job": user[2],
                    "hp": user[3],
                    "atk": user[4],
                }
                st.success(f"{user[0]}님 환영합니다!")
                st.rerun()
            else:
                st.error("이름 또는 비밀번호가 틀렸습니다.")

    # 플레이어 정보 하단 표시
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; font-size: 18px;'>"
        f"🧍‍♂️ {player['name']} | 🪪 {player['job']} | ❤️ HP: {player['hp']} | ⚔️ ATK: {player['atk']}"
        f"</div>",
        unsafe_allow_html=True
    )

import sqlite3
import pandas as pd

st.markdown("---")
st.write("📁 현재 디렉토리:", os.getcwd())
st.write("📦 users.db 파일 있음?", os.path.exists("users.db"))

if st.checkbox("📂 저장된 유저 보기"):
    conn = sqlite3.connect("users.db")
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    st.dataframe(df)
