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
        # st.session_state["uploaded_data"],
        st.session_state["x_axis"],
        st.session_state["y_axis"],
        st.session_state["transformed_data"],
    )


def train_test_split(data, split_ratio):
    """Split data into train and test sets"""
    train_size = int(len(data) * (split_ratio / 100))
    train_data = data.iloc[:train_size]
    test_data = data.iloc[train_size:]

    return train_data, test_data


def return_imported_models():
    return ["AutoARIMA", "SeasonalNaive", "HoltWinters", "HistoricAverage", "MSTL"]


def get_model(selected_model, season_length):
    """Retrieve the model based on the selected type and season length."""
    model_map = {
        "AutoARIMA": AutoARIMA(season_length=int(season_length)),
        "HoltWinters": HoltWinters(season_length=int(season_length)),
        "SeasonalNaive": SeasonalNaive(season_length=int(season_length)),
        "HistoricAverage": HistoricAverage(),
        "MSTL": MSTL(season_length=int(season_length)),
    }
    return model_map.get(selected_model)


def fit_model(model, training_data, testing_data, freq):
    """Fit the model to training data and validate it against testing data"""
    sf = StatsForecast(models=[model], freq=freq, n_jobs=-1)
    sf.fit(df=training_data)

    # Prepare a DataFrame for forecasting
    forecast_horizon = len(testing_data)
    forecast_df = sf.forecast(h=forecast_horizon, df=training_data)

    # Ensure column names align for consistency
    forecast_df = forecast_df.rename(columns={"y_hat": "y"})
    forecast_df["Type"] = "Predicted"

    return forecast_df


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
