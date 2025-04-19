# src/components/stores.py
import streamlit as st
import requests
import pandas as pd

@st.cache_data
def get_stores(location):
    stores_df = pd.read_csv("data/stores.csv")
    local_stores = stores_df[stores_df["city"].str.contains(location.split("都")[0], na=False)]
    stores = local_stores.to_dict("records")
    
    api_key = st.secrets["general"].get("GOOGLE_MAPS_API_KEY")
    if api_key:
        try:
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=garden+center+in+{location}&key={api_key}"
            response = requests.get(url).json().get("results", [])
            stores.extend([{"name": r["name"], "address": r["formatted_address"]} for r in response[:3]])
        except Exception as e:
            st.warning(f"Google Mapsエラー: {str(e)}")
    return stores if stores else [{"name": "なし", "address": "店舗が見つかりませんでした"}]
