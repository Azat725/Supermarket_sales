import pandas as pd  # Импорт библиотеки pandas для работы с данными
import streamlit as st  # Импорт библиотеки Streamlit для создания веб-приложений
import plotly.express as px  # Импорт библиотеки Plotly Express для создания интерактивных графиков
from openpyxl import load_workbook # Импорт библиотеки openpyxl для работы с Excel файлами

# Устанавливаем конфигурацию страницы
st.set_page_config(
    page_title="Supermarket Dashboard",  # Название страницы
    page_icon=":bar_chart:",  # Иконка страницы
    layout="wide"  # Широкий формат страницы
)

# Загрузка данных из файла Excel
@st.cache_resource  # Кэширование данных для повышения производительности
def get_data_from_excel():
    file_path = r"C:\Users\Ildar\Desktop\Azat\programming\Python\проекты\Supermarket_sales\other_elements\Supermarket_sales.xlsx"

    df = pd.read_excel(  # Чтение данных из файла Excel
        io=file_path,
        engine="openpyxl",
        sheet_name="Лист1",
        usecols="B:R",
        skiprows=3
    )

    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour  # Извлечение часа из столбца времени
    return df

# Получаем данные
df = get_data_from_excel()

# Фильтры
st.sidebar.header("Filter here:")  # Заголовок для боковой панели с фильтрами
city = st.sidebar.multiselect("Select the city", options=df["City"].unique(), default=df["City"].unique(), key="city_filter")  # Фильтр по городу
customer = st.sidebar.multiselect("Select the customer", options=df["Customer_type"].unique(), default=df["Customer_type"].unique(), key="customer_filter")  # Фильтр по типу покупателя
gender = st.sidebar.multiselect("Select the gender", options=df["Gender"].unique(), default=df["Gender"].unique(), key="gender_filter")  # Фильтр по полу

# Применение CSS для изменения цвета кнопок фильтра
st.markdown(
    '<style>'
    'div[data-baseweb="select"] button[role="option"] { background-color: purple !important; border-color: purple !important; color: white !important; }'
    '</style>',
    unsafe_allow_html=True
)


# HTML-стили для фильтров
st.markdown("""
<style>
.sidebar .multiselect-placeholder {
    color: purple;
}
</style>
""", unsafe_allow_html=True)

# Применяем фильтры к данным
df_selection = df.query("City == @city & Customer_type == @customer & Gender == @gender")

# Дашборд
st.title(":bar_chart: Sales Dashboard")  # Заголовок дашборда
st.markdown("##")  # Разделительная строка

# Общие показатели
total_sales = df_selection["Total"].sum()
average_rating = df_selection["Rating"].mean()
average_rating_by_transaction = df_selection["Total"].mean()

# Выводим общие показатели
st.subheader("Total Sales")  # Подзаголовок "Общий объем продаж"
st.subheader(f"US $ {total_sales:,.0f}")  # Вывод общего объема продаж в формате долларов

st.subheader("Average Rating")  # Подзаголовок "Средний рейтинг"
st.subheader(f"{average_rating:.1f} ★" + " " * int(round(average_rating, 0)))  # Вывод среднего рейтинга с символом звезды

st.subheader("Average Sales Per Transaction")  # Подзаголовок "Средний объем продаж за транзакцию"
st.subheader(f"US $ {average_rating_by_transaction:.2f}")  # Вывод среднего объема продаж за транзакцию

st.markdown("---")  # Горизонтальная линия для разделения

# График продаж по типам продуктов
sales_by_product_line = df_selection.groupby("Product line")["Total"].sum().sort_values()  # Группировка продаж по типам продуктов
fig_product_sales = px.bar(  # Создание столбчатой диаграммы
    sales_by_product_line,
    x=sales_by_product_line.index,
    y="Total",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=['#800080', '#9400D3', '#8A2BE2', '#9932CC', '#BA55D3', '#9370DB'] * len(sales_by_product_line),
    template="plotly_white"  # Шаблон диаграммы
)

fig_product_sales.update_layout(
    plot_bgcolor='black'  # Устанавливаем черный фон
)

st.plotly_chart(fig_product_sales, use_container_width=True) # Отображение столбчатой диаграммы продаж по типам продуктов

# График продаж по часам
sales_by_hour = df_selection.groupby("hour")["Total"].sum().reset_index() # Группировка продаж по часам

fig_hourly_sales = px.bar(  # Создание столбчатой диаграммы
    sales_by_hour,
    x="hour",
    y="Total",
    title="<b>Sales by Hour</b>",
    color_discrete_sequence=['#800080', '#9400D3', '#8A2BE2', '#9932CC', '#BA55D3', '#9370DB'] * len(sales_by_hour),
    template="plotly_white"  # Шаблон диаграммы
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0, 0, 0, 0)",
    yaxis=dict(showgrid=False)  # Настройка макета диаграммы
)

st.plotly_chart(fig_hourly_sales, use_container_width=True)  # Отображение столбчатой диаграммы продаж по часам
