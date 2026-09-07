import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="MoCA & Aviation News", layout="wide")

# Connect to Database securely using Streamlit Secrets
@st.cache_resource
def init_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_connection()

# Fetch latest data
def load_data():
    response = supabase.table("viral_news").select("*").order("published_at", desc=True).limit(50).execute()
    return pd.DataFrame(response.data)

st.title("✈️ Indian Aviation Real-Time Dashboard")
st.markdown("Live tracking of MoCA, DGCA, and major Indian airlines.")

df = load_data()

if not df.empty:
    # Filter out low-impact news
    viral_df = df[df['score'] >= 50]
    
    st.subheader("🔥 High-Impact Alerts (Potential Virality)")
    for idx, row in viral_df.iterrows():
        st.error(f"**[{row['score']} Score]** [{row['title']}]({row['url']})")

    st.subheader("📰 Recent Mentions Stream")
    st.dataframe(df[['published_at', 'title', 'source', 'score']], use_container_width=True, hide_index=True)
else:
    st.write("Awaiting first data scrape...")