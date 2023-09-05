import streamlit as st

import func
import web.CRUD as CRUD

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
def delete_opt():
    st.subheader("Удаление оптимизации")

    name_opt = CRUD.get_name_opt()
    select_optimizer = st.selectbox("Выберите имя оптимизации для удаления", func.get_name(name_opt))

    def button_delete(select_optimizer):
        button = st.button('Удалить')
        if button:
            CRUD.delete_opt(select_optimizer)
            st.sidebar.success(f"Данные были удалены из БД")

    button_delete(select_optimizer)

