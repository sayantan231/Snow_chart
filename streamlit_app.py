import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Himalayan Snow Monitor", layout="wide")
st.title("🏔 Himalayan Snow Monitor - CSV Upload")
st.markdown("Upload your snow data CSV to visualize monthly snow coverage")

# Upload CSV
uploaded_file = st.file_uploader("Upload your snow CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Raw Data")
    st.dataframe(df, use_container_width=True)

    # Line chart
    if "month_name" in df.columns and "snow_percentage" in df.columns and "year" in df.columns:
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
    else:
        st.error("CSV must have columns: month_name, year, snow_percentage")

else:
    st.info("Please upload your CSV to see the data.")
