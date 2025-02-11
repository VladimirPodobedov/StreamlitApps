# программа делает следующее:
# Загружает выбранный Excel-файл в pandas DataFrame.
# Посылает в чат gpt пользовательский запрос и получает SQL.
# Выполняет SQL-запрос (SELECT *) на этих данных.

import os
from groq import Groq
#from openai import OpenAI
import streamlit as st
import pandas as pd
import pandasql as ps
import sqlite3
import re


fields = "name, price"
conditions = "" #My car is Porsche
question = "" #What is my car?

#------------------------------------------------------------------------------
def extract_substring_regex(text):
    pattern = r'(?<=\`\`\`sql).*?(?=\`\`\`)'
    match = re.search(pattern, text, flags=re.DOTALL)
    
    if match:
        return match.group()
       
def add_last_char_if_needed(str,ch):
    if str and (str[-1:] != ch):
        str = str + ch
    return str
    
#------------------------------------------------------------------------------
def UI_create_title(str):
    #print(str)
    st.title(str)

#------------------------------------------------------------------------------
def UI_output_str(str):
    #print(str)
    st.write(str)

#------------------------------------------------------------------------------
def UI_get_string(prompt_string):
    return st.text_input(prompt_string)
    
#------------------------------------------------------------------------------
def UI_get_excel_file(prompt, file_type):
    return st.file_uploader(prompt+" ("+file_type+")", type=[file_type])


#------------------------------------------------------------------------------
# Groq - Chat GPT
# https://console.groq.com/playground
# org-id: org_01jkstbcz9e2ss1s5cdtvfaawd
def ai_groq_get_query(user_query_string):
    client = Groq( 
        api_key="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" 
    )
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_query_string,
                }
            ],
            #model="llama-3.3-70b-versatile",
            model="gemma2-9b-it",
        )
        return chat_completion.choices[0].message.content

    except Exception as e:

        st.error(f"Ошибка обращения к GPT: {e}")
        return None

#------------------------------------------------------------------------------
# Функция для загрузки данных из Excel-файла в DataFrame
def load_excel_to_df(file_path):
    try:
        # Загрузка данных из Excel-файла
        df = pd.read_excel(file_path)
        return df
    
    except Exception as e:
        st.error(f"Ошибка при загрузке файла: {e}")
        return None


# Основная функция программы
def main():
    user_query = ''
    sql_query_string = ''
    sql_result = ''
    
    UI_create_title("Natural language SQL")
    with st.form("my_form"):
        #st.subheader("This is a subheader")
        #file_rules = UI_get_excel_file("Select the rule file", 'xls')
        file_data = UI_get_excel_file("Select the data file", 'xls')    
        conditions = add_last_char_if_needed(st.text_input("Write conditions here"),'.')
        question = add_last_char_if_needed(st.text_input("Write the query string here"),'?')
        show_sql = st.checkbox("show query")
        
        if st.form_submit_button(f":red[ RUN ]"):
        
            #df1 = load_excel_to_df(file_rules)
            df = load_excel_to_df(file_data)
            if df is not None:

                fields = ', '.join(list(df.columns))

                if not question:
                    sql_query = """SELECT * FROM df """
                else:
                    user_query = "Show only SQL. The table df has columns: "+fields+". "+conditions +" "+ question
                    #UI_output_str(user_query)
                    sql_query = extract_substring_regex(ai_groq_get_query(user_query))
                
                if sql_query is not None:
                    sql_query_string = f"SQL: {sql_query}"
                    sql_result = ps.sqldf(sql_query, locals())

    
    if user_query or sql_query_string:
        if show_sql:
            UI_output_str(user_query)
            UI_output_str(sql_query_string)
        UI_output_str(sql_result)
            
if __name__ == "__main__":
    main()