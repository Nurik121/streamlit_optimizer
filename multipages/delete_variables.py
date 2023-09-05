import streamlit as st

import func
import web.CRUD as CRUD

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
def delete_variables():
    st.subheader("Удаление переменных")

    name_from_db = CRUD.get_name()
    select_name = st.selectbox("Выберите имя набора для удаления", func.get_name(name_from_db))


    def button_delete(select_name):
        button = st.button('Удалить')
        if button:
            CRUD.delete_variables(select_name)
            st.sidebar.success(f"Данные были удалены из БД")

    button_delete(select_name)
