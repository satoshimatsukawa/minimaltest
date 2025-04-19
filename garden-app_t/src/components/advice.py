# src/components/advice.py
import streamlit as st
from openai import OpenAI
import json

@st.cache_data
def get_advice(location, plant):
    client = OpenAI(api_key=st.secrets["general"]["OPENAI_API_KEY"])
    try:
        with open("data/climate.json") as f:
            climate_data = json.load(f)
        climate = climate_data.get(location, {"temp": "不明", "humidity": "不明", "season": "不明"})
        prompt = f"""
        地域: {location} (気温: {climate['temp']}, 湿度: {climate['humidity']}, 季節: {climate['season']})
        植物: {plant}
        {plant}の栽培方法とポイントを簡潔に教えてください。日本語で、150文字以内。
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"アドバイス取得エラー: {str(e)}"
