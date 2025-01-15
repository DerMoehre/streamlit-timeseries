import streamlit as st
import csv
import plotly.express as px
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose 
import matplotlib.pyplot as plt


####### PAGE 1: Upload your Data #######


def select_columns(dataframe):
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
    return x_axis, y_axis


def render_initial_main_content():
    # Instructions when no data is uploaded
    st.markdown(
        """
        ## Procedure
        1. Upload your file on the left side 👈
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

    # Save transformed data to session
    if "transformed_data" not in st.session_state:
        st.session_state["transformed_data"] = transform_df_nixtla(df, x_col, y_col)

    # Plot
    st.write(f"### Plot: {x_col} vs {y_col}")
    fig = px.line(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
    season_data = seasonal_decompose(df[y_col], model = "add", period=12)
    st.plotly_chart(fig, use_container_width=True)

    decompose_df = pd.DataFrame({
        'date': df.index,
        'observed': season_data.observed,
        'trend': season_data.trend,
        'seasonal': season_data.seasonal,
        'residual': season_data.resid
    })

    decomposed_df_long = decompose_df.melt(id_vars="date", value_vars=['observed', 'trend', 'seasonal', 'residual'],
                                        var_name='component', value_name='value')

    # Plot the decomposition using Plotly Express
    fig_season = px.line(decomposed_df_long, x='date', y='value', color='component', 
              title="Decomposed Time Series", labels={'value': 'Value', 'date': 'Date'})

    # Show the plot in Streamlit
    st.plotly_chart(fig_season)

    # Layout: DataFrame and description side by side
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Data Preview")
        st.dataframe(df, use_container_width=True)
    with col2:
        st.write("### Data Description")
        description = df[[x_col, y_col]].describe()
        st.dataframe(description, use_container_width=True)
