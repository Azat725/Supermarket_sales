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

st.sidebar.header("Filter here:")
city = st.sidebar.multiselect("Select the city", options=df["City"].unique(), default=df["City"].unique())
customer = st.sidebar.multiselect("Select the customer", options=df["Customer_type"].unique(), default=df["Customer_type"].unique())
gender = st.sidebar.multiselect("Select the gender", options=df["Gender"].unique(), default=df["Gender"].unique())

df_selection = df.query("City == @city & Customer_type == @customer & Gender == @gender")



st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

total_sales = df_selection["Total"].sum()
average_rating = df_selection["Rating"].mean()
average_rating_by_transaction = df_selection["Total"].mean()

st.subheader("Total Sales")
st.subheader(f"US $ {total_sales:,.0f}")

st.subheader("Average Rating")
st.subheader(f"{average_rating:.1f} ★" + " " * int(round(average_rating, 0)))

st.subheader("Average Sales Per Transaction")
st.subheader(f"US $ {average_rating_by_transaction:.2f}")

st.markdown("---")

sales_by_product_line = df_selection.groupby("Product line")["Total"].sum().sort_values()
fig_product_sales = px.bar(
    sales_by_product_line,
    x=sales_by_product_line.index,
    y="Total",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#fc2b51"] * len(sales_by_product_line),
    template="plotly_white"
)
st.plotly_chart(fig_product_sales, use_container_width=True)

sales_by_hour = df_selection.groupby("hour")["Total"].sum().reset_index()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x="hour",
    y="Total",
    title="<b>Sales by Hour</b>",
    color_discrete_sequence=["#fc2b51"] * len(sales_by_hour),
    template="plotly_white"
)

fig_hourly_sales.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(showgrid=False))
st.plotly_chart(fig_hourly_sales, use_container_width=True)