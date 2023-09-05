import ast

import pandas as pd
import streamlit as st

import func
import web.CRUD as CRUD
from web.schemas import DataOptimization

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def change_variables():
    st.subheader("Изменение переменных")
    name_from_db = CRUD.get_name()
    select_name = st.selectbox("Выберите имя набора для изменения", func.get_name(name_from_db))


    def button_update_to_db(result_JSON, select_name):
        button = st.button('Обновить в БД')

        if button:

            matrix = CRUD.get_matrix(select_name)
            old_matrix = ast.literal_eval(matrix)

            form = {'isOpt': [], 'isConstraint': []}
            for value in result_JSON:
                if value['isOpt'] == True:
                    form['isOpt'].append(value['tag'])
                if value['isConstraint'] == True:
                    form['isConstraint'].append(value['tag'])

            new_matrix = []
            for Opt in form['isOpt']:
                for Constraint in form['isConstraint']:
                    new_matrix.append({'opt': Opt, 'constraint': Constraint, 'coef': 0})
            from functools import partial
            import itertools
            from operator import is_not
            element_new = []
            element_old = []
            for combination in itertools.zip_longest(new_matrix, old_matrix):
                element_new.append(combination[0])
                element_old.append(combination[1])

            element_new = list(filter(partial(is_not, None), element_new))
            element_old = list(filter(partial(is_not, None), element_old))

            Opt_new = []
            Const_new = []
            for elem in element_new:
                Opt_new.append(elem['opt'])
                Const_new.append(elem['constraint'])

            Opt_old = []
            Const_old = []
            for elem in element_old:
                Opt_old.append(elem['opt'])
                Const_old.append(elem['constraint'])

            Opt_new = set(Opt_new)
            Opt_old = set(Opt_old)

            Const_new = set(Const_new)
            Const_old = set(Const_old)

            del_Opt = Opt_old.difference(Opt_new)
            del_Const = Const_old.difference(Const_new)

            df_matrix = pd.DataFrame(columns=form['isConstraint'], index=form['isOpt'])
            for cell in old_matrix:
                df_matrix.loc[cell['opt'], cell['constraint']] = cell['coef']

            df_matrix = df_matrix.drop(del_Opt)
            df_matrix = df_matrix.drop(del_Const, axis=1)
            df_matrix = df_matrix.fillna('0')
            form_to_db = []
            form_index = df_matrix.to_dict('index')

            for Opt in form_index:
                for Constraint in form_index[Opt]:
                    form_to_db.append({'opt': Opt, 'constraint': Constraint, 'coef': int(form_index[Opt][Constraint])})

            result = DataOptimization(name=select_name, variables=str(result_JSON), matrix=str(form_to_db))
            CRUD.update_data(result)
            st.sidebar.success(f"Данные были обновлены")


    uploaded_file = st.file_uploader('Подгрузите свой Excel файл')
    if uploaded_file is not None:
        df_excel = pd.read_excel(uploaded_file)
        df = st.experimental_data_editor(df_excel, num_rows="dynamic", width=1000)
        st.sidebar.info("После подгрузки Excel-файла в БД необходимо будет обновить страницу!")
        button_update_to_db(func.parsing_data(df), select_name)

    else:
        variables = CRUD.get_variables(select_name)
        variables = ast.literal_eval(variables)
        df = pd.DataFrame(variables)
        table_df = st.experimental_data_editor(df, num_rows="dynamic", width=1000)
        button_update_to_db(func.parsing_data(table_df), select_name)
