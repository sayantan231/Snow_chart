import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Himalayan Snow Monitor", layout="wide")
st.title("🏔 Himalayan Snow Monitor - CSV Upload")
st.markdown("Compare monthly snow percentages for 2022 vs 2023")

# Upload CSV
uploaded_file = st.file_uploader("Upload your snow CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Raw Data")
    st.dataframe(df, use_container_width=True)

    # Reshape data for line chart
    if all(col in df.columns for col in ["month_name", "perc_2022", "perc_2023"]):
        df_long = df.melt(
            id_vars="month_name",
            value_vars=["perc_2022", "perc_2023"],
            var_name="year",
            value_name="snow_percentage"
        )

        # Clean year column to just 2022 / 2023
        df_long["year"] = df_long["year"].str.replace("perc_", "")

        # Line chart
        fig = px.line(
            df_long,
            x="month_name",
            y="snow_percentage",
            color="year",
            markers=True,
            title="Monthly Snow Percentage Comparison"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Yearly average
        avg = df_long.groupby("year")["snow_percentage"].mean().reset_index()
        st.subheader("📈 Average Snow % by Year")
        st.dataframe(avg, use_container_width=True)

        # Insight
        highest = df_long.loc[df_long["snow_percentage"].idxmax()]
        st.subheader("🔎 Insight")
        st.write(
            f"Highest snow recorded: {highest['snow_percentage']:.2f}% "
            f"in {highest['month_name']} {highest['year']}."
        )
    else:
        st.error("CSV must have columns: month_name, perc_2022, perc_2023")

else:
    st.info("Please upload your CSV to see the data.")
