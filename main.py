import streamlit as st
import os
import json
import sqlite3
import pandas as pd
from db import init_db, get_user, add_user
import random
import time
# ✅ 페이지 상태 초기화
if "page" not in st.session_state:
    st.session_state["page"] = "홈"
    
# -------------------------------
# Player 클래스 정의
# -------------------------------
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
        return {
            "name": self.name,
            "job": self.job,
            "hp": self.hp,
            "atk": self.atk
        }

# -------------------------------
# JSON 저장용 함수
# -------------------------------
def save_player(player):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{player.name}.json", "w", encoding="utf-8") as f:
        json.dump(player.to_dict(), f, ensure_ascii=False, indent=2)

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(page_title="모험 게임", layout="centered")
st.title("🎮 나만의 모험 게임")
init_db()

# -------------------------------
# 로그인 완료 상태: 게임 화면
# -------------------------------
if "player" in st.session_state:
    p = st.session_state["player"]
    power = p['hp'] + p['atk']
    if st.session_state["page"] == "홈":
        st.markdown("---")
        st.markdown(
            f"<div style='text-align:center; font-size:18px;'>"
            f"🧍‍♂️ {p['name']} | 🪪 {p['job']} | ❤️ HP: {p['hp']} | ⚔️ ATK: {p['atk']} | 💥 전투력: {power}"
            f"</div>",
            unsafe_allow_html=True
        )

        st.subheader("🗺️ 맵 선택")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🍜 식당"):
                st.session_state["page"] = "식당"
                st.rerun()
        with col2:
            if st.button("🏫 학교"):
                st.session_state["page"] = "식당"
                st.rerun("학교")
        with col3:
            if st.button("🗡️ 던전"):
                st.session_state["page"] = "식당"
                st.rerun("던전")

        if st.button("로그아웃"):
            st.session_state.clear()
            st.rerun()
            
    elif st.session_state["page"] == "식당":

        if "gauge" not in st.session_state:
            st.session_state["gauge"] = 0

        st.title("🍜 식당에 오신 걸 환영합니다!")
        st.markdown("음식을 먹어 체력을 회복하세요! (게이지가 5가 되면 HP 회복 효과 발생)")
        
        if "boost_result" in st.session_state:
            result = st.session_state["boost_result"]
            st.markdown(
                f"""
                <div style='text-align:center; font-size:32px; color:{result['color']}; font-weight:bold;'>
                {result['msg']}<br>❤️ HP +{result['amount']}
                </div>
                """,
                unsafe_allow_html=True
            )
        col_food1, col_food2, col_food3 = st.columns(3)
        with col_food1:
            if st.button("🍙 삼각김밥"):
                st.session_state["gauge"] += 1
        with col_food2:
            if st.button("🍜 라면"):
                st.session_state["gauge"] += 1
        with col_food3:
            if st.button("🥟 만두"):
                st.session_state["gauge"] += 1

        st.progress(st.session_state["gauge"] / 5)

        if st.session_state["gauge"] >= 5:
            boost = random.randint(1, 50)
            st.session_state["player"]["hp"] += boost
            st.session_state["gauge"] = 0

            if boost <= 15:
                msg = "동혁이가 씻지 않은 손으로 만든 손만두"
                color = "brown"
            elif boost <= 30:
                msg = "서윤이가 2달간 사물함에 보관해둔 간식"
                color = "green"
            elif boost <= 40:
                msg = "목욕 끝나고 먹는 요구르트"
                color = "skyblue"
            else:
                msg = "영양사 선생님의 48년 전통 해장국"
                color = "gold"
                
            st.session_state["boost_result"] = {
                "msg": msg,
                "color": color,
                "amount": boost
            }
            
            st.rerun()

        st.markdown("---")
        st.markdown(f"❤️ 현재 HP: **{st.session_state['player']['hp']}**")

        if st.button("🔙 돌아가기"):
            st.session_state["page"] = "홈"
            st.rerun()

# -------------------------------
# 로그인되지 않은 경우: 회원가입/로그인/직접 생성
# -------------------------------
else:
    st.subheader("👤 로그인 / 회원가입")
    mode = st.radio("모드 선택", ["로그인", "회원가입"])
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

# -------------------------------
# 디버깅/관리용: 랭킹 보기
# -------------------------------
st.markdown("---")

if st.checkbox("📂 랭킹 보기"):
    conn = sqlite3.connect("users.db")
    df = pd.read_sql_query("SELECT *, (hp + atk) as 전투력 FROM users ORDER BY 전투력 DESC", conn)
    conn.close()
    st.dataframe(df)

st.write("📁 현재 디렉토리:", os.getcwd())
