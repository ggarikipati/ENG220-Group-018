import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Group-018 | Air Quality and EPA Funding", layout="wide")
st.title("Group-018: Air Quality Trends and EPA Funding")

st.markdown("""
This project analyzes national and regional air quality trends in the U.S. and the corresponding EPA funding over the years.  
It uses multiple datasets sourced from the **EPA** to explore pollutant levels in **cities and counties**, track **budget allocations**,  
and visualize **applications and awards** of EPA grants across states and regions.
""")

# === File Loaders ===
def load_csv(folder, filename):
    base_dir = os.path.dirname(__file__)
    return pd.read_csv(os.path.join(base_dir, "datasets", folder, filename))

def load_city_data():
    base_dir = os.path.dirname(__file__)
    return pd.read_csv(os.path.join(base_dir, "datasets", "airqualitybycity2000-2023.csv"))

def load_county_data():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "datasets", "county_datasets")
    dfs = []
    for year in range(2000, 2024):
        file = f"conreport{year}.csv"
        path = os.path.join(data_dir, file)
        if os.path.exists(path):
            df = pd.read_csv(path)
            df['Year'] = year
            dfs.append(df)
    if not dfs:
        st.warning("County data files not found.")
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)

def load_national_pollutant(pollutant_name):
    file = f"{pollutant_name}National.csv"
    return load_csv("National_trend", file)

def load_applications_data():
    df = load_csv("finance", "airqualityapplications2024.csv")
    df['Proposed EPA Funding'] = df['Proposed EPA Funding'].replace('[\$,]', '', regex=True).astype(float) * 1000
    return df

def load_awards_data():
    df = load_csv("finance", "AirQualityDirectAwards2022.csv")
    df['Amount Awarded'] = df['Amount Awarded'].replace('[\$,]', '', regex=True).astype(float) * 1000
    return df

def load_budget_data():
    df = load_csv("finance", "EPAbudget.csv")
    df['Enacted Budget'] = df['Enacted Budget'].replace('[\$,]', '', regex=True).astype(float) * 1000
    return df

# === Tabs ===
tabs = st.tabs([
    "City Trends",
    "County Trends",
    "National Trends",
    "EPA Applications",
    "Awards Granted",
    "EPA Budget"
])

# === City Trends ===
with tabs[0]:
    st.subheader("City Air Quality (2000–2023)")
    city_df = load_city_data()
    city_df['CBSA'] = city_df['CBSA'].fillna(method='ffill')
    cities = city_df['CBSA'].unique().tolist()
    selected_cbsa = st.selectbox("Select City CBSA", sorted(cities))

    city_data = city_df[city_df['CBSA'] == selected_cbsa]
    pollutants = city_data['Pollutant'].unique()
    years = [str(y) for y in range(2000, 2024)]

    plt.figure(figsize=(10, 5))
    for pollutant in pollutants:
        pollutant_data = city_data[city_data['Pollutant'] == pollutant]
        values = pd.to_numeric(pollutant_data[years].iloc[0], errors='coerce')
        plt.plot(years, values, marker='o', label=pollutant)

    plt.title(f"Pollutant Levels in {selected_cbsa} (2000–2023)")
    plt.xlabel("Year")
    plt.ylabel("Level")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# === County Trends ===
with tabs[1]:
    st.subheader("County Pollutants (2000–2023)")
    county_df = load_county_data()
    if not county_df.empty:
        counties = sorted(county_df['County'].dropna().unique())
        selected_county = st.selectbox("Select County", counties)
        pollutants = [col for col in county_df.columns if col not in ['County Code', 'County', 'Year']]
        selected_pollutant = st.selectbox("Select Pollutant", pollutants)

        subset = county_df[county_df['County'] == selected_county][['Year', selected_pollutant]].dropna()

        plt.figure(figsize=(10, 5))
        plt.plot(subset['Year'], subset[selected_pollutant], marker='o')
        plt.title(f"{selected_pollutant} Trend in {selected_county}")
        plt.xlabel("Year")
        plt.ylabel(selected_pollutant)
        plt.grid(True)
        st.pyplot(plt)
        st.dataframe(subset.set_index("Year"))

# === National Trends ===
with tabs[2]:
    st.subheader("National Pollutant Trends (2000–2023)")
    pollutant = st.selectbox("Select Pollutant", ['CO', 'NO2', 'O3', 'PM10', 'PM25', 'SO2'])
    df = load_national_pollutant(pollutant)

    plt.figure(figsize=(10, 5))
    plt.plot(df['Year'], df['Mean'], label="Mean", marker='o')
    plt.plot(df['Year'], df['10th Percentile'], label="10th %", marker='x')
    plt.plot(df['Year'], df['90th Percentile'], label="90th %", marker='x')
    plt.title(f"National Trend for {pollutant}")
    plt.xlabel("Year")
    plt.ylabel(df['Units'].iloc[0] if 'Units' in df.columns else pollutant)
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# === EPA Applications ===
with tabs[3]:
    st.subheader("Air Quality Grant Applications (2024)")
    apps = load_applications_data()
    state_options = sorted(set(", ".join(apps["Project State(s)"].dropna()).split(", ")))
    selected_state = st.selectbox("Select State", state_options)

    filtered = apps[apps["Project State(s)"].str.contains(selected_state)]
    st.dataframe(filtered)

    plt.figure(figsize=(12, 6))
    plt.bar(filtered["Primary Applicant"], filtered["Proposed EPA Funding"], color="skyblue")
    plt.xticks(rotation=90)
    plt.ylabel("Funding ($)")
    plt.title(f"Proposed EPA Funding for {selected_state}")
    plt.tight_layout()
    st.pyplot(plt)

# === Awards Granted ===
with tabs[4]:
    st.subheader("Direct Awards (2022)")
    awards = load_awards_data()
    regions = awards['EPA Region'].dropna().unique().tolist()
    selected_region = st.selectbox("Select EPA Region", sorted(regions))
    region_data = awards[awards['EPA Region'] == selected_region]
    st.dataframe(region_data)

    plt.figure(figsize=(12, 6))
    plt.bar(region_data["Grant Recipient"], region_data["Amount Awarded"], color="orange")
    plt.xticks(rotation=90)
    plt.ylabel("Amount Awarded ($)")
    plt.title(f"Grants in EPA Region {selected_region}")
    plt.tight_layout()
    st.pyplot(plt)

# === EPA Budget ===
with tabs[5]:
    st.subheader("EPA Budget & Workforce (2000–2023)")
    budget_df = load_budget_data()
    st.dataframe(budget_df)

    plt.figure(figsize=(10, 5))
    plt.plot(budget_df['Fiscal Year'], budget_df['Enacted Budget'], marker='o', label="Enacted Budget")
    plt.title("EPA Enacted Budget Over the Years")
    plt.xlabel("Year")
    plt.ylabel("Budget ($)")
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)

    plt.figure(figsize=(10, 5))
    plt.plot(budget_df['Fiscal Year'], budget_df['Workforce'], marker='o', color="green", label="Workforce")
    plt.title("EPA Workforce Over the Years")
    plt.xlabel("Year")
    plt.ylabel("Number of Employees")
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)
