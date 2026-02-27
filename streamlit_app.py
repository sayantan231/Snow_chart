import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(page_title="Himalayan Snow Monitor", layout="wide")

st.title("🏔 Himalayan Snow Monitor - Live Supabase Data")
st.markdown("Monthly Snow Cover Percentage Analysis (2022 vs 2023)")

# Connect to Supabase
@st.cache_data
def load_data():
    conn = psycopg2.connect(
        host=st.secrets["DB_HOST"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        port=st.secrets["DB_PORT"]
    )
    query = "SELECT * FROM snow_raw_data;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

# Show raw table
st.subheader("📊 Snow Data from Supabase")
st.dataframe(df, use_container_width=True)

# Line chart
fig = px.line(
    df,
    x="month_name",
    y="snow_percentage",
    color="year",
    markers=True,
    title="Monthly Snow Percentage Comparison"
)
st.plotly_chart(fig, use_container_width=True)

# Yearly average
avg = df.groupby("year")["snow_percentage"].mean().reset_index()
st.subheader("📈 Average Snow % by Year")
st.dataframe(avg, use_container_width=True)

# Insight
highest = df.loc[df["snow_percentage"].idxmax()]
st.subheader("🔎 Insight")
st.write(
    f"Highest snow recorded: {highest['snow_percentage']:.2f}% "
    f"in {highest['month_name']} {highest['year']}."
)
