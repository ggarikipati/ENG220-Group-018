import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Air Quality Visualizations")

# Function to load the cleaned city CSV dataset
def load_city_data():
    url = 'https://github.com/Ahhfjarawan3/ENG-220-MATLAB-PROJECTS/blob/30664fb22520cf1fbdab0ecaf20734a4932ad18f/datasets/airqualitybycity2000-2023.csv?raw=true'
    city_data = pd.read_csv(url)
    # Fill forward the CBSA and Core Based Statistical Area columns to handle empty values
    city_data['CBSA'].fillna(method='ffill', inplace=True)
    city_data['Core Based Statistical Area'].fillna(method='ffill', inplace=True)
    return city_data

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
    base_url = "https://github.com/Ahhfjarawan3/ENG-220-MATLAB-PROJECTS/blob/ace503643ae54f6486fe708d856a01c95961489e/datasets/county_datasets/conreport"
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

# Load data for both cities and counties
city_data = load_city_data()
city_data = preprocess_city_data(city_data)
county_data = load_and_clean_county_data()

# Create tabs for City and County visualization
tabs = st.tabs(["City Visualization", "County Visualization"])

with tabs[0]:
    st.markdown("### Baseline Air Quality Levels")
    st.markdown("""
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
    
    st.markdown("---")  # Separator
    
    st.markdown("### City Information")
    
    city_options_dict = {f"{row['CBSA']} - {row['Core Based Statistical Area']}": row['CBSA'] for _, row in city_data.iterrows()}
    city_options = list(city_options_dict.keys())
    selected_city_info = st.selectbox("Choose a city", city_options)
    
    st.markdown("---")  # Separator
    
    st.markdown("### City Pollutant Graph")
    plot_city_pollutants(city_data, selected_city_info)

with tabs[1]:
    st.markdown("### Baseline Air Quality Levels")
    st.markdown("""
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
    
    st.markdown("---")  # Separator
 
    st.markdown("### County Information")
    
    county_options = county_data['County'].unique()
    selected_county = st.selectbox("Choose a county", county_options)
    pollutant_options = county_data.columns[2:-1]  # Exclude 'County Code', 'County', and 'Year'
    selected_pollutant = st.selectbox("Choose a pollutant", pollutant_options)
    
    st.markdown("---")  # Separator
    
    st.markdown("### County Pollutant Graph")
    plot_county_pollutant(county_data[county_data['County'] == selected_county], selected_pollutant)

