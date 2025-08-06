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
        if job == "최동혁":
            self.hp = 12
            self.atk = 15
        elif job == "강민구 T":
            self.hp = 800
            self.atk = 200
        elif job == "최지혜 T":
            self.hp = 300
            self.atk = 1400
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
                st.session_state["page"] = "학교"
                st.rerun()
        with col3:
            if st.button("🗡️ 던전"):
                st.session_state["page"] = "던전"
                st.rerun()

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
            if st.button("🍙정민이네 삼각김밥"):
                st.session_state["gauge"] += 1
        with col_food2:
            if st.button("🍜우석석이네 라면"):
                st.session_state["gauge"] += 1
        with col_food3:
            if st.button("🥟희준이네 만두"):
                st.session_state["gauge"] += 1

        st.progress(st.session_state["gauge"] / 5)

        if st.session_state["gauge"] >= 5:
            boost = random.randint(1, 50)
            st.session_state["player"]["hp"] += boost

            conn = sqlite3.connect("users.db")
            cur = conn.cursor()
            cur.execute("UPDATE users SET hp = ? WHERE name = ?", (st.session_state["player"]["hp"], st.session_state["player"]["name"]))
            conn.commit()
            conn.close()

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
        
    elif st.session_state["page"] == "학교":

        st.title("🏫 학교에 오신 걸 환영합니다!")
        st.markdown("훈련을 통해 공격력을 강화하세요! (게이지가 3이 되면 ATK 증가 효과 발생)")

        if "school_gauge" not in st.session_state:
            st.session_state["school_gauge"] = 0
    
        if "train_result" in st.session_state:
            result = st.session_state["train_result"]
            st.markdown(
                f"""
                <div style='text-align:center; font-size:32px; color:{result['color']}; font-weight:bold;'>
                {result['msg']}<br>⚔️ ATK +{result['amount']}
                </div>
                """,
                unsafe_allow_html=True
            )
        
        col_train1, col_train2, col_train3 = st.columns(3)
        with col_train1:
            if st.button("📚원준이의 수학 과외"):
                st.session_state["school_gauge"] += 1
        with col_train2:
            if st.button("💻진호의 국어 과외"):
                st.session_state["school_gauge"] += 0
        with col_train3:
            if st.button("💪민욱쌤의 영어 과외"):
                st.session_state["school_gauge"] += 1

        st.progress(st.session_state["school_gauge"] / 3)

        if st.session_state["school_gauge"] >= 3:
            boost = random.randint(1, 100)
            st.session_state["player"]["atk"] += boost

            conn = sqlite3.connect("users.db")
            cur = conn.cursor()
            cur.execute("UPDATE users SET atk = ? WHERE name = ?", (st.session_state["player"]["atk"], st.session_state["player"]["name"]))
            conn.commit()
            conn.close()

            st.session_state["school_gauge"] = 0

            if boost <= 10:
                msg = "Zzz... 자버렸다!"
                color = "gray"
            elif boost <= 20:
                msg = "오늘은 피타고라스 정리를 배웠다! a = b + c"
                color = "lightgreen"
            else:
                msg = "..이루 말할 수 없는 풀이를 여백이 부족하여..."
                color = "orange"

            st.session_state["train_result"] = {
                "msg": msg,
                "color": color,
                "amount": boost
            }

            st.rerun()

        # 현재 ATK 표시
        st.markdown("---")
        st.markdown(f"⚔️ 현재 ATK: **{st.session_state['player']['atk']}**")

        if st.button("🔙 돌아가기"):
            st.session_state["page"] = "홈"
            st.rerun()
                
    elif st.session_state["page"] == "던전":
        st.title("🗡️ 던전에 도전합니다!")

        # 스테이지 저장
        if "stage" not in st.session_state:
            st.session_state["stage"] = 1
        stage = st.session_state["stage"]

        # 몬스터 능력 설정
        base_monster_hp = 100
        base_monster_atk = 10
        monster = {
            "name": random.choice(["고블린", "슬라임", "늑대", "마왕의 그림자"]),
            "hp": base_monster_hp + (stage - 1) * 200,
            "atk": base_monster_atk + (stage - 1) * 50
        }

        st.markdown(f"👹 스테이지 {stage} 몬스터: **{monster['name']}**")
        st.markdown(f"❤️ HP: {monster['hp']} | ⚔️ ATK: {monster['atk']}")

        if st.button("⚔️ 전투 시작"):
            player = st.session_state["player"]
            original_hp = player["hp"]

            # 전투 로그 저장용
            battle_log = []
            turn = 1

            monster_hp = monster["hp"]
            player_hp = player["hp"]

            while player_hp > 0 and monster_hp > 0:
                log = f"🎯 [턴 {turn}]"

                # 플레이어 공격
                crit_player = random.random() < 0.2
                damage_to_monster = player["atk"] * (2 if crit_player else 1)
                monster_hp -= damage_to_monster
                log += f"\n🧍‍♂️ 플레이어 공격! {'💥크리티컬! ' if crit_player else ''}-{damage_to_monster} → 몬스터 HP: {max(monster_hp, 0)}"

                # 몬스터 생존 시 반격
                if monster_hp > 0:
                    crit_monster = random.random() < 0.5
                    damage_to_player = monster["atk"] * (2 if crit_monster else 1)
                    player_hp -= damage_to_player
                    log += f"\n👹 몬스터 반격! {'💥강타! ' if crit_monster else ''}-{damage_to_player} → 플레이어 HP: {max(player_hp, 0)}"
                else:
                    log += "\n✅ 몬스터 쓰러짐!"

                battle_log.append(log)
                turn += 1

            # 로그 출력 (한 턴씩 천천히 출력)
            for entry in battle_log:
                st.markdown("---")
                st.markdown(f"<pre>{entry}</pre>", unsafe_allow_html=True)
                time.sleep(0.1)  # 0.1초 간격으로 천천히 보여줌

            # 승패 판정
            if player_hp > 0:
                st.success(f"🎉 스테이지 {stage} 클리어 성공!")
                st.session_state["stage"] += 1
                
                # DB에서 기존 최고 스테이지 확인
                conn = sqlite3.connect("users.db")
                cur = conn.cursor()
                cur.execute("SELECT stage FROM users WHERE name = ?", (player["name"],))
                saved_stage = cur.fetchone()[0]
                # 최고 스테이지 갱신 필요 시 업데이트
                if st.session_state["stage"] > saved_stage:
                    cur.execute("UPDATE users SET stage = ? WHERE name = ?", (st.session_state["stage"], player["name"]))
                conn.commit()
                conn.close()
            else:
                st.error("💀 패배! 다음에 다시 도전하세요.")

            # HP 복원
            player["hp"] = original_hp

            if st.button("🔙 돌아가기"):
                st.session_state["page"] = "홈"
                st.rerun()
                
        if st.button("🏠 홈으로 돌아가기"):
            st.session_state["page"] = "홈"
            st.rerun()

else:
    st.subheader("👤 로그인 / 회원가입")
    mode = st.radio("모드 선택", ["로그인", "회원가입"])
    name = st.text_input("이름:")
    password = st.text_input("비밀번호:", type="password")

    if mode == "회원가입":
        job = st.selectbox("직업 선택:", ["최동혁", "강민구 T", "최지혜 T"])
        if st.button("회원가입"):
            if get_user(name):
                st.warning("이미 존재하는 이름입니다.")
            else:
                if job == "최동혁":
                    hp, atk = 12, 15
                elif job == "강민구 T":
                    hp, atk = 800, 200
                else:
                    hp, atk = 300, 1400
                add_user(name, password, job, hp, atk, 1)
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
                    "stage": user[5]
                }
                st.success(f"{user[0]}님 환영합니다!")
                st.rerun()
            else:
                st.error("이름 또는 비밀번호가 틀렸습니다.")

# -------------------------------
# 디버깅/관리용: 랭킹 보기
# -------------------------------
st.markdown("---")

if st.checkbox("🏆 랭킹 보기"):
    conn = sqlite3.connect("users.db")
    df = pd.read_sql_query("SELECT *, (hp + atk) as 전투력 FROM users ORDER BY 전투력 DESC", conn)
    conn.close()
    st.dataframe(df)

    st.subheader("📊 전체 유저 랭킹")
    st.dataframe(df)
  
    if st.button("🏅 순위로 보기 (Top 5 전투력 그래프)"):
        import plotly.express as px
        top5 = df.head(5)

        # 순위별 색상 지정
        colors = ['red', 'silver', 'peru', 'skyblue', 'lightgreen']

        # 막대그래프용 데이터프레임 구성
        chart_data = pd.DataFrame({
                "이름": top5["name"],
                "전투력": top5["전투력"],
                "색상": colors
            })

        fig = px.bar(chart_data, x="이름", y="전투력", color="이름",
                         color_discrete_sequence=colors,
                         title="🏆 Top 5 전투력 순위")

        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.write("📁 현재 디렉토리:", os.getcwd())
