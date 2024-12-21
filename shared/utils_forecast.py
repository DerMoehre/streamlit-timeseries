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


def render_model_sidebar(model, freq, season_length, season_mstl):
    st.sidebar.header("Fitted Model")
    st.sidebar.write(f"**Model:** {model}")
    st.sidebar.write(f"**Frequency:** {freq}")
    st.sidebar.write(f"**Season Lenght:** {season_length}")
    if model == "MSTL":
        st.sidebar.write(f"**Second Season Lenght:** {season_mstl}")
    st.sidebar.divider()
    st.sidebar.header("Model Performance")


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
