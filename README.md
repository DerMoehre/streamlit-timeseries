# Time Series Analysis Dashboard

A **Time Series Analysis Dashboard** built using Python and Streamlit, designed for interactive data visualization, model fitting, and forecasting. This project leverages powerful forecasting models from **Nixtla's `statsforecast` package** and integrates them into a user-friendly, web-based application.

https://github.com/user-attachments/assets/9d1642c1-17f3-467c-b4be-be0a94619556


## Features

### Data Upload and Management

- **Upload CSV files**: Allows users to upload time series data directly into the app.
- **Data clearing**: Remove previously uploaded data to reset the dashboard.

### Interactive Graphs and Visualizations

- **Training, Testing, and Forecast Visualization**: Split your data into training and testing sets and visualize the results along with the forecast.
- **Dynamic Forecast Display**: Choose from multiple models (e.g., AutoARIMA, HoltWinters) to display forecasted values.
- **Adjustable Slider**: Set the split point for training and testing datasets dynamically using a slider.

### Model Fitting and Forecasting

- **Built-in Forecasting Models**:
  - AutoARIMA
  - HoltWinters
  - SeasonalNaive
  - HistoricAverage
  - MSTL
- **Parameter Tuning**: Modify hyperparameters like `freq` and `season_length` directly in the app.
- **Real-time Loading Animation**: Provides visual feedback while forecasts are being calculated.

## Technologies Used

- **Streamlit**: Framework for building interactive web applications in Python.
- **Pandas**: Data manipulation and analysis.
- **Nixtla's `statsforecast`**: State-of-the-art time series forecasting package.
- **Plotly**: Create beautiful graphics

## Installation

### Option 1: Run locally

1. Clone the repository:
   ```bash
   git clone https://github.com/DerMoehre/streamlit-timeseries.git
   cd streamlit-timeseries
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app
    ```bash
   streamlit run Home.py
   ```

### Option 2: Run with Docker

1. Build the Docker Image
    ```bash
    docker-compose build
    ```
2. Run the app
    ```bash
    docker-compose up
    ```
   
Open the app in your browser at `http://127.0.0.1:8501/`

## Usage

1. **Upload your time series data** via the **Upload Modal**.
2. **Adjust the training and testing split** using the **slider**.
3. **Select a forecasting model** from the dropdown and fine-tune parameters if needed.
4. **View forecasts** alongside training and testing data in the interactive graph.

## Data Format

The uploaded timedata should have the following structure:
- `YYYY-MM-DD HH:MM:SS` format for hourly data 
- `YYYY-MM-DD` for daily data.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
