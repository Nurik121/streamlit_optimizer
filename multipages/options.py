import ast
import streamlit as st
import sqlalchemy.exc
import pandas as pd

from func import get_name, parsing_data
import web.CRUD as CRUD
from web.schemas import Optmizers, DataOptimization

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def create_options():
    st.subheader("Добавление настроек оптимизации")
    name_from_db = CRUD.get_name()
    select_name = st.selectbox("Выберите имя набора", get_name(name_from_db))
    df_options = pd.DataFrame(ast.literal_eval(CRUD.get_options(select_name)))

    # Возможность редактирования таблиц
    edited_df = st.experimental_data_editor(df_options, num_rows="dynamic", width=1000)
    edited_dict = parsing_data(edited_df)
    print(edited_dict)
    if st.button("Загрузить в БД"):
        result = DataOptimization(name=select_name,options = str(edited_dict))
        CRUD.update_options(result)
        st.sidebar.success(f"Данные были обновлены")
