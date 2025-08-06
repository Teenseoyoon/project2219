# admin.py
import streamlit as st
import sqlite3

import streamlit as st
import sqlite3

st.set_page_config(page_title="관리자 페이지", layout="centered")
st.title("🛠️ 관리자 도구")

# DB 테이블이 없으면 생성
def init_db():
    conn = sqlite3.connect("users.db")
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

init_db()

st.set_page_config(page_title="관리자 페이지", layout="centered")
st.title("🛠️ 관리자 도구")

# -------------------------------
# 관리자 인증
# -------------------------------
admin_name = st.text_input("🔑 관리자 이름을 입력하세요:", value="")

if admin_name.strip().lower() == "admin":
    st.success("✅ 관리자 인증 완료")

    # -------------------------------
    # 기능 1: 모든 유저 데이터 삭제
    # -------------------------------
    st.header("🔥 전체 유저 초기화")
    
    def reset_users_table():
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM users")  # 전체 삭제
        conn.commit()
        conn.close()

    if st.button("🧨 모든 유저 삭제 (복구 불가!)"):
        reset_users_table()
        st.success("✅ 모든 유저 데이터가 삭제되었습니다.")
        st.experimental_rerun()

    st.markdown("---")

    # -------------------------------
    # 기능 2: 특정 유저만 삭제
    # -------------------------------
    st.header("🗑️ 특정 유저 삭제")

    def get_all_users():
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("SELECT name FROM users")
        users = [row[0] for row in cur.fetchall()]
        conn.close()
        return users

    def delete_user_by_name(name):
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE name = ?", (name,))
        conn.commit()
        conn.close()

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
