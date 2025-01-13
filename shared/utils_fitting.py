import streamlit as st
import csv
import plotly.express as px
import pandas as pd

from statsforecast import StatsForecast
from statsforecast.models import (
    AutoARIMA,
    SeasonalNaive,
    HoltWinters,
    HistoricAverage,
    MSTL,
)

from sklearn.metrics import (
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error,
)

####### PAGE 2: Model Fitting #######


def load_data_from_session():
    """Load all data from session state"""
    return (
        st.session_state["x_axis"],
        st.session_state["y_axis"],
        st.session_state["transformed_data"],
    )


def render_initial_sidebar():
    st.sidebar.header("Train-Test Split")
    split_ratio = st.sidebar.slider(
        "Select Train-Test Split Ratio (%)",
        min_value=50,
        max_value=90,
        value=70,
        step=1,
    )

    type_selector = st.sidebar.radio(
        "Select Modeltype",
        ["Statistics", "Machine Learning"],
         horizontal=True
         )
    if type_selector == "Statistics":
        model_list = return_imported_stat_models()
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
            "Season Length",
            min_value=1,
            placeholder="Type a number...",
            help="How many periods are in a season?",
        )

        season_mstl = 0

        if model == "MSTL":
            season_mstl = st.sidebar.number_input(
                "Second Season Length",
                min_value=0,
                placeholder="Type a number...",
                help="How many periods are in a season?",
            )
        return split_ratio, model, selected_freq, season_length, season_mstl
    else:
        st.sidebar.write("Currently not implemented - Coming soon")
        return None, None, None, None, None


def train_test_split(data, split_ratio):
    """Split data into train and test sets"""
    train_size = int(len(data) * (split_ratio / 100))
    train_data = data.iloc[:train_size]
    test_data = data.iloc[train_size:]

    return train_data, test_data


def return_imported_stat_models():
    return ["AutoARIMA", "SeasonalNaive", "HoltWinters", "HistoricAverage", "MSTL"]


def get_model(selected_model, season_length, season_mstl=None):
    """Retrieve the model based on the selected type and season length."""
    if selected_model == "MSTL":
        if season_mstl is None or season_mstl <= 1:
            return MSTL(season_length=[int(season_length)])
        else:
            return MSTL(season_length=[int(season_length), int(season_mstl)])
    model_map = {
        "AutoARIMA": AutoARIMA(season_length=int(season_length)),
        "HoltWinters": HoltWinters(season_length=int(season_length)),
        "SeasonalNaive": SeasonalNaive(season_length=int(season_length)),
        "HistoricAverage": HistoricAverage(),
    }
    return model_map.get(selected_model)


def fit_model(model, training_data, testing_data, freq, freq_mstl=None):
    """Fit the model to training data and validate it against testing data"""
    if model == "MSTL":
        sf = StatsForecast(models=[model], freq=[freq, freq_mstl], n_jobs=-1)
    else:
        sf = StatsForecast(models=[model], freq=freq, n_jobs=-1)
    sf.fit(df=training_data)

    # Prepare a DataFrame for forecasting
    forecast_horizon = len(testing_data)
    forecast_df = sf.forecast(h=forecast_horizon, df=training_data)

    # Ensure column names align for consistency
    forecast_df = forecast_df.rename(columns={"y_hat": "y"})
    forecast_df["Type"] = "Predicted"

    return forecast_df, sf


def evaluate_performance(forecast_df, testing_data, model):
    """Evaluate the model using the forecasted data"""
    mae = round(mean_absolute_error(testing_data["y"], forecast_df[model]), 2)
    r2 = round(r2_score(testing_data["y"], forecast_df[model]), 2)
    mape = round(
        mean_absolute_percentage_error(testing_data["y"], forecast_df[model]), 2
    )

    return mae, r2, mape


def return_frequency():
    return {"Yearly": "YS", "Monthly": "MS", "Weekly": "W", "Daily": "D", "Hourly": "H"}


def test_train_plot(
    data, train_data, test_data, x_axis, y_axis, split_ratio, model_fit=None, model=None
):
    fig = px.line(data, x="ds", y="y", title=f"{x_axis} vs {y_axis}")
    fig.update_layout(xaxis_title=x_axis, yaxis_title=y_axis)
    fig.update_traces(opacity=0.1)

    fig.add_scatter(
        x=train_data["ds"],
        y=train_data["y"],
        mode="lines",
        name="Train Data",
        line=dict(color="blue", width=4),
    )
    fig.add_scatter(
        x=test_data["ds"],
        y=test_data["y"],
        mode="lines",
        name="Test Data",
        line=dict(color="red", width=4),
    )
    if model_fit is not None:
        fig.add_scatter(
            x=model_fit["ds"],
            y=model_fit[model],
            mode="lines",
            name="Fitted Data",
            line=dict(color="purple", width=4, dash="dot"),
        )
    fig.update_layout(
        xaxis_title="Date", yaxis_title="Values", legend_title="Data Split"
    )

    return fig
