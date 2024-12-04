import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Visualizations for Air Quality Projects")

# Sidebar for baseline levels
st.sidebar.markdown("### Baseline Air Quality Levels")
st.sidebar.markdown("""
- **<span style='color:green;'>Safe levels</span>**:
  - **O3 (Ozone):** ≤ 100 µg/m³ (8-hour mean)
  - **SO2 (Sulfur Dioxide):** ≤ 75 µg/m³ (1-hour mean)
  - **PM2.5 (Fine Particulate Matter):** ≤ 5 µg/m³ (annual mean)
  - **PM10 (Coarse Particulate Matter):** ≤ 15 µg/m³ (annual mean)
  - **NO2 (Nitrogen Dioxide):** ≤ 40 µg/m³ (annual mean)
  - **CO (Carbon Monoxide):** ≤ 9 ppm (8-hour mean)
  - **Pb (Lead):** ≤ 0.15 µg/m³ (rolling 3-month average)

- **<span style='color:orange;'>Normal levels</span>**:
  - **O3 (Ozone):** 100-150 µg/m³
  - **SO2 (Sulfur Dioxide):** 75-150 µg/m³
  - **PM2.5 (Fine Particulate Matter):** 5-15 µg/m³
  - **PM10 (Coarse Particulate Matter):** 15-45 µg/m³
  - **NO2 (Nitrogen Dioxide):** 40-80 µg/m³
  - **CO (Carbon Monoxide):** 9-15 ppm
  - **Pb (Lead):** 0.15-0.5 µg/m³

- **<span style='color:red;'>Dangerous levels</span>**:
  - **O3 (Ozone):** > 150 µg/m³
  - **SO2 (Sulfur Dioxide):** > 150 µg/m³
  - **PM2.5 (Fine Particulate Matter):** > 15 µg/m³
  - **PM10 (Coarse Particulate Matter):** > 45 µg/m³
  - **NO2 (Nitrogen Dioxide):** > 80 µg/m³
  - **CO (Carbon Monoxide):** > 15 ppm
  - **Pb (Lead):** > 0.5 µg/m³
""", unsafe_allow_html=True)

# Function to load air quality applications data
def load_applications_data():
    url = 'https://github.com/Alrashdan906/ENG220-Group-18/blob/main/datasets/finance/airqualityapplications2024.csv?raw=true'
    data = pd.read_csv(url)
    data.columns = [col.strip() for col in data.columns]  # Strip any extra spaces from column names
    data['Proposed EPA Funding'] = data['Proposed EPA Funding'].replace('[\$,]', '', regex=True).astype(float) * 1000  # Clean funding values and convert to actual
    return data

# Function to load awards granted data
def load_awards_data():
    url = 'https://github.com/Alrashdan906/ENG220-Group-18/blob/main/datasets/finance/AirQualityDirectAwards2022.csv?raw=true'
    data = pd.read_csv(url)
    data['Amount Awarded'] = data['Amount Awarded'].replace('[\$,]', '', regex=True).astype(float) * 1000  # Convert to actual
    return data

# Function to load EPA budget data
def load_budget_data():
    url = 'https://github.com/Alrashdan906/ENG220-Group-18/blob/main/datasets/finance/EPAbudget.csv?raw=true'
    data = pd.read_csv(url)
    data['Enacted Budget'] = data['Enacted Budget'].replace('[\$,]', '', regex=True).astype(float) * 1000  # Convert to actual
    return data

# Function to load the cleaned city CSV dataset
def load_city_data():
    url = 'https://github.com/Alrashdan906/ENG220-Group-18/blob/main/datasets/airqualitybycity2000-2023.csv?raw=true'
    city_data = pd.read_csv(url)
    # Fill forward the CBSA and Core Based Statistical Area columns to handle empty values
    city_data['CBSA'].fillna(method='ffill', inplace=True)
    city_data['Core Based Statistical Area'].fillna(method='ffill', inplace=True)
    return city_data

# Function to load national trend data for a given pollutant
def load_national_trend_data(pollutant):
    urls = {
        'CO': 'https://github.com/Alrashdan906/ENG220-Group-18/blob/main/datasets/National_trend/Carbon_MonoxideNational.csv?raw=true',
        'NO2': 'https://github.com/Alrashdan906/ENG220-Group-18/blob/main/datasets/National_trend/Nitrogen_DioxideNational.csv?raw=true',
        'O3': 'https://github.com/Alrashdan906/ENG220-Group-18/blob/main/datasets/National_trend/OzoneNational.csv?raw=true',
        'PM10': 'https://github.com/Alrashdan906/ENG220-Group-18/blob/main/datasets/National_trend/PM10National.csv?raw=true',
        'PM25': 'https://github.com/Alrashdan906/ENG220-Group-18/blob/main/datasets/National_trend/PM25National.csv?raw=true',
        'SO2': 'https://github.com/Alrashdan906/ENG220-Group-18/blob/main/datasets/National_trend/Sulfur_DioxideNational.csv?raw=true'
    }
    url = urls[pollutant]
    data = pd.read_csv(url)
    return data

# Preprocess city data to focus on required pollutants and trend statistics
def preprocess_city_data(city_data):
    filtered_data = city_data.dropna(subset=['Pollutant', 'Trend Statistic'])
    return filtered_data

# Function to plot pollutants for a selected city
def plot_city_pollutants(city_data, city_info):
    st.write(f"Selected City: {city_info}")
    
    city_cbs_code, city_name = city_info.split(" - ", 1)
    city_data = city_data[city_data['CBSA'] == city_cbs_code]
    st.write(f"Filtered Data for Selected City ({city_name}):", city_data)
    
    years = [str(year) for year in range(2000, 2023 + 1)]
    
    plt.figure(figsize=(12, 6))
    
    for index, row in city_data.iterrows():
        pollutant = row['Pollutant']
        statistic = row['Trend Statistic']
        data_values = pd.to_numeric(row[4:], errors='coerce').fillna(0)
        
        plt.plot(years, data_values, label=f'{pollutant} ({statistic})')
    
    plt.xlabel('Year')
    plt.ylabel('Pollutant Level')
    plt.title(f'Pollutant Trends in {city_name} (2000-2023)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Function to load and clean all county datasets
def load_and_clean_county_data():
    base_url = "https://github.com/Alrashdan906/ENG220-Group-18/blob/main/datasets/county_datasets/conreport"
    all_data = []

    for year in range(2000, 2023 + 1):
        url = f"{base_url}{year}.csv?raw=true"
        
        df = pd.read_csv(url)
        df.replace('.', pd.NA, inplace=True)
        df['Year'] = year
        all_data.append(df)
    
    merged_data = pd.concat(all_data, ignore_index=True)
    return merged_data

# Function to check if there is enough data to plot
def has_enough_data(data, pollutant):
    return data[pollutant].count() >= 3

# Function to plot pollutants for a selected county and pollutant
def plot_county_pollutant(data, pollutant):
    data = data[['Year', pollutant]].dropna()
    
    if not has_enough_data(data, pollutant):
        st.write("No data available for this pollutant in the selected county.")
    else:
        plt.figure(figsize=(12, 6))
        plt.plot(data['Year'], data[pollutant], marker='o')
        plt.xlabel('Year')
        plt.ylabel(f'{pollutant} Level')
        plt.title(f'Trend of {pollutant} in {selected_county} (2000-2023)')
        plt.grid(True)
        st.pyplot(plt)
        
        st.write("Data for selected pollutant and county:")
        st.dataframe(data.set_index('Year'))

# Function to plot national trend data for a selected pollutant
def plot_national_trend(pollutant):
    data = load_national_trend_data(pollutant)
    
    plt.figure(figsize=(12, 6))
    plt.plot(data['Year'], data['Mean'], label='Mean', marker='o')
    plt.plot(data['Year'], data['10th Percentile'], label='10th Percentile', marker='o')
    plt.plot(data['Year'], data['90th Percentile'], label='90th Percentile', marker='o')
    
    plt.xlabel('Year')
    plt.ylabel(data['Units'].iloc[0])
    plt.title(f'National Trend of {pollutant} (2000-2023)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    
    st.write("Data for selected pollutant:")
    st.dataframe(data.set_index('Year'))

# Function to plot bar chart
def plot_bar_chart(data, x, y, title, x_label, y_label):
    plt.figure(figsize=(12, 6))
    plt.bar(data[x], data[y], color='skyblue')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=90)
    plt.grid(True)
    st.pyplot(plt)

# Convert state abbreviations to full state names
STATE_ABBR = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts",
    "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
    "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
    "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia"
}

# Function to filter applications data by state
def filter_applications_by_state(data, state_abbrs):
    pattern = '|'.join(state_abbrs)
    return data[data['Project State(s)'].str.contains(pattern)]

# Visualization for Air Quality Applications
def visualize_applications():
    applications_data = load_applications_data()
    all_states = set()
    applications_data['Project State(s)'].str.split(', ').apply(all_states.update)
    
    states_full = [STATE_ABBR.get(state, state) for state in all_states if state in STATE_ABBR]
    selected_state = st.selectbox("Select a State", sorted(states_full))
    selected_state_abbrs = [abbr for abbr, full in STATE_ABBR.items() if full == selected_state]
    
    filtered_data = filter_applications_by_state(applications_data, selected_state_abbrs)
    
    st.write("### Applications Data")
    st.dataframe(filtered_data)
    
    plot_bar_chart(filtered_data, 'Primary Applicant', 'Proposed EPA Funding', 
                   f'Proposed EPA Funding for {selected_state}', 'Primary Applicant', 'Proposed EPA Funding ($)')
    
    total_funding = filtered_data['Proposed EPA Funding'].sum()
    st.write(f"### Total Proposed EPA Funding for {selected_state}: ${total_funding:,.2f}")

# Function to filter awards data by EPA region
def filter_awards_by_region(data, region):
    return data[data['EPA Region'] == region]

# Visualization for Awards Granted in 2022
def visualize_awards():
    awards_data = load_awards_data()
    regions = awards_data['EPA Region'].unique()
    selected_region = st.selectbox("Select an EPA Region", regions)
    
    st.image('https://github.com/Alrashdan906/ENG220-Group-18/blob/main/eparegions.png?raw=true', caption='EPA Regions Map', use_column_width=True)
    
    filtered_data = filter_awards_by_region(awards_data, selected_region)
    
    st.write("### Awards Data")
    st.dataframe(filtered_data)
    
    plot_bar_chart(filtered_data, 'Grant Recipient', 'Amount Awarded', 
                   f'Amount Awarded in EPA Region {selected_region}', 'Grant Recipient', 'Amount Awarded ($)')
    
    total_awarded = filtered_data['Amount Awarded'].sum()
    st.write(f"### Total Amount Awarded in EPA Region {selected_region}: ${total_awarded:,.2f}")

# Visualization for EPA Budget from 2000-2023
def visualize_budget():
    budget_data = load_budget_data()
    
    st.write("### EPA Budget Data")
    st.dataframe(budget_data)
    
    plot_bar_chart(budget_data, 'Fiscal Year', 'Enacted Budget', 
                   'EPA Budget Over the Years', 'Fiscal Year', 'Enacted Budget ($)')
    
    plt.figure(figsize=(12, 6))
    plt.plot(budget_data['Fiscal Year'], budget_data['Workforce'], marker='o', color='orange')
    plt.xlabel('Fiscal Year')
    plt.ylabel('Workforce')
    plt.title('EPA Workforce Over the Years')
    plt.grid(True)
    st.pyplot(plt)

# Load data for both cities and counties
city_data = load_city_data()
city_data = preprocess_city_data(city_data)
county_data = load_and_clean_county_data()

# Create tabs for visualizations
tabs = st.tabs(["City Visualization", "County Visualization", "National Trends", "Air Quality Applications", "Awards Granted", "EPA Budget"])

with tabs[0]:
    st.markdown("### City Information")
    
    city_options_dict = {f"{row['CBSA']} - {row['Core Based Statistical Area']}": row['CBSA'] for _, row in city_data.iterrows()}
    city_options = list(city_options_dict.keys())
    selected_city_info = st.selectbox("Choose a city", city_options)
    
    st.markdown("---")  # Separator
    
    st.markdown("### City Pollutant Graph")
    plot_city_pollutants(city_data, selected_city_info)

with tabs[1]:
    st.markdown("### County Information")
    
    county_options = county_data['County'].unique()
    selected_county = st.selectbox("Choose a county", county_options)
    pollutant_options = county_data.columns[2:-1]  # Exclude 'County Code', 'County', and 'Year'
    selected_pollutant = st.selectbox("Choose a pollutant", pollutant_options)
    
    st.markdown("---")  # Separator
    
    st.markdown("### County Pollutant Graph")
    plot_county_pollutant(county_data[county_data['County'] == selected_county], selected_pollutant)

with tabs[2]:
    st.markdown("### National Trends of Air Quality")
    
    national_pollutants = ['CO', 'NO2', 'O3', 'PM10', 'PM25', 'SO2']
    selected_national_pollutant = st.selectbox("Choose a pollutant", national_pollutants)
    
    st.markdown("---")  # Separator
    
    st.markdown(f"### National Trend Graph for {selected_national_pollutant}")
    plot_national_trend(selected_national_pollutant)

with tabs[3]:
    st.markdown("## Air Quality Applications and Funding")
    visualize_applications()

with tabs[4]:
    st.markdown("## Awards Granted in 2022")
    visualize_awards()

with tabs[5]:
    st.markdown("## EPA Budget from 2000-2023")
    visualize_budget()
