import pandas as pd
import sqlalchemy.exc
import streamlit as st

import web.CRUD as CRUD
import func
from web.schemas import DataOptimization
import base64
import io

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
def create_variables():
    st.subheader("Внесение переменных")
    name_model = st.text_input('Введите имя набора')
    options = [
        {
            "name": "tol",
            "value": str(1e-08),
            "descriptions": "Желаемый допуск сходимости (относительный)",
            "isActive": True
        },
        {
            "name": "max_iter",
            "value": str(3000),
            "descriptions": "Максимальное количество итераций",
            "isActive": True
        },
        {
            "name": "max_wall_time",
            "value": str(100000000000000000000),
            "descriptions": "Максимальное время для решения",
            "isActive": True
        },
        {
            "name": "dual_inf_tol",
            "value": str(1),
            "descriptions": "Абсолютная терпимость к двойной неосуществимости",
            "isActive": True
        },
        {
            "name": "constr_viol_tol",
            "value": str(0.0001),
            "descriptions": "Желаемый порог для нарушения ограничения",
            "isActive": True
        },
        {
            "name": "acceptable_tol",
            "value": str(1e-06),
            "descriptions": "Приемлемый допуск сходимости",
            "isActive": True
        },
        {
            "name": "acceptable_iter",
            "value": str(15),
            "descriptions": "Количество приемлемых итераций перед завершением",
            "isActive": True
        },
        {
            "name": "acceptable_dual_inf_tol",
            "value": str(10000000000),
            "descriptions": "Порог приемлемости для двойной неосуществимости",
            "isActive": True
        },
        {
            "name": "acceptable_constr_viol_tol",
            "value": str(0.01),
            "descriptions": "Порог приемлемости при нарушении ограничения",
            "isActive": True
        },
        {
            "name": "acceptable_compl_inf_tol",
            "value": str(0.01),
            "descriptions": "Порог приемлемости для условий взаимодополняемости",
            "isActive": True
        },
        {
            "name": "acceptable_obj_change_tol",
            "value": str(100000000000000000000),
            "descriptions": "Критерий остановки Принятия, основанный на изменении целевой функции",
            "isActive": True
        },
        {
            "name": "diverging_iterates_tol",
            "value": str(100000000000000000000),
            "descriptions": "Порог для максимального значения первичных итераций",
            "isActive": True
        },
        {
            "name": "mu_target",
            "value": str(0),
            "descriptions": "Желаемое значение взаимодополняемости",
            "isActive": True
        },
        {
            "name": "print_level",
            "value": str(5),
            "descriptions": "Уровень логирования",
            "isActive": True
        }
    ]

    def button_load_to_bd(result_JSON):
        # for element in result_JSON:
        #     for key in element:
        #         if element[key] == "None":
        #             st.warning('Вы заполнили не все данные!')
        #             break

        button_txt_create = st.button('Загрузить в БД')

        if button_txt_create:
            form = {'isOpt': [], 'isConstraint': []}
            for value in result_JSON:
                if value['isOpt'] == True:
                    form['isOpt'].append(value['tag'])
                if value['isConstraint'] == True:
                    form['isConstraint'].append(value['tag'])
                form_to_db = []
                for Opt in form['isOpt']:
                    for Constraint in form['isConstraint']:
                        form_to_db.append({'opt': Opt, 'constraint': Constraint, 'coef': 0})
            try:
                result = DataOptimization(name=name_model, variables=str(result_JSON), matrix=str(form_to_db),options = str(options))
                CRUD.create_model(result)
                st.sidebar.success(f"Данные были загружены в БД")
            except sqlalchemy.exc.IntegrityError as e:
                st.sidebar.error(f"Имя набора для оптимизации уже существует")


    uploaded_file = st.file_uploader('Подгрузите свой Excel файл')
    if uploaded_file is not None:
        df_excel = pd.read_excel(uploaded_file)
        df = st.experimental_data_editor(df_excel, num_rows="dynamic", width=1000)
        st.sidebar.info("После подгрузки Excel-файла в БД необходимо будет обновить страницу!")
        a = func.parsing_data(df)
        button_load_to_bd(a)



    else:
        df = pd.DataFrame(
            [

                {"tag": "PI_24-2000", "hl": 4, "ll": 1, "status": True, "weight": 11, "isOpt": True,
                 "isConstraint": False, "value":1}
            ]
        )

        df = st.experimental_data_editor(df, num_rows="dynamic", width=1000)
        buffer = io.BytesIO()
        df.to_excel(buffer, encoding='utf-8', sheet_name='Лист1', index=False, header=True)
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode()
        link = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="pattern_variables.xlsx">Скачать шаблон переменных (Excel-файл)</a>'
        st.sidebar.markdown(link, unsafe_allow_html=True)
        a = func.parsing_data(df)
        button_load_to_bd(a)

