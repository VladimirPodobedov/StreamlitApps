# программа загружает выбранный excel файл в pandas, читает имена столбцов и делает sql запрос и выводит результат

# программа делает следующее:
# Загружает выбранный Excel-файл в pandas DataFrame.
# Выводит имена столбцов.
# Создает временную базу данных SQLite.
# Записывает данные из DataFrame в эту базу.
# Выполняет простой SQL-запрос (SELECT *) на этих данных.
# Чтобы использовать более сложные SQL-запросы или конкретные условия фильтрации, просто измените строку query внутри функции execute_sql_query.

import streamlit as st
from openai import OpenAI
import pandas as pd
import pandasql as ps
import sqlite3
import re


OPEN_KEY = "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"

fields = "name, price"
conditions = "Если говорю моя машина, то имей в виду Porsсhe."
question = "сколько стоит моя машина"

def extract_substring_regex(text):
    pattern = r'(?<=\`\`\`sql).*?(?=\`\`\`)'
    match = re.search(pattern, text, flags=re.DOTALL)
    
    if match:
        return match.group()
        
        
def output_title(str):
    #print(str)
    st.title(str)

def output_str(str):
    #print(str)
    st.write(str)

def get_excel_file(prompt, file_type):
    return st.file_uploader(prompt+" ("+file_type+")", type=[file_type])

# Функция для загрузки данных из Excel-файла в DataFrame
def load_excel_to_df(file_path):
    try:
        # Загрузка данных из Excel-файла
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        output_str(f"Ошибка при загрузке файла: {e}")
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
            output_str(row)  # Выводим результат
        
    except Exception as e:
        output_str(f"Ошибка при выполнении запроса: {e}")

# Основная функция программы
def main():

    # Создание интерфейса для выбора файла
    output_title("Natural language SQL")
    
#    file_rules = get_excel_file("Select the rule file", 'xls')
    file_data = get_excel_file("Select the data file", 'xls')    
    
    conditions = st.text_input("Write conditions here")
    if conditions[-1:] != '.':
        conditions = conditions + '.'
        
    question = st.text_input("Write the query string here")
    if question[-1:] != '?':
        question = question + '?'
    
    if st.button(" RUN "):
    
#        df1 = load_excel_to_df(file_rules)
        df = load_excel_to_df(file_data)
        if df is not None:
        
        
            fields = ', '.join(list(df.columns))
            #output_str(result_string)
        
            # Выполняем запрос и выводим результат
            #execute_sql_query(df)
            
            if not question:
                sql_query = """SELECT * FROM df """
            else:
                user_query = "Show only SQL. The table df has columns: "+fields+". "+conditions +" "+ question
                output_str(user_query)
                
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=OPEN_KEY,
                )
                try:
                    completion = client.chat.completions.create(
                        extra_headers={
                            "HTTP-Referer": "https://gsktb.com", # Optional. Site URL for rankings on openrouter.ai.
                            "X-Title": "https://gsktb.com", # Optional. Site title for rankings on openrouter.ai.
                        },
                        extra_body={},
                        model="deepseek/deepseek-r1:free",
                        messages=[{
                            "role": "user",
                            "content": user_query
                        }]
                    )
                except Exception as e:
                    output_str(f"Ошибка при выполнении запроса: {e}")
                    
                sql_query = extract_substring_regex(completion.choices[0].message.content)
            
            output_str(f"SQL: {sql_query}")
            output_str(ps.sqldf(sql_query, locals()))


            
if __name__ == "__main__":
    main()