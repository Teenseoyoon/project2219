# admin.py
import streamlit as st
import sqlite3

st.set_page_config(page_title="관리자 페이지", layout="centered")
st.title("🛠️ 관리자 도구")

# 관리자 이름 입력 (간단한 인증)
admin_name = st.text_input("🔑 관리자 이름을 입력하세요:", value="")

# 데이터베이스 초기화 함수
def reset_users_table():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users")  # 모든 유저 삭제
    conn.commit()
    conn.close()

# 버튼 조건: 이름이 'admin'일 때만 작동
if admin_name.strip().lower() == "admin":
    st.success("✅ 관리자 인증 완료")

    if st.button("🔥 모든 유저 데이터 초기화"):
        reset_users_table()
        st.success("🧹 모든 유저 정보가 삭제되었습니다.")
else:
    st.warning("이 페이지는 관리자(admin)만 접근 가능합니다.")
