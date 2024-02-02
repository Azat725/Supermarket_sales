import pandas as pd 
import streamlit as st
import plotly.express as px
import openpyxl

# Устанавливаем конфигурацию страницы
st.set_page_config(
    page_title="Supermarket Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

# Загрузка данных из файла Excel
@st.cache_resource
def get_data_from_excel():
    # file_path = r"C:\Users\Ildar\Desktop\Azat\programming\Python\Supermarket_sales\other_elements\Supermarket_sales.xlsx"

    df = pd.read_excel(
        io=r"C:\Users\Ildar\Desktop\Azat\programming\Python\Supermarket_sales\other_elements\Supermarket_sales.xlsx",
        engine="openpyxl",
        sheet_name="Лист1",
        usecols="B:R",
        skiprows=3
    )

    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

# Получаем данные
df = get_data_from_excel()

# Фильтры
st.sidebar.header("Filter here:")
city = st.sidebar.multiselect("Select the city", options=df["City"].unique(), default=df["City"].unique())
customer = st.sidebar.multiselect("Select the customer", options=df["Customer_type"].unique(), default=df["Customer_type"].unique())
gender = st.sidebar.multiselect("Select the gender", options=df["Gender"].unique(), default=df["Gender"].unique())

# Применяем фильтры к данным
df_selection = df.query("City == @city & Customer_type == @customer & Gender == @gender")

# Дашборд
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# Общие показатели
total_sales = df_selection["Total"].sum()
average_rating = df_selection["Rating"].mean()
average_rating_by_transaction = df_selection["Total"].mean()

# Выводим общие показатели
st.subheader("Total Sales")
st.subheader(f"US $ {total_sales:,.0f}")

st.subheader("Average Rating")
st.subheader(f"{average_rating:.1f} ★" + " " * int(round(average_rating, 0)))

st.subheader("Average Sales Per Transaction")
st.subheader(f"US $ {average_rating_by_transaction:.2f}")

st.markdown("---")

# График продаж по типам продуктов
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

# График продаж по часам
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