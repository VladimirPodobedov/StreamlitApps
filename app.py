# программа делает следующее:
# Загружает выбранный Excel-файл в pandas DataFrame.
# Посылает в чат gpt пользовательский запрос и получает SQL.
# Выполняет SQL-запрос (SELECT *) на этих данных.

import os
from groq import Groq
#from openai import OpenAI
import pandas as pd
import pandasql as ps
import sqlite3
from library import Lib
import streamlit as st

df = None
ui = None
fields = "name, price"
conditions = "" #My car is Porsche
question = "" #What is my car?

class UI:
    def title(self, str):
        #print(str)
        st.title(str)

    def output(self, str):
        #print(str)
        st.write(str)
       
    def input(self, str):
        return st.text_input(str)

    def input_with(self, str, end_char):
        return Lib.add_last_char_if_needed(st.text_input(str),end_char)

    def error(self, str):
        st.error(str)

    def checkbox(self, str):
        return st.checkbox(str)
        
    def get(self, prompt_string):
        return st.text_input(prompt_string)
        
    def file(self, prompt, file_type):
        return st.file_uploader(prompt+" ("+file_type+")", type=[file_type])

    def form(self, name):
        return st.form(name)
        
    def submit_button(self, str):
        return st.form_submit_button(str)
        
        
class TableXls:

    #df = None

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

    def not_empty(self, df):
        return df is not None
        
    def execute_sql(self, df, str):
        return ps.sqldf(str, locals())
        
        
class AI:

    """
    Class for access to service Groq - Chat GPT
    https://console.groq.com/playground
    org-id: org_01jkstbcz9e2ss1s5cdtvfaawd
    """

    secret_key = "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"
    ai_model = "gemma2-9b-it"   # "llama-3.3-70b-versatile"
    exception_error = None

    def error_code(self):
        return self.exception_error
        
    def set_model(self, model_name):
        self.ai_model = model_name

    def get_answer(self, question_string):
        exception_error = None
        client = Groq( 
            api_key = self.secret_key
        )
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": question_string,
                    }
                ],
                model = self.ai_model,
            )
            return chat_completion.choices[0].message.content

        except Exception as e:
            self.exception_error = e
            return None
        
        

# Основная функция программы
def main():
    
    ui =  UI()
    
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
        
            xls = TableXls()
            #df = xls.load_file(file_rules)
            df = xls.load_file(file_data)
           
            if xls.not_empty(df):
                
                xls.fields_normalize(df)
                
                if not question:
                    sql = """SELECT * FROM df """
                else:
                    user_query = conditions + "The table df has columns: " + xls.fields_string(df) +". "+" "+ question + " Show only SQL."
                    
                    user_query1 = f"""

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
                    ai = AI()
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