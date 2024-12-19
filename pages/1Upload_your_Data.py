import streamlit as st
import pandas as pd
import csv
import plotly.express as px

from shared.utils_upload import (
    is_data_in_session,
    load_file,
    render_initial_main_content,
    process_data,
)

st.set_page_config(page_title="Upload Data", page_icon="⬆️", layout="wide")


st.title("Upload Your Data and Visualize It 📊")
st.sidebar.header("Upload your data")

# File uploader
if not is_data_in_session():
    uploaded_file = st.sidebar.file_uploader("**Choose a file**", type=["csv"])

if is_data_in_session():
    st.sidebar.write("### File Information:")
    st.sidebar.write(f"**Filename:** {st.session_state.get('filename', 'Unknown')}")
    dataframe = st.session_state["uploaded_data"]
    # Column Selection
    x_axis = st.sidebar.selectbox(
        "**Select X-Axis**",
        dataframe.columns,
        key="temp_x_axis",
        index=dataframe.columns.tolist().index(
            st.session_state.get("x_axis", dataframe.columns[0])
        ),
    )
    y_axis = st.sidebar.selectbox(
        "**Select Y-Axis**",
        dataframe.columns,
        key="temp_y_axis",
        index=dataframe.columns.tolist().index(
            st.session_state.get("y_axis", dataframe.columns[1])
        ),
    )
    # Update session state and render content when Submit is clicked
    if st.sidebar.button("Submit"):
        st.session_state["x_axis"] = x_axis
        st.session_state["y_axis"] = y_axis
        process_data()
    # Render the content when reloading
    if "x_axis" in st.session_state and "y_axis" in st.session_state:
        process_data()

    if st.sidebar.button("Delete Data"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.sidebar.success("Data deleted successfully!")
        st.rerun()


elif uploaded_file:
    # Load new file
    dataframe = load_file(uploaded_file)
    if dataframe is not None:
        st.sidebar.success("File successfully loaded!")
        # Column Selection
        st.sidebar.header("Select Columns for Plot")
        x_axis = st.sidebar.selectbox(
            "**Select X-Axis**", dataframe.columns, key="temp_x_axis"
        )
        y_axis = st.sidebar.selectbox(
            "**Select Y-Axis**", dataframe.columns, key="temp_y_axis"
        )

        # Button to Confirm Selection
        if st.sidebar.button("Submit"):
            st.session_state["filename"] = uploaded_file.name
            st.session_state["uploaded_data"] = dataframe
            st.session_state["x_axis"] = x_axis
            st.session_state["y_axis"] = y_axis
            process_data(dataframe, x_axis, y_axis)
else:
    render_initial_main_content()
