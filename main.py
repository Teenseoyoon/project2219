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
            st.experimental_rerun()
# db.py
import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            job TEXT,
            hp INTEGER,
            atk INTEGER
        )
    """)
    conn.commit()
    conn.close()

def get_user(name):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(name, password, job, hp, atk):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (name, password, job, hp, atk))
    conn.commit()
    conn.close()

import streamlit as st
from db import init_db, get_user, add_user

# DB 초기화
init_db()

st.title("🎮 SQLite 로그인 시스템")

# 로그인/회원가입 모드 선택
mode = st.radio("모드 선택", ["로그인", "회원가입"])

# 입력창
name = st.text_input("이름:")
password = st.text_input("비밀번호:", type="password")

# 회원가입 모드일 경우 직업 선택
if mode == "회원가입":
    job = st.selectbox("직업을 선택하세요:", ["검사", "마법사", "거지"])
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

# 로그인 처리
elif mode == "로그인":
    if st.button("로그인"):
        user = get_user(name)
        if user and user[1] == password:  # user[1]은 password
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

# 로그인된 사용자 정보 출력
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
