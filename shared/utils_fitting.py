import streamlit as st
import csv
import plotly.express as px
import pandas as pd

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
