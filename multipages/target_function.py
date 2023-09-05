import streamlit as st

import web.CRUD as CRUD
import func
from web.schemas import DataOptimization

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
def target_func():
    st.subheader("Целевая функция")
    name_from_db = CRUD.get_name()
    select_name = st.selectbox("Выберите имя набора", func.get_name(name_from_db))
    target = CRUD.get_target(select_name)
    st.markdown('Целевая функция должна быть следующего вида:')
    st.markdown(':red[([ISOM_FEED] - [KPA_HK62_TOISOM]) * [KPA_HK62_TOISOM]/1000]')
    target_func = st.text_input('Введите свою целевую функцию', target)
    button_create_target = st.button('Добавить/Обновить целевую функцию')
    if button_create_target:
        result = DataOptimization(name=select_name, obj=target_func)
        CRUD.create_target(result)
        st.sidebar.success(f"Данные были загружены в БД")
