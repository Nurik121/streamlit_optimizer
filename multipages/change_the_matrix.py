import ast

import pandas as pd
import streamlit as st
import base64
import io
import web.CRUD as CRUD
import func
from web.schemas import DataOptimization

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def change_the_matrix():
    st.subheader("Матрица")
    name_from_db = CRUD.get_name()
    select_name = st.selectbox("Выберите имя набора для изменения", func.get_name(name_from_db))
    uploaded_file = st.file_uploader('Подгрузите свой Excel файл')
    JSON_from_DB = CRUD.get_variables(select_name)
    JSON_from_DB = ast.literal_eval(JSON_from_DB)


    def button_update_to_db(matrix, name, JSON_from_DB):
        button = st.button('Обновить в БД')
        matrix = matrix.fillna('0')
        # for element in JSON_from_DB:
        #     for key in element:
        #         if element[key] == "None":
        #             st.warning('Вы заполнили не все данные!')
        #             break
        if button:

            form_to_db = []
            form = matrix.to_dict('index')

            for Opt in form:
                for Constraint in form[Opt]:
                    # coef = str(form[Opt][Constraint])
                    form_to_db.append({'opt': Opt, 'constraint': Constraint, 'coef': form[Opt][Constraint]})
            result = DataOptimization(name=name, variables=str(JSON_from_DB), matrix=str(form_to_db))
            CRUD.update_data(result)
            st.sidebar.success(f"Данные были обновлены")


    if uploaded_file is not None:
        df_excel = pd.read_excel(uploaded_file)
        df_excel = df_excel.fillna(0)
        headings = df_excel.columns.ravel()
        list_indexes = df_excel['Tags'].tolist()
        list_head = headings.tolist()
        list_head.pop(0)
        form = df_excel.to_dict('dict')
        form.pop('Tags')
        df_excel = pd.DataFrame(columns=list_head, index=list_indexes)

        for index in range(0, len(list_indexes)):
            for x in form:
                df_excel.loc[list_indexes[index], x] = form[x][index]

        df = st.experimental_data_editor(df_excel, width=1000)
        st.sidebar.info("После подгрузки Excel-файла в БД необходимо будет обновить страницу!")
        button_update_to_db(df, select_name, JSON_from_DB)

    else:
        matrix = CRUD.get_matrix(select_name)
        form_list = ast.literal_eval(matrix)

        form = {'isOpt': [], 'isConstraint': []}
        for value in JSON_from_DB:
            if value['isOpt'] == True:
                form['isOpt'].append(value['tag'])
            if value['isConstraint'] == True:
                form['isConstraint'].append(value['tag'])

        df_matrix = pd.DataFrame(columns=form['isConstraint'], index=form['isOpt'])
        for cell in form_list:
            df_matrix.loc[cell['opt'], cell['constraint']] = cell['coef']

        # buffer = io.BytesIO()
        # df_matrix.to_excel(buffer, encoding='utf-8', sheet_name='Лист1', index=False, header=True)
        # buffer.seek(0)
        # b64 = base64.b64encode(buffer.read()).decode()

        excel_data = pd.read_excel('matrix.xlsx')
        data = pd.DataFrame(excel_data)
        buffer = io.BytesIO()
        data.to_excel(buffer, encoding='utf-8', sheet_name='Лист1', index=False, header=True)
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode()
        link = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="pattern_matrix.xlsx">Скачать шаблон матрицы (Excel-файл)</a>'
        st.sidebar.markdown(link, unsafe_allow_html=True)

        df_to_db = st.experimental_data_editor(df_matrix, width=1000)
        button_update_to_db(df_to_db, select_name, JSON_from_DB)
