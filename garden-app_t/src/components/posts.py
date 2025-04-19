# src/components/posts.py
import streamlit as st
from supabase import create_client
from datetime import datetime
from PIL import Image
import io

def create_post(supabase, user_id):
    st.subheader("新しい投稿")
    with st.form(key="post_form", clear_on_submit=True):
        plant = st.selectbox("植物", ["トマト", "バジル", "レタス"])
        uploaded_file = st.file_uploader("写真をアップロード", type=["jpg", "png"])
        submit = st.form_submit_button("投稿")
        if submit and uploaded_file:
            try:
                image_name = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                image_data = uploaded_file.getvalue()
                supabase.storage.from_("images").upload(image_name, image_data, file_options={"content-type": "image/jpeg"})
                image_url = supabase.storage.from_("images").get_public_url(image_name)
                data = {
                    "user_id": user_id,
                    "plant": plant,
                    "image_url": image_url,
                    "created_at": datetime.now().isoformat(),
                    "likes": 0
                }
                supabase.table("posts").insert(data).execute()
                st.success("投稿しました！")
            except Exception as e:
                st.error(f"投稿エラー: {str(e)}")

def post_feed(supabase, user_id):
    st.subheader("みんなの投稿")
    posts = supabase.table("posts").select("*").order("created_at", desc=True).execute().data
    if posts:
        column_count = 3 if st.get_option("client.displayWidth") > 600 else 1
        cols = st.columns(column_count)
        for i, post in enumerate(posts):
            with cols[i % column_count]:
                st.markdown(
                    f"""
                    <div class='card'>
                        <img src='{post['image_url']}' alt='{post['plant']}'>
                        <p>{post['plant']}</p>
                        <div class='like-container'>
                            <button class='like-button'>♥</button>
                            <span class='like-count'>{post['likes']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button("いいね", key=f"like_{post['id']}"):
                    try:
                        new_likes = post["likes"] + 1
                        supabase.table("posts").update({"likes": new_likes}).eq("id", post["id"]).execute()
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"いいねエラー: {str(e)}")
    else:
        st.write("まだ投稿がありません。")
