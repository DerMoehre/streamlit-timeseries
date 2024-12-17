import streamlit as st
import pandas as pd
import csv


def detect_delimiter(data_string):
    """Detect the delimiter of a CSV file"""
    try:
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(data_string).delimiter
        return delimiter
    except Exception as e:
        return ","


def load_file(file):
    try:
        data_string = file.getvalue().decode("utf-8")
        delimiter = detect_delimiter(data_string)
        df = pd.read_csv(uploaded_file, delimiter=delimiter)
        return df
    except Exception as e:
        return e


st.set_page_config(page_title="Upload Data", page_icon="⬆️", layout="wide")

st.title("Upload your data")
st.sidebar.header("Upload your data")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    st.dataframe(load_file(uploaded_file), use_container_width=True)
