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

st.sidebar.header("Filter here:")
city = st.sidebar.multiselect("Select the city", options=df["City"].unique(), default=df["City"].unique())
customer = st.sidebar.multiselect("Select the customer", options=df["Customer_type"].unique(), default=df["Customer_type"].unique())
gender = st.sidebar.multiselect("Select the gender", options=df["Gender"].unique(), default=df["Gender"].unique())

df_selection = df.query("City == @city & Customer_type == @customer & Gender == @gender")