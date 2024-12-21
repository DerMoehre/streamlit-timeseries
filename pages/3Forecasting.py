import streamlit as st
import plotly.express as px

from shared.utils_upload import is_data_in_session
from shared.utils_fitting import (
    load_data_from_session,
    load_model_data_from_session,
)
from shared.utils_forecast import (
    forecast_plot,
    render_model_sidebar,
)


st.set_page_config(page_title="Forecasting", page_icon="🚀", layout="wide")

st.title("Forecasting 🚀")

st.write(st.session_state)

if is_data_in_session():
    x_axis, y_axis, data = load_data_from_session()
    (
        selected_model,
        selected_freq,
        season_length,
        season_mstl,
        split_ratio,
    ) = load_model_data_from_session()
    render_model_sidebar(selected_model, selected_freq, season_length, season_mstl)
    fig = forecast_plot(data, x_axis, y_axis, selected_model)
    st.plotly_chart(fig, use_container_width=True)
