import streamlit as st
import plotly.express as px

from shared.utils_fitting import (
    load_data_from_session,
    train_test_split,
    return_imported_models,
    test_train_plot,
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
    "Select Model", [model_list[model] for model in model_list]
)

if is_data_in_session():
    x_axis, y_axis, data = load_data_from_session()
    train_data, test_data = train_test_split(data, split_ratio)
    test_train_plot(data, train_data, test_data, x_axis, y_axis, split_ratio)

else:
    st.error("You have to first update Data on the upload page.")
