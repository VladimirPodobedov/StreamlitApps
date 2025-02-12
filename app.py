# программа делает следующее:
# Загружает выбранный Excel-файл в pandas DataFrame.
# Посылает в чат gpt пользовательский запрос и получает SQL.
# Выполняет SQL-запрос (SELECT *) на этих данных.

import os
from groq import Groq
#from openai import OpenAI
import pandas as pd
#import pandasql as ps
#import sqlite3
from library import Lib
import streamlit_ui
import ai_helper
import dataset

ui = None
fields = "name, price"
conditions = "" #My car is Porsche
question = "" #What is my car?


# Основная функция программы
def main():
    xls = dataset.TableXls()
    ui =  streamlit_ui.UI()
    
    user_query = ''
    sql = ''
    sql_result = ''
    
    ui.title("Natural language SQL")
    with ui.form("my_form"):
        file_data = ui.file("Select the data file", 'xls')    
        conditions = ui.input_with("Used rules:",'.')
        question = ui.input_with("Your question:",'?')
        show_sql = ui.checkbox("show debug information")
        
        if ui.submit_button(f":red[ RUN ]"):
        
            #df = xls.load_file(file_rules)
            df = xls.load_file(file_data)
           
            if xls.not_empty(df):
                
                xls.fields_normalize(df)
                
                if not question:
                    sql = """SELECT * FROM df """
                else:
                    user_query = "Show only SQL. The table df has columns: " + xls.fields_string(df) +". "+conditions +" "+ question
                    
                    ai = ai_helper.AI()
                    sql = ai.get_answer(user_query)
                    
                    if (error := ai.error_code()) is not None:
                        ui.error(f"GPT access error: {error}")
                        return
                    try:
                        sql = Lib.extract_substring_regex(sql)
                    except Exception as e:
                        ui.error(f"Error in response: {e}")
                
                if sql is not None:
                    try:
                        sql_result = xls.execute_sql(df,sql)
                        
                    except Exception as e:
                        ui.error(f"Request execution error: {e}")

    
    if user_query or sql:
        if show_sql:
            ui.output(user_query)
            ui.output(f"SQL: {sql}")
        ui.output(sql_result)
            
if __name__ == "__main__":
    main()