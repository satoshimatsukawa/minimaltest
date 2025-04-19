# src/app.py
import streamlit as st
from supabase_py import create_client, Client
from components.auth import authenticate, get_user_id
from components.posts import create_post, post_feed
from components.advice import get_advice
from components.stores import get_stores

# Supabase初期化
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(url, key)

# CSS
with open("src/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# タイトル
st.title("🌱 家庭菜園アプリ")

# 認証
if not authenticate(supabase):
    st.stop()

user_id = get_user_id()

# サイドバー
st.sidebar.title("メニュー")
page = st.sidebar.radio("選択", ["ホーム", "投稿", "アドバイス"])

# ページ
if page == "ホーム":
    st.markdown(
        "<div class='card' style='max-width: 500px; margin: 0 auto;'>"
        "ようこそ！投稿をシェアしたり、アドバイスをチェックしよう！"
        "</div>",
        unsafe_allow_html=True
    )
elif page == "投稿":
    create_post(supabase, user_id)
    post_feed(supabase, user_id)
elif page == "アドバイス":
    st.subheader("栽培アドバイス")
    with st.form(key="advice_form"):
        location = st.selectbox("居住地", ["東京都", "北海道"])
        plant = st.selectbox("植物", ["トマト", "バジル", "レタス"])
        submit = st.form_submit_button("アドバイスを表示")
        if submit:
            advice = get_advice(location, plant)
            st.markdown(f"<div class='card' style='max-width: 500px;'>{advice}</div>", unsafe_allow_html=True)
            stores = get_stores(location)
            st.markdown("<div class='card' style='max-width: 500px;'><h3>近くの店舗</h3>", unsafe_allow_html=True)
            for store in stores:
                st.markdown(f"- **{store['name']}**<br>住所: {store['address']}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# リアルタイム更新
def on_post_update(payload):
    st.experimental_rerun()
supabase.table("posts").on("UPDATE", on_post_update).subscribe()
