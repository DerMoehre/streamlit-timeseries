import streamlit as st
import plotly.express as px

from shared.utils_fitting import (
    load_data_from_session,
)
from shared.utils_forecast import (
    forecast_plot,
    render_model_sidebar,
    forecast,
    load_model_data_from_session,
    is_model_data_in_session,
)


st.set_page_config(page_title="Forecasting", page_icon="🚀", layout="wide")

st.title("Forecasting 🚀")

forecasted_data = None

if is_model_data_in_session():
    x_axis, y_axis, data = load_data_from_session()
    (
        selected_model,
        model_name,
        selected_freq,
        season_length,
        season_mstl,
        split_ratio,
    ) = load_model_data_from_session()
    fig = forecast_plot(data, x_axis, y_axis, selected_model)
    forecast_horizon = render_model_sidebar(
        model_name, selected_freq, season_length, season_mstl
    )
    if st.sidebar.button("Forecast"):
        with st.spinner("Forecasting..."):
            forecasted_data = forecast(
                selected_model, data, forecast_horizon, selected_freq, season_mstl
            )
            fig = forecast_plot(data, x_axis, y_axis, str(model_name), forecasted_data)
    st.plotly_chart(fig, use_container_width=True)
    if forecasted_data is not None:
        st.dataframe(forecasted_data, use_container_width=True)
else:
    st.error("You have to first fit a model.")
