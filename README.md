# Climate Change Data Analysis

This project analyzes global climate change indicators using open datasets. It explores trends in global temperature anomalies, CO2 emissions, and sea level rise, and examines the relationships between these variables.

## Features
- **Automated data download** for global temperature, CO2 emissions, and sea level rise
- **Data preprocessing** for each dataset
- **Visualizations**:
  - Global temperature anomaly trends
  - Global CO2 emissions trends
  - Global sea level rise
  - Correlation matrix between indicators
  - Combined trends plot
- **Detailed analysis** in markdown cells within the Jupyter Notebook

## Datasets Used
- **Global Temperature**: [NASA GISTEMP](https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.txt)
- **CO2 Emissions**: [Our World in Data CO2 dataset](https://github.com/owid/co2-data)
- **Sea Level Rise**: [EPA Sea Level dataset](https://github.com/datasets/sea-level-rise)

## How to Install Jupyter Notebook
If you don't have Jupyter installed, you can install it with pip:

```bash
pip install jupyter
```

Or, if you want the full JupyterLab experience:

```bash
pip install jupyterlab
```

After installation, you can launch the notebook with:

```bash
jupyter notebook
```
or
```bash
jupyter lab
```

## How to Use
1. **Install dependencies** (recommended: use a virtual environment):
   ```bash
   pip install -r requirements.txt
   # or manually:
   pip install pandas matplotlib seaborn requests numpy jupyter
   ```
2. **Launch Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```
3. **Open `climate_analysis.ipynb`** in your browser.
4. **Run all cells** (Shift+Enter) to download data, preprocess, and generate all visualizations and analysis.

## Notebook Structure
- **Data Download**: Automatically downloads the latest datasets.
- **Preprocessing**: Cleans and structures the data for analysis.
- **Visualization & Analysis**: Each section includes a plot and a markdown cell with interpretation and insights.

## Visualizations Included
- **Global Temperature Trends**: Line plot of temperature anomaly over time.
- **CO2 Emissions Trends**: Line plot with 5-year moving average.
- **Sea Level Rise**: Scatter plot with trend line.
- **Correlation Matrix**: Heatmap showing relationships between indicators.
- **Combined Trends**: All three indicators on a shared timeline.

## Requirements
- Python 3.7+
- pandas
- matplotlib
- seaborn
- requests
- numpy
- jupyter

## License
This project is for educational and research purposes. Data sources are credited to their respective organizations. 