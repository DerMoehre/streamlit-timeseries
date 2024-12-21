import streamlit as st
import plotly.express as px

from shared.utils_fitting import (
    load_data_from_session,
    train_test_split,
    render_initial_sidebar,
    test_train_plot,
    get_model,
    fit_model,
    evaluate_performance,
)
from shared.utils_upload import is_data_in_session

st.set_page_config(page_title="Model Fitting", page_icon="🦾", layout="wide")

st.title("Model Fitting 🦾")

# Sidebar
split_ratio, model, selected_freq, season_length, season_mstl = render_initial_sidebar()

mae = None

if "last_evaluation" not in st.session_state:
    st.session_state.last_evaluation = None

if is_data_in_session():
    x_axis, y_axis, data = load_data_from_session()
    train_data, test_data = train_test_split(data, split_ratio)
    fig = test_train_plot(data, train_data, test_data, x_axis, y_axis, split_ratio)

    if st.sidebar.button("Fit Model"):
        selected_model = get_model(model, season_length, season_mstl)
        with st.spinner("Fitting Model..."):
            forecast, sf = fit_model(
                selected_model, train_data, test_data, selected_freq
            )
            st.session_state["fitted_model"] = sf
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
        current_evaluation = {"mae": mae, "r2": r2, "mape": mape}
        st.session_state["selected_model"] = selected_model
        st.session_state["freq"] = selected_freq
        st.session_state["season_length"] = season_length
        st.session_state["season_mstl"] = season_mstl
        st.session_state["split_ratio"] = split_ratio

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
                delta=None
                if st.session_state.last_evaluation is None
                else f"{mae - st.session_state.last_evaluation['mae']:.2f}",
                delta_color="inverse",
            )
        with col2:
            st.metric(
                label="R²",
                value=r2,
                help="Indicates how well the forecast explains the variance in the actual data. Values closer to 1 signify a better fit.",
                delta=None
                if st.session_state.last_evaluation is None
                else f"{r2 - st.session_state.last_evaluation['r2']:.2f}",
            )
        with col3:
            st.metric(
                label="Mean absolute percentage error",
                value=mape,
                help="Measures the average percentage error between actual and predicted values. Useful for comparing accuracy across scales.",
                delta=None
                if st.session_state.last_evaluation is None
                else f"{mape - st.session_state.last_evaluation['mape']:.2f}",
                delta_color="inverse",
            )
        st.session_state.last_evaluation = current_evaluation
else:
    st.error("You have to first update Data on the upload page.")
