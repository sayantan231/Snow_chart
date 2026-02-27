import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(page_title="Himalayan Snow Monitor", layout="wide")

st.title("🏔 Himalayan Snow Monitor - Live Supabase Integration")

@st.cache_data
def load_data():
    conn = psycopg2.connect(
        host=st.secrets["DB_HOST"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        port=st.secrets["DB_PORT"]
    )
    
    query = "SELECT * FROM snow_data;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

st.subheader("📊 Snow Data from Supabase")
st.dataframe(df, use_container_width=True)

fig = px.line(
    df,
    x="month",
    y="snow_percentage",
    color="year",
    markers=True,
    title="Monthly Snow Percentage Comparison"
)

st.plotly_chart(fig, use_container_width=True)
