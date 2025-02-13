from library import Lib
import streamlit as st

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

    def input_with_question(self, str, end_char):
        return Lib.add_last_char_if_needed_qm(st.text_input(str),end_char)

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
        
    def select_list(self, prompt, user_list):
        return st.selectbox(prompt, user_list)
        