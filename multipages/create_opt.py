import streamlit as st
import sqlalchemy.exc
import web.CRUD as CRUD

from web.schemas import Optmizers

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def create_opt():
    st.subheader("Создание оптимизации")
    name_opt = st.text_input('Введите имя оптимизации')
    description = st.text_input('Введите описание оптимизации')
    if st.button("Загрузить в БД"):
        try:
            result = Optmizers(name=name_opt, description=description)
            CRUD.create_opt(result)
            st.sidebar.success(f"Данные были загружены в БД")
        except sqlalchemy.exc.IntegrityError as e:
            st.sidebar.error(f"Такая оптимизация уже существует!")