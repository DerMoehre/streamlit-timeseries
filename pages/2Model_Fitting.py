import streamlit as st
import plotly.express as px

from shared.utils_fitting import load_data_from_session

st.set_page_config(page_title="Model Fitting", page_icon="🦾", layout="wide")


st.title("Model Fitting 🦾")

x_axis, y_axis, data = load_data_from_session()

# Plot
st.write(f"### Plot: {x_axis} vs {y_axis}")
fig = px.line(data, x="ds", y="y", title=f"{x_axis} vs {y_axis}")
fig.update_layout(xaxis_title=x_axis, yaxis_title=y_axis)
st.plotly_chart(fig, use_container_width=True)
