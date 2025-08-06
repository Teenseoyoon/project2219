# admin.py
import streamlit as st
import sqlite3

# 파일 상단에 추가
DB_PATH = "users.db"


# -------------------------------
# [1] DB 테이블 생성 함수
# -------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            job TEXT,
            hp INTEGER,
            atk INTEGER,
            stage INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()  # 테이블 없으면 생성

# -------------------------------
# [2] 유저 목록 불러오기
# -------------------------------
def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM users")
    users = [row[0] for row in cur.fetchall()]
    conn.close()
    return users

# -------------------------------
# [3] 전체 삭제 함수
# -------------------------------
def reset_users_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users")
    conn.commit()
    conn.close()

# -------------------------------
# [4] 특정 유저 삭제 함수
# -------------------------------
def delete_user_by_name(name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE name = ?", (name,))
    conn.commit()
    conn.close()

# -------------------------------
# [5] 관리자 인증 입력
# -------------------------------
admin_name = st.text_input("🔑 관리자 이름을 입력하세요:", value="")

# -------------------------------
# [6] 관리자 페이지 본문
# -------------------------------
if admin_name.strip().lower() == "admin":
    st.success("✅ 관리자 인증 완료")

    # 🔥 전체 유저 삭제
    st.header("🧨 전체 유저 초기화")
    if st.button("🔥 모든 유저 삭제 (복구 불가!)"):
        reset_users_table()
        st.success("✅ 모든 유저 데이터가 삭제되었습니다.")
        st.experimental_rerun()

    st.markdown("---")

    # 🗑️ 특정 유저 삭제
    st.header("🗑️ 특정 유저 삭제")

    user_list = get_all_users()
    if user_list:
        selected_user = st.selectbox("👤 삭제할 유저를 선택하세요:", user_list)

        if st.button("🚫 선택한 유저 삭제"):
            delete_user_by_name(selected_user)
            st.success(f"✅ 유저 '{selected_user}' 가 삭제되었습니다.")
            st.experimental_rerun()
    else:
        st.info("현재 등록된 유저가 없습니다.")
else:
    st.warning("이 페이지는 관리자(admin)만 접근 가능합니다.")
