# Team 18 Air quality funding Project

# Authors:

- Abdullah Jarawan
- Ahmad Alazmi
- Mubarak Fhid
- Mohammad Alazemi
- Meshal Alazmi
- Faisal Alrashdan

# Air Quality and Finance Visualizations

This Streamlit app provides comprehensive visualizations for air quality and finance-related data, focusing on air quality monitoring projects and EPA budget details. The app is divided into two main sections: Air Quality Visualizations and Finance Visualizations.

# Project Link
https://eng220-group-18-finall.streamlit.app/

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [Visualizations](#visualizations)
  - [Air Quality Visualizations](#air-quality-visualizations)
    - [City Visualization](#city-visualization)
    - [County Visualization](#county-visualization)
    - [National Trends](#national-trends)
  - [Finance Visualizations](#finance-visualizations)
    - [Air Quality Applications](#air-quality-applications)
    - [Awards Granted](#awards-granted)
    - [EPA Budget](#epa-budget)


## Overview

The app provides insightful visualizations for various air quality monitoring data and financial data related to air quality projects. It is designed to help users understand the trends and distribution of air pollutants across different regions and analyze the funding and budget allocation for air quality projects.

## Installation

To run the app locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/air-quality-finance-visualizations.git
    cd air-quality-finance-visualizations
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

## Usage

The app is structured into two main sections: Air Quality Visualizations and Finance Visualizations. Each section contains multiple tabs to display different types of data visualizations.

### Data Sources

- **Air Quality Data**: Contains information about air quality levels in various cities and counties from 2000 to 2023.
- **Finance Data**: Includes details about air quality project applications, awards granted, and the EPA budget from 2000 to 2023.

### Visualizations

#### Air Quality Visualizations

##### City Visualization

- **Description**: Displays pollutant trends in selected cities from 2000 to 2023.
- **Usage**:
  1. Select a city from the dropdown menu.
  2. View the pollutant trend graph and detailed data for the selected city.

##### County Visualization

- **Description**: Shows pollutant trends in selected counties from 2000 to 2023.
- **Usage**:
  1. Select a county and a pollutant from the dropdown menus.
  2. View the pollutant trend graph and detailed data for the selected county.

##### National Trends

- **Description**: Illustrates national trends for various pollutants from 2000 to 2023.
- **Usage**:
  1. Select a pollutant from the dropdown menu.
  2. View the national trend graph and detailed data for the selected pollutant.

#### Finance Visualizations

##### Air Quality Applications

- **Description**: Provides information about air quality project applications and proposed EPA funding by state.
- **Usage**:
  1. Select a state from the dropdown menu.
  2. View the table of applicants, a bar chart of proposed funding, and the total proposed funding for the selected state.

##### Awards Granted

- **Description**: Shows details about awards granted for air quality projects in 2022 by EPA region.
- **Usage**:
  1. Select an EPA region from the dropdown menu.
  2. View the table of award recipients, a bar chart of awarded amounts, and the total awarded amount for the selected region.

##### EPA Budget

- **Description**: Visualizes the EPA budget and workforce from 2000 to 2023.
- **Usage**: View the bar chart of the enacted budget over the years and the trend of the workforce.

