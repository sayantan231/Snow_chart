import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Himalayan Snow Monitor", layout="wide")

st.title("🏔 Himalayan Snow Monitor - Uttarakhand")
st.markdown("Monthly Snow Cover Percentage Analysis (2022 vs 2023)")

uploaded_file = st.file_uploader("Upload Snow Data CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Raw Data")
    st.dataframe(df, use_container_width=True)

    # Line chart comparison
    fig = px.line(
        df,
        x="Month",
        y="Snow_Percentage",
        color="Year",
        markers=True,
        title="Monthly Snow Percentage Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Yearly average
    avg = df.groupby("Year")["Snow_Percentage"].mean().reset_index()

    st.subheader("📈 Average Snow % by Year")
    st.dataframe(avg, use_container_width=True)

    # Simple insight
    highest_month = df.loc[df["Snow_Percentage"].idxmax()]

    st.subheader("🔎 Insight")
    st.write(
        f"Highest snow recorded: {highest_month['Snow_Percentage']}% "
        f"in {highest_month['Month']} {highest_month['Year']}."
    )

else:
    st.info("Please upload your snow dataset CSV to begin.")
