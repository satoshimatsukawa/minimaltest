# src/components/auth.py
import streamlit as st
from supabase import create_client

def authenticate(supabase):
    if not st.session_state.get("user"):
        st.subheader("ログインまたはサインアップ")
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("ログイン"):
                try:
                    user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state["user"] = user
                    st.success("ログイン成功！")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"エラー: {str(e)}")
        with col2:
            if st.button("サインアップ"):
                try:
                    user = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("サインアップ成功！メールを確認してください。")
                except Exception as e:
                    st.error(f"エラー: {str(e)}")
        return False
    return True

def get_user_id():
    return st.session_state["user"].user.id if st.session_state.get("user") else None
