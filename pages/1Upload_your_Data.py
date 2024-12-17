import streamlit as st
import pandas as pd
import csv
import plotly.express as px


def detect_delimiter(data_string):
    """Detect the delimiter of a CSV file"""
    try:
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(data_string).delimiter
        return delimiter
    except Exception as e:
        return ","


def load_file(file):
    """Load the file into a DataFrame."""
    try:
        data_string = file.getvalue().decode("utf-8")  # Decode file content
        delimiter = detect_delimiter(data_string)
        file.seek(0)  # Reset file pointer for reading
        df = pd.read_csv(file, delimiter=delimiter)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def process_data(df, x_col=None, y_col=None):
    """Helper function to generate content from a DataFrame."""
    # Generate the graph
    fig = px.line(df, x=x_col, y=y_col, title=f"Plot: {x_col} vs {y_col}")
    # Data description
    description = df.describe()
    description_table = st.dataframe(description)

    # Return content
    return fig, description_table


st.set_page_config(page_title="Upload Data", page_icon="⬆️", layout="wide")

st.title("Upload Your Data and Visualize It 📊")
st.sidebar.header("Upload your data")

uploaded_file = st.sidebar.file_uploader("**Choose a file**", type=["csv", "txt"])

# Initialize variables
x_axis = None
y_axis = None

if uploaded_file is not None:
    # Load DataFrame
    dataframe = load_file(uploaded_file)

    if dataframe is not None:
        st.sidebar.success("File successfully loaded!")

        # Column Selection
        st.sidebar.header("Select Columns for Plot")
        x_axis = st.sidebar.selectbox(
            "**Select X-Axis**", dataframe.columns, key="x_axis"
        )
        y_axis = st.sidebar.selectbox(
            "**Select Y-Axis**", dataframe.columns, key="y_axis"
        )

        # Button to Confirm Selection
        if st.sidebar.button("Generate Plot"):
            # Layout: Plot at the top
            st.write(f"### Plot: {x_axis} vs {y_axis}")
            fig = px.line(dataframe, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
            st.plotly_chart(fig, use_container_width=True)

            # Layout: DataFrame and Description Side by Side
            col1, col2 = st.columns(2)  # Split the space into 2 columns

            with col1:
                st.write("### Data Preview")
                st.dataframe(dataframe)

            with col2:
                st.write("### Data Description")
                description = dataframe[[x_axis, y_axis]].describe()
                st.dataframe(description)
