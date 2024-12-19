import streamlit as st
import pandas as pd
import csv
import plotly.express as px

st.set_page_config(page_title="Upload Data", page_icon="⬆️", layout="wide")


def render_initial_main_content():
    # Instructions when no data is uploaded
    st.markdown(
        """
        ## Procedure
        1. Upload your file on the right side 👈
        2. Choose the right columns in your data for the **X** and **Y** axis
        3. Submit your choice with the button
        You will get the plotted graph, a brief description of the input data, and the data itself.
        """
    )


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


def transform_df_nixtla(df, x_col, y_col):
    df_transformed = df[[x_col, y_col]].rename(columns={x_col: "ds", y_col: "y"})
    df_transformed.insert(0, "unique_id", "time-analysis")
    return df_transformed


def is_data_in_session():
    """Check if data is stored in session"""
    return (
        "uploaded_data" in st.session_state
        and st.session_state["uploaded_data"] is not None
        and "x_axis" in st.session_state
        and "y_axis" in st.session_state
    )


def process_data(df=None, x_col=None, y_col=None):
    """Process the DataFrame and generate content."""
    # Use session state if inputs are not provided
    if df is None:
        df = st.session_state.get("uploaded_data")
    if x_col is None:
        x_col = st.session_state.get("x_axis")
    if y_col is None:
        y_col = st.session_state.get("y_axis")

    # Save transformed data to session
    if "transformed_data" not in st.session_state:
        st.session_state["transformed_data"] = transform_df_nixtla(df, x_col, y_col)

    # Plot
    st.write(f"### Plot: {x_col} vs {y_col}")
    fig = px.line(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
    st.plotly_chart(fig, use_container_width=True)

    # Layout: DataFrame and description side by side
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Data Preview")
        st.dataframe(df, use_container_width=True)
    with col2:
        st.write("### Data Description")
        description = df[[x_col, y_col]].describe()
        st.dataframe(description, use_container_width=True)


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
