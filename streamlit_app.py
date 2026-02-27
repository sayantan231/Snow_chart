import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client

st.set_page_config(page_title="Himalayan Snow Monitor", layout="wide")
st.title("🏔 Himalayan Snow Monitor - Live Supabase API")

# Connect to Supabase
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)

# Fetch data
data = supabase.table("snow_raw_data").select("*").execute()
df = pd.DataFrame(data.data)

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
