import streamlit as st

st.set_page_config(
    page_title="Forecast",
    page_icon="📈",
)

st.title("Welcome to TimeSeries Forecasting")

st.markdown(
    """ 
This app allows you to explore and forecast time series data effortlessly. With a user-friendly interface and powerful modeling tools, you can:

- **Upload Data**: Import your time series data for analysis and forecasting.  
- **Preprocess and Visualize**: Split your data into train and test sets, and visualize the splits interactively.  
- **Fit Models**: Choose from a range of forecasting models like AutoARIMA, Holt-Winters, MSTL, and more. Customize model settings to suit your data.  
- **Evaluate Performance**: Assess model accuracy using metrics such as MAE, R², and MAPE.  
- **Forecast Future Values**: Generate future predictions with adjustable forecast horizons.

The app is designed for users of all skill levels, from beginners to advanced analysts. Dive into your time series data and uncover insights with ease! 🚀

"""
)
