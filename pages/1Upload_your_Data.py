import streamlit as st
import pandas as pd
from shared.utils_upload import (
    is_data_in_session,
    load_file,
    render_initial_main_content,
    process_data,
    select_columns,
)

st.set_page_config(page_title="Upload Data", page_icon="⬆️", layout="wide")

st.title("Upload Your Data and Visualize It 📊")
st.sidebar.header("Upload your data")


# Handle file upload and session data
if not is_data_in_session():
    uploaded_file = st.sidebar.file_uploader("**Choose a file**", type=["csv"])
    if uploaded_file:
        dataframe = load_file(uploaded_file)
        if dataframe is not None:
            st.sidebar.success("File successfully loaded!")
            x_axis, y_axis = select_columns(dataframe)
            if st.sidebar.button("Submit"):
                st.session_state.update(
                    {
                        "filename": uploaded_file.name,
                        "uploaded_data": dataframe,
                        "x_axis": x_axis,
                        "y_axis": y_axis,
                    }
                )
                process_data(dataframe, x_axis, y_axis)
else:
    st.sidebar.write("### File Information:")
    st.sidebar.write(f"**Filename:** {st.session_state.get('filename', 'Unknown')}")
    dataframe = st.session_state["uploaded_data"]
    x_axis, y_axis = select_columns(dataframe)

    if st.sidebar.button("Submit"):
        st.session_state.update(
            {
                "x_axis": x_axis,
                "y_axis": y_axis,
            }
        )
        process_data(dataframe, x_axis, y_axis)

    if st.sidebar.button("Delete Data"):
        st.session_state.clear()
        st.sidebar.success("Data deleted successfully!")
        st.rerun()

# Render initial content if no data
if not is_data_in_session():
    render_initial_main_content()
