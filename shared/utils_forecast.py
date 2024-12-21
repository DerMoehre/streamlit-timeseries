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


def load_model_data_from_session():
    return (
        st.session_state["fitted_model"],
        st.session_state["selected_model"],
        st.session_state["freq"],
        st.session_state["season_length"],
        st.session_state["season_mstl"],
        st.session_state["split_ratio"],
    )


def is_model_data_in_session():
    return (
        "fitted_model" in st.session_state
        and "freq" in st.session_state
        and "season_length" in st.session_state
        and "season_mstl" in st.session_state
    )


def render_model_sidebar(model, freq, season_length, season_mstl):
    st.sidebar.header("Fitted Model")
    st.sidebar.write(f"**Model:** {model}")
    st.sidebar.write(f"**Frequency:** {freq}")
    st.sidebar.write(f"**Season Lenght:** {season_length}")
    if str(model) == "MSTL":
        st.sidebar.write(f"**Second Season Lenght:** {season_mstl}")
    st.sidebar.divider()
    model_performance = st.session_state.get("last_evaluation")
    st.sidebar.header("Model Performance")
    st.sidebar.write(f"**MAE:** {model_performance.get('mae')}")
    st.sidebar.write(f"**R2:** {model_performance.get('r2')}")
    st.sidebar.write(f"**MAPE:** {model_performance.get('mape')}")
    st.sidebar.divider()
    forecast_horizon = st.sidebar.number_input(
        "Forecast Horizon",
        min_value=0,
        placeholder="Type a number...",
        help="How many seasons do you want to forecast?",
    )
    return forecast_horizon


def forecast_plot(data, x_axis, y_axis, model, forecast=None):
    fig = px.line(data, x="ds", y="y", title=f"{x_axis} vs {y_axis}")
    fig.update_layout(xaxis_title=x_axis, yaxis_title=y_axis)

    if forecast is not None:
        fig.add_scatter(
            x=forecast["ds"],
            y=forecast[model],
            mode="lines",
            name="Forecast",
            line=dict(color="purple", width=4, dash="dot"),
        )
    fig.update_layout(
        xaxis_title="Date", yaxis_title="Values", legend_title="Data Split"
    )

    return fig


def forecast(model, data, forecast_horizon, freq, freq_mstl=None):
    """Fit the model to training data and validate it against testing data"""
    model.fit(df=data)

    # Prepare a DataFrame for forecasting
    forecast_df = model.forecast(h=forecast_horizon, df=data)

    # Ensure column names align for consistency
    forecast_df = forecast_df.rename(columns={"y_hat": "y"})
    forecast_df["Type"] = "Predicted"

    return forecast_df
