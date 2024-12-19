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
    return {
        "AutoARIMA": AutoARIMA,
        "SeasonalNaive": SeasonalNaive,
        "HoltWinters": HoltWinters,
        "HistoricAverage": HistoricAverage,
        "MSTL": MSTL,
    }


def test_train_plot(data, train_data, test_data, x_axis, y_axis, split_ratio):
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
    fig.update_layout(
        xaxis_title="Date", yaxis_title="Values", legend_title="Data Split"
    )

    st.write(
        f"### Train-Test Split Visualization ({split_ratio}% Train, {100 - split_ratio}% Test)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # return
