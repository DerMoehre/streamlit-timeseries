import streamlit as st
import plotly.express as px

from shared.utils_fitting import load_data_from_session, train_test_split

st.set_page_config(page_title="Model Fitting", page_icon="🦾", layout="wide")


st.title("Model Fitting 🦾")

x_axis, y_axis, data = load_data_from_session()

# Sidebar
st.sidebar.header("Train-Test Split")
split_ratio = st.sidebar.slider(
    "Select Train-Test Split Ratio (%)", min_value=50, max_value=90, value=70, step=1
)

train_data, test_data = train_test_split(data, split_ratio)

# Plot
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
fig.update_layout(xaxis_title="Date", yaxis_title="Values", legend_title="Data Split")

st.write(
    f"### Train-Test Split Visualization ({split_ratio}% Train, {100 - split_ratio}% Test)"
)
st.plotly_chart(fig, use_container_width=True)
