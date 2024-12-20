import streamlit as st
import plotly.express as px

from shared.utils_fitting import (
    load_data_from_session,
    train_test_split,
    return_imported_models,
    test_train_plot,
    return_frequency,
    get_model,
    fit_model,
    evaluate_performance,
)
from shared.utils_upload import is_data_in_session

st.set_page_config(page_title="Model Fitting", page_icon="🦾", layout="wide")

st.title("Model Fitting 🦾")

# Sidebar
st.sidebar.header("Train-Test Split")
split_ratio = st.sidebar.slider(
    "Select Train-Test Split Ratio (%)", min_value=50, max_value=90, value=70, step=1
)

model_list = return_imported_models()
model = st.sidebar.selectbox(
    "Select Model",
    [model for model in model_list],
    help="""
- **AutoARIMA**: Automatically selects the best ARIMA model for your data.  
  **Pros**: No manual tuning, handles trends and seasonality, adaptable to various datasets.  
- **SeasonalNaive**: Predicts by repeating the last observed seasonal pattern.  
  **Pros**: Simple, fast, effective for strong seasonality.  
- **HoltWinters**: Captures trends and seasonality using weighted smoothing.  
  **Pros**: Robust for data with clear patterns, easy to interpret.  
- **HistoricAverage**: Forecasts using the average of historical data.  
  **Pros**: Extremely simple, efficient, and suitable for stationary data.  
- **MSTL**: Decomposes data into multiple seasonal components, trend, and residuals.  
  **Pros**: Ideal for complex seasonality, flexible, and interpretable.
""",
)

freq = return_frequency()
frequency = st.sidebar.selectbox(
    "Select Frequency",
    [freq for freq in freq.keys()],
    help="Select the frequency of the underlying data",
)
selected_freq = freq.get(frequency)

season_length = st.sidebar.number_input(
    "Season Lenght",
    min_value=1,
    placeholder="Type a number...",
    help="How many periods are in a season?",
)

mae = None

if is_data_in_session():
    x_axis, y_axis, data = load_data_from_session()
    train_data, test_data = train_test_split(data, split_ratio)
    fig = test_train_plot(data, train_data, test_data, x_axis, y_axis, split_ratio)

    if st.sidebar.button("Fit Model"):
        selected_model = get_model(model, season_length)
        with st.spinner("Fitting Model..."):
            forecast = fit_model(selected_model, train_data, test_data, selected_freq)
            fig = test_train_plot(
                data,
                train_data,
                test_data,
                x_axis,
                y_axis,
                split_ratio,
                forecast,
                model,
            )
        st.sidebar.success("Model Fitted Successfully")
        mae, r2, mape = evaluate_performance(forecast, test_data, model)
    st.write(
        f"### Train-Test Split Visualization ({split_ratio}% Train, {100 - split_ratio}% Test)"
    )
    st.plotly_chart(fig, use_container_width=True)
    if mae:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="Mean absolute error",
                value=mae,
                help="Measures the average absolute difference between actual and predicted values. Lower values indicate better accuracy.",
            )
        with col2:
            st.metric(
                label="R2",
                value=r2,
                help="Indicates how well the forecast explains the variance in the actual data. Values closer to 1 signify a better fit.",
            )
        with col3:
            st.metric(
                label="Mean absolute percentage error",
                value=mape,
                help="Measures the average percentage error between actual and predicted values. Useful for comparing accuracy across scales.",
            )

else:
    st.error("You have to first update Data on the upload page.")
