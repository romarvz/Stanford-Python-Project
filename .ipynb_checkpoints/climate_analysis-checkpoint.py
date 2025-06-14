import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import os
from datetime import datetime
import numpy as np

# Set style for better visualizations
plt.style.use('default')
sns.set_theme()

def download_dataset(url, filename):
    """Download dataset from URL and save it locally"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename} successfully")
    else:
        print(f"Failed to download {filename}")

def load_data(filename):
    """Load dataset from local file"""
    try:
        return pd.read_csv(f'data/{filename}')
    except FileNotFoundError:
        print(f"File {filename} not found. Please download it first.")
        return None

def preprocess_temperature_data(filename):
    """Preprocess temperature data from NASA text file"""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        # Find the header line
        data_start = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('Year'):
                data_start = i
                break
        # Parse the data
        data_lines = lines[data_start+1:]
        years = []
        temps = []
        for line in data_lines:
            if line.strip() and not line.strip().startswith('Year'):
                parts = line.split()
                if len(parts) >= 14:
                    try:
                        year = int(parts[0])
                        temp = float(parts[13]) / 100  # J-D column, convert to degrees
                        years.append(year)
                        temps.append(temp)
                    except (ValueError, IndexError):
                        continue
        temp_data = pd.DataFrame({'Year': years, 'Temperature': temps})
        return temp_data
    except Exception as e:
        print(f"Error processing temperature data: {e}")
        return None

def preprocess_co2_data(filename):
    """Preprocess CO2 data from OWID CSV, using only global data"""
    try:
        data = pd.read_csv(filename)
        # Filter for global data
        data = data[data['country'] == 'World']
        # Use 'year' and 'co2' columns
        data = data[['year', 'co2']].dropna()
        data = data.rename(columns={'year': 'Year', 'co2': 'CO2_Emissions'})
        return data
    except Exception as e:
        print(f"Error processing CO2 data: {e}")
        return None

def preprocess_sea_level_data(data):
    """Preprocess sea level data"""
    print("Sea level data columns:", data.columns.tolist())
    try:
        data['CSIRO Adjusted Sea Level'] = pd.to_numeric(data['CSIRO Adjusted Sea Level'], errors='coerce')
        data = data.dropna(subset=['CSIRO Adjusted Sea Level'])
        return data[['Year', 'CSIRO Adjusted Sea Level']].rename(
            columns={'CSIRO Adjusted Sea Level': 'Sea_Level'}
        )
    except Exception as e:
        print(f"Error processing sea level data: {e}")
        return None

def plot_temperature_trends(data):
    """Plot global temperature trends with confidence intervals"""
    plt.figure(figsize=(12, 6))
    plt.plot(data['Year'], data['Temperature'], marker='o', label='Temperature')
    if 'Temperature_Uncertainty' in data.columns:
        plt.fill_between(data['Year'], 
                        data['Temperature'] - data['Temperature_Uncertainty'],
                        data['Temperature'] + data['Temperature_Uncertainty'],
                        alpha=0.2)
    plt.title('Global Temperature Trends Over Time')
    plt.xlabel('Year')
    plt.ylabel('Temperature Anomaly (°C)')
    plt.grid(True)
    plt.legend()
    plt.savefig('temperature_trends.png')
    plt.close()

def plot_co2_emissions(data):
    """Plot CO2 emissions trends with rolling average"""
    plt.figure(figsize=(12, 6))
    plt.plot(data['Year'], data['CO2_Emissions'], marker='o', color='red', alpha=0.5, label='Annual Emissions')
    
    # Add rolling average
    rolling_avg = data['CO2_Emissions'].rolling(window=5).mean()
    plt.plot(data['Year'], rolling_avg, color='darkred', linewidth=2, label='5-year Average')
    
    plt.title('Global CO2 Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('CO2 Emissions (million metric tons)')
    plt.grid(True)
    plt.legend()
    plt.savefig('co2_emissions.png')
    plt.close()

def plot_sea_levels(data):
    """Plot sea level rise with trend line"""
    plt.figure(figsize=(12, 6))
    plt.scatter(data['Year'], data['Sea_Level'], alpha=0.5, label='Measured Levels')
    
    # Add trend line
    z = np.polyfit(data['Year'], data['Sea_Level'], 1)
    p = np.poly1d(z)
    plt.plot(data['Year'], p(data['Year']), "r--", linewidth=2, label='Trend Line')
    
    plt.title('Global Sea Level Rise')
    plt.xlabel('Year')
    plt.ylabel('Sea Level (mm)')
    plt.grid(True)
    plt.legend()
    plt.savefig('sea_levels.png')
    plt.close()

def plot_correlation_matrix(temp_data, co2_data, sea_level_data):
    """Create correlation matrix between different climate indicators"""
    # Merge datasets on year
    merged_data = pd.merge(temp_data, co2_data, on='Year')
    merged_data = pd.merge(merged_data, sea_level_data, on='Year')
    
    # Calculate correlation matrix
    corr_matrix = merged_data[['Temperature', 'CO2_Emissions', 'Sea_Level']].corr()
    
    # Plot correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Between Climate Indicators')
    plt.savefig('correlation_matrix.png')
    plt.close()

def plot_combined_trends(temp_data, co2_data, sea_level_data):
    """Plot all three indicators on the same timeline"""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
    
    # Temperature plot
    ax1.plot(temp_data['Year'], temp_data['Temperature'], 'b-', label='Temperature')
    ax1.set_ylabel('Temperature Anomaly (°C)')
    ax1.grid(True)
    ax1.legend()
    
    # CO2 plot
    ax2.plot(co2_data['Year'], co2_data['CO2_Emissions'], 'r-', label='CO2 Emissions')
    ax2.set_ylabel('CO2 Emissions (million metric tons)')
    ax2.grid(True)
    ax2.legend()
    
    # Sea level plot
    ax3.plot(sea_level_data['Year'], sea_level_data['Sea_Level'], 'g-', label='Sea Level')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Sea Level (mm)')
    ax3.grid(True)
    ax3.legend()
    
    plt.suptitle('Climate Change Indicators Over Time')
    plt.tight_layout()
    plt.savefig('combined_trends.png')
    plt.close()

def create_visualizations(temp_data, co2_data, sea_level_data):
    """Create all visualizations for the climate analysis"""
    plot_temperature_trends(temp_data)
    plot_co2_emissions(co2_data)
    plot_sea_levels(sea_level_data)
    plot_correlation_matrix(temp_data, co2_data, sea_level_data)
    plot_combined_trends(temp_data, co2_data, sea_level_data)
    print("All visualizations have been created successfully!")

def main():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Download datasets
    download_dataset('https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.txt', 'data/temperature_data.csv')
    download_dataset('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv', 'data/co2_data.csv')
    download_dataset('https://raw.githubusercontent.com/datasets/sea-level-rise/master/data/epa-sea-level.csv', 'data/sea_level_data.csv')
    
    # Load and preprocess data
    temp_data = preprocess_temperature_data('data/temperature_data.csv')
    co2_data = preprocess_co2_data('data/co2_data.csv')
    sea_level_data = preprocess_sea_level_data(pd.read_csv('data/sea_level_data.csv'))
    
    if temp_data is None or co2_data is None or sea_level_data is None:
        print("Error: Could not process all datasets. Please check the data format.")
        return
    
    # Create visualizations
    create_visualizations(temp_data, co2_data, sea_level_data)

if __name__ == "__main__":
    main() 