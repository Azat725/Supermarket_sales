import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Supermaarket Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)

file_path = r"C:/Users/Ildar/Desktop/Khajrullin_Azat/Supermarket_sales/other_elements/Supermarket_sales.xlsx"
df = pd.read_excel(
    io=file_path,
    engine="openpyxl",
    sheet_name="Лист1",
    usecols="B:R",
    nrows=206,
    skiprows=3
)

st.dataframe(df)