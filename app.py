# программа делает следующее:
# Загружает выбранный Excel-файл в pandas DataFrame.
# Посылает в чат gpt пользовательский запрос и получает SQL.
# Выполняет SQL-запрос (SELECT *) на этих данных.

import os
import pandas as pd
import pandasql as ps
import sqlite3

from library import Lib
import ui_streamlit
import ai_groq

df = None
ui = None
conditions = "" #My car is Porsche
question = "" #What is my car?
   
        
class TableXls:

    def load_file(self, file_path):
        try:
            return pd.read_excel(file_path)
        
        except Exception as e:
            ui.error(f"File upload error: {e}")
            return None
            
    # Datafield normalize
    def fields_normalize(self, df):
        if df is not None:

            old_fields_list = list(df.columns)
            new_fields_list = Lib.list_normalize(old_fields_list, " /*`""", "_")
            result = Lib.map_without_duplicates(old_fields_list, new_fields_list)
            df.rename(columns=result, inplace=True)
            
    def fields_string(self, df):
        if df is not None:
            return ', '.join(Lib.list_normalize(list(df.columns), " /*`""", "_"))
        else:
            return None

    def empty(self, df):
        return df is None
        
    def execute_sql(self, df, str):
        return ps.sqldf(str, locals())

    def sql_normalize(self, sql):
        sql = sql.replace('!=', '<>')
        sql = sql.replace("'", '"')
        sql = sql.replace(";", '')
        return sql

# Основная функция программы
def main():
    
    ui =  ui_streamlit.UI()
    df = None
    user_query = ''
    sql = ''
    sql_result = ''
    
    ui.title("Natural language SQL")
    with ui.form("my_form"): 
        ai_model = ui.select_list("Select an AI assistant model:",
                (
                    'gemma2-9b-it',
                    'deepseek-r1-distill-llama-70b',
                    'deepseek-r1-distill-qwen-32b',
                    'llama-3.1-8b-instant',
                    'llama-3.2-11b-vision-preview',
                    'llama-3.2-1b-preview',
                    'llama-3.2-3b-preview',
                    'llama-3.2-90b-vision-preview',
                    'llama-3.3-70b-specdec',
                    'llama-3.3-70b-versatile',
                    'llama-guard-3-8b',
                    'llama3-70b-8192',
                    'llama3-8b-8192',
                    'mixtral-8x7b-32768',
                    'qwen-2.5-32b'                
                ),
        )


        file_data = ui.file("Select the data file", 'xls')    
        conditions = ui.input_with("Used rules:",'.')
        question = ui.input_with_question("Your question:",'.')
        show_sql = ui.checkbox("show debug information")
        
        if ui.submit_button(f":red[ RUN ]"):
        
            xls = TableXls()
            #df = xls.load_file(file_rules)
            
            
            try:
                df = xls.load_file(file_data)
            except Exception as e:
                ui.error(f"File download failure: {e}")
               
           
            if df is None:
                ui.error("File has'nt been downloaded")
                return
                
            xls.fields_normalize(df)
            
            if not question:
                sql = """SELECT * FROM df """
            else:
                user_query = f"""{conditions} The table df has columns: {xls.fields_string(df)}. {question} Show only SQL in SQLite syntax."""
                
                user_query_template = f"""

                    My car is Porsche. 

                    Given the following database schema:
                    Table: df
                    Columns:
                    - name_of_car: TEXT
                    - price: INTEGER
                    - year: TEXT (in format YYYY)
                    
                    Translate the following natural language query into SQL:
                    
                    {question}
                    
                    Show only SQL.
                """
                ai = ai_groq.AI()
                ai.set_model(ai_model)
                sql = ai.get_answer(user_query)
                sql = xls.sql_normalize(sql)
                
                
                #sql = "SELECT name_of_car FROM df WHERE name_of_car <> 'Porsche' ORDER BY price ASC LIMIT 1"
                
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