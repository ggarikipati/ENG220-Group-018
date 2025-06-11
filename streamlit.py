import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Group-018 | Air Quality Finance", layout="wide")
st.title("Group-018: Air Quality Finance & Trends Dashboard")

st.markdown("""
This project analyzes **funding, budgets, and pollutant trends** in air quality initiatives across the United States.  
It explores:
- City- and county-level air quality trends
- National pollutant trends
- EPA funding applications and awarded grants
- Historical EPA budgets and workforce changes
""")

# ============================
# Utility Functions
# ============================
def load_csv_local(filename):
    base_dir = os.path.dirname(__file__)
    return pd.read_csv(os.path.join(base_dir, "datasets", filename))

def load_multiple_csvs(prefix, start_year, end_year):
    dfs = []
    for year in range(start_year, end_year + 1):
        try:
            df = load_csv_local(f"{prefix}{year}.csv")
            df['Year'] = year
            dfs.append(df)
        except FileNotFoundError:
            continue
    return pd.concat(dfs, ignore_index=True)

# ============================
# Load Data
# ============================
city_data = load_csv_local("airqualitybycity2000-2023.csv")
city_data['CBSA'].fillna(method='ffill', inplace=True)
city_data['Core Based Statistical Area'].fillna(method='ffill', inplace=True)
city_data = city_data.dropna(subset=['Pollutant', 'Trend Statistic'])

county_data = load_multiple_csvs("conreport", 2000, 2023)
county_data.replace('.', pd.NA, inplace=True)

applications_data = load_csv_local("airqualityapplications2024.csv")
applications_data['Proposed EPA Funding'] = applications_data['Proposed EPA Funding'].replace('[\$,]', '', regex=True).astype(float) * 1000

awards_data = load_csv_local("AirQualityDirectAwards2022.csv")
awards_data['Amount Awarded'] = awards_data['Amount Awarded'].replace('[\$,]', '', regex=True).astype(float) * 1000

budget_data = load_csv_local("EPAbudget.csv")
budget_data['Enacted Budget'] = budget_data['Enacted Budget'].replace('[\$,]', '', regex=True).astype(float) * 1000

# ============================
# Tabs
# ============================
tabs = st.tabs([
    "City Trends", "County Trends", "Applications", "Awards", "Budget"
])

# ============================
# Tab 1: City Trends
# ============================
with tabs[0]:
    st.subheader("Air Quality by City (2000–2023)")

    city_options = {
        f"{row['CBSA']} - {row['Core Based Statistical Area']}": row['CBSA']
        for _, row in city_data.iterrows()
    }
    selected_city_info = st.selectbox("Choose a city", list(city_options.keys()))
    selected_cbsa = selected_city_info.split(" - ")[0]
    selected_city_df = city_data[city_data['CBSA'] == selected_cbsa]

    st.write("#### Pollutant Trend Graph")
    years = [str(year) for year in range(2000, 2024)]
    plt.figure(figsize=(12, 6))
    for _, row in selected_city_df.iterrows():
        pollutant = row['Pollutant']
        stat = row['Trend Statistic']
        values = pd.to_numeric(row[4:], errors='coerce').fillna(0)
        plt.plot(years, values, label=f'{pollutant} ({stat})')
    plt.xlabel('Year')
    plt.ylabel('Level')
    plt.title(f"Trends for {selected_city_info}")
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)

# ============================
# Tab 2: County Trends
# ============================
with tabs[1]:
    st.subheader("Air Quality by County")

    county_names = county_data['County'].dropna().unique()
    selected_county = st.selectbox("Choose a county", county_names)
    county_df = county_data[county_data['County'] == selected_county]

    pollutant_options = [col for col in county_df.columns if col not in ['County Code', 'County', 'Year']]
    selected_pollutant = st.selectbox("Choose pollutant", pollutant_options)

    plot_df = county_df[['Year', selected_pollutant]].dropna()
    if plot_df.shape[0] >= 3:
        plt.figure(figsize=(12, 6))
        plt.plot(plot_df['Year'], plot_df[selected_pollutant], marker='o')
        plt.title(f"{selected_pollutant} in {selected_county} (2000–2023)")
        plt.xlabel("Year")
        plt.ylabel("Level")
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.warning("Insufficient data for this pollutant.")

# ============================
# Tab 3: Applications
# ============================
with tabs[2]:
    st.subheader("EPA Air Quality Applications (2024)")

    all_states = set()
    applications_data['Project State(s)'].str.split(', ').apply(all_states.update)
    state_list = sorted(list(all_states))
    selected_state = st.selectbox("Select State", state_list)

    filtered_app = applications_data[
        applications_data['Project State(s)'].str.contains(selected_state, na=False)
    ]
    st.write("### Applications Table")
    st.dataframe(filtered_app)

    if not filtered_app.empty:
        st.write(f"### Total Proposed Funding: ${filtered_app['Proposed EPA Funding'].sum():,.0f}")
        top_applicants = filtered_app.sort_values(by='Proposed EPA Funding', ascending=False).head(10)
        plt.figure(figsize=(12, 6))
        plt.bar(top_applicants['Primary Applicant'], top_applicants['Proposed EPA Funding'])
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("Funding ($)")
        plt.title(f"Top Applicants in {selected_state}")
        plt.grid(True)
        st.pyplot(plt)

# ============================
# Tab 4: Awards
# ============================
with tabs[3]:
    st.subheader("Grants Awarded (2022) by EPA Region")

    regions = awards_data['EPA Region'].dropna().unique()
    selected_region = st.selectbox("Select EPA Region", sorted(regions))

    filtered_awards = awards_data[awards_data['EPA Region'] == selected_region]
    st.dataframe(filtered_awards)

    if not filtered_awards.empty:
        st.write(f"### Total Awarded: ${filtered_awards['Amount Awarded'].sum():,.0f}")
        top_awards = filtered_awards.sort_values(by='Amount Awarded', ascending=False).head(10)
        plt.figure(figsize=(12, 6))
        plt.bar(top_awards['Grant Recipient'], top_awards['Amount Awarded'])
        plt.xticks(rotation=45, ha='right')
        plt.title(f"Top Grant Recipients in Region {selected_region}")
        plt.ylabel("Awarded ($)")
        plt.grid(True)
        st.pyplot(plt)

# ============================
# Tab 5: Budget
# ============================
with tabs[4]:
    st.subheader("EPA Budget & Workforce (2000–2023)")

    st.dataframe(budget_data)

    plt.figure(figsize=(12, 6))
    plt.bar(budget_data['Fiscal Year'], budget_data['Enacted Budget'], color='skyblue')
    plt.title("EPA Enacted Budget Over Time")
    plt.xlabel("Fiscal Year")
    plt.ylabel("Budget ($)")
    plt.grid(True)
    st.pyplot(plt)

    plt.figure(figsize=(12, 6))
    plt.plot(budget_data['Fiscal Year'], budget_data['Workforce'], marker='o', color='orange')
    plt.title("EPA Workforce Over Time")
    plt.xlabel("Fiscal Year")
    plt.ylabel("Number of Employees")
    plt.grid(True)
    st.pyplot(plt)
