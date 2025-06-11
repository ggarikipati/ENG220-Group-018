import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


st.title("Group-018")

st.markdown("""
This dashboard explores air quality trends in U.S. cities and counties from 2000 to 2023.  
It includes pollutant trends, EPA budget data, direct awards, and application funding.  
Datasets were collected from EPA, CDC, and other government sources.
""")

# === Utility functions ===
def load_csv(folder, filename):
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "datasets", folder, filename)
    return pd.read_csv(path)

def load_city_data():
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "datasets", "airqualitybycity2000-2023.csv")
    df = pd.read_csv(path)
    df['CBSA'].fillna(method='ffill', inplace=True)
    df['Core Based Statistical Area'].fillna(method='ffill', inplace=True)
    return df.dropna(subset=['Pollutant', 'Trend Statistic'])

def load_multiple_csvs(prefix, start, end):
    base_dir = os.path.dirname(__file__)
    dfs = []
    for year in range(start, end + 1):
        path = os.path.join(base_dir, "datasets", "county_datasets", f"{prefix}{year}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            df['Year'] = year
            df.replace('.', pd.NA, inplace=True)
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def load_national_pollutant(pollutant_name):
    filenames = {
        'CO': 'Carbon_MonoxideNational.csv',
        'NO2': 'Nitrogen_DioxideNational.csv',
        'O3': 'OzoneNational.csv',
        'PM10': 'PM10National.csv',
        'PM25': 'PM25National.csv',
        'SO2': 'Sulfur_DioxideNational.csv',
    }
    file = filenames.get(pollutant_name)
    if not file:
        st.error(f"No file mapped for pollutant {pollutant_name}")
        return pd.DataFrame()
    return load_csv("National_trend", file)

# === Load datasets ===
city_data = load_city_data()
county_data = load_multiple_csvs("conreport", 2000, 2023)

# === Tabs ===
tabs = st.tabs(["City Trends", "County Trends", "National Trends", "Applications", "Awards", "EPA Budget"])

# --- Tab 1: City Trends ---
with tabs[0]:
    st.subheader("City Air Quality Trends (2000–2023)")
    cities = city_data['CBSA'] + " - " + city_data['Core Based Statistical Area']
    selected_city = st.selectbox("Select a City", sorted(cities.unique()))
    cbsa_code = selected_city.split(" - ")[0]
    city_filtered = city_data[city_data['CBSA'] == cbsa_code]

    st.write(f"Pollutant trends for {selected_city}:")
    years = [str(y) for y in range(2000, 2024)]
    fig, ax = plt.subplots(figsize=(12, 6))
    for _, row in city_filtered.iterrows():
        yvals = pd.to_numeric(row[4:], errors='coerce').fillna(0)
        ax.plot(years, yvals, label=f"{row['Pollutant']} ({row['Trend Statistic']})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Pollutant Level")
    ax.set_title(f"Pollutant Trends in {selected_city}")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# --- Tab 2: County Trends ---
with tabs[1]:
    st.subheader("County Air Quality Trends (2000–2023)")
    if not county_data.empty:
        county = st.selectbox("Select a County", sorted(county_data['County'].dropna().unique()))
        pollutant = st.selectbox("Select a Pollutant", [col for col in county_data.columns if col not in ['County', 'County Code', 'Year']])
        df = county_data[county_data['County'] == county][['Year', pollutant]].dropna()
        if df.empty:
            st.warning("Not enough data for this selection.")
        else:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df['Year'], df[pollutant], marker='o')
            ax.set_title(f"{pollutant} in {county}")
            ax.set_xlabel("Year")
            ax.set_ylabel(pollutant)
            ax.grid(True)
            st.pyplot(fig)
            st.dataframe(df.set_index("Year"))

# --- Tab 3: National Trends ---
with tabs[2]:
    st.subheader("National Pollutant Trends (2000–2023)")
    selected_pollutant = st.selectbox("Choose Pollutant", ["CO", "NO2", "O3", "PM10", "PM25", "SO2"])
    national_df = load_national_pollutant(selected_pollutant)
    if not national_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(national_df['Year'], national_df['Mean'], label="Mean", marker='o')
        ax.plot(national_df['Year'], national_df['10th Percentile'], label="10th Percentile", marker='x')
        ax.plot(national_df['Year'], national_df['90th Percentile'], label="90th Percentile", marker='s')
        ax.set_xlabel("Year")
        ax.set_ylabel(national_df['Units'].iloc[0] if 'Units' in national_df else '')
        ax.set_title(f"National Trend of {selected_pollutant}")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
        st.dataframe(national_df)

# --- Tab 4: Applications ---
with tabs[3]:
    st.subheader("Air Quality Applications (2024)")
    df = load_csv("finance", "airqualityapplications2024.csv")
    df['Proposed EPA Funding'] = df['Proposed EPA Funding'].replace('[\$,]', '', regex=True).astype(float)
    st.dataframe(df)
    st.bar_chart(df.groupby("Primary Applicant")['Proposed EPA Funding'].sum())

# --- Tab 5: Awards ---
with tabs[4]:
    st.subheader("Direct Awards (2022)")
    df = load_csv("finance", "AirQualityDirectAwards2022.csv")
    df['Amount Awarded'] = df['Amount Awarded'].replace('[\$,]', '', regex=True).astype(float)
    st.dataframe(df)
    st.bar_chart(df.groupby("Grant Recipient")['Amount Awarded'].sum())

# --- Tab 6: EPA Budget ---
with tabs[5]:
    st.subheader("EPA Budget (2000–2023)")
    df = load_csv("finance", "EPAbudget.csv")
    df['Enacted Budget'] = df['Enacted Budget'].replace('[\$,]', '', regex=True).astype(float)
    st.line_chart(df.set_index("Fiscal Year")[["Enacted Budget", "Workforce"]])
    st.dataframe(df)
