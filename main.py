# программу на python которая загружает выбранный exce файл в pandas, читает имена столбцов и делает sql запрос и выводит результат

# программа делает следующее:
# Загружает выбранный Excel-файл в pandas DataFrame.
# Выводит имена столбцов.
# Создает временную базу данных SQLite.
# Записывает данные из DataFrame в эту базу.
# Выполняет простой SQL-запрос (SELECT *) на этих данных.
# Чтобы использовать более сложные SQL-запросы или конкретные условия фильтрации, просто измените строку query внутри функции execute_sql_query.

# https://www.youtube.com/watch?v=D0D4Pa22iG0
import streamlit as st

import pandas as pd
import pandasql as ps
import sqlite3

# Функция для загрузки данных из Excel-файла в DataFrame
def load_excel_to_df(file_path):
    try:
        # Загрузка данных из Excel-файла
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return None

# Функция для создания базы данных SQLite и выполнения запроса
def execute_sql_query(df):
    try:
        # Создание базы данных SQLite в памяти (для простоты)
        conn = sqlite3.connect(':memory:')
        
        # Запись DataFrame в таблицу базы данных SQLite
        df.to_sql('data', conn, if_exists='replace', index=False)

        # Выполнение SQL-запроса (например, выборка всех столбцов)
        cursor = conn.cursor()
        
        # Прочитаем все столбцы из DataFrame (теперь таблицы 'data')
        columns = list(df.columns)
        
        query = f"SELECT * FROM data LIMIT 2"
        cursor.execute(query)
        
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)  # Выводим результат
        
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")

# Основная функция программы
def main():

    # Создание интерфейса для выбора файла
    #file_path = input("Введите путь к вашему Excel-файлу (.xlsx): ")
    st.title("Natural language SQL")
    uploaded_rules_file = st.file_uploader("Select the rule file (xls)", type=['xls'])
    df1 = load_excel_to_df(uploaded_rules_file)

    uploaded_data_file = st.file_uploader("Select the data file (xls)", type=['xls'])
    df = load_excel_to_df(uploaded_data_file)
    
    s = st.text_input("Write the query string here")
    
    if df is not None:
        
        if st.button(" RUN "):
        
            columns_list = list(df.columns)
        
            # Выводим имена столбцов перед выполнением запроса 
            #print("Имена столбцов:")
            #print(list(df.columns))
            #st.write("Имена столбцов:")
            #st.write(list(df.columns))
        
        
            # Выполняем запрос и выводим результат
            #execute_sql_query(df)
            q1 = """SELECT `name of car`, price FROM df """
            #print(ps.sqldf(q1, locals()))
            st.write(f"Result by query: {s}")
            st.write(ps.sqldf(q1, locals()))


if __name__ == "__main__":
    main()