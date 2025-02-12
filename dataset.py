import pandas as pd
import pandasql as ps
import sqlite3
from library import Lib

df = None

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
    