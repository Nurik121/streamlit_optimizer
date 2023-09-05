import ast
import io

import streamlit as st
import json
import web.CRUD as CRUD
from func import get_name
import requests
import pandas as pd
import web.settings as settings
import base64
from datetime import datetime


def opt():
    st.subheader("Оптимизатор")

    def color_boolean(val):
        color = 'white'
        if val == 'False':
            color = 'red'
        return 'background-color: %s' % color

    def parse_opt_out(dict_opt_data):
        df_dict_opt = {"tag":list(),
        "value":list(),
        "opt_value":list(),
        "hl":list(),
        "ll":list(),
        "isLimit":list(),
        }
        df_dict_con = {"tag":list(),
        "value":list(),
        "opt_value":list(),
        "hl":list(),
        "ll":list(),
        "isLimit":list(),
        }
        for i in dict_opt_data:
            if i['isOpt'] == True:
                df_dict_opt["tag"].append(i['tag'])
                df_dict_opt["value"].append(i['value'])
                df_dict_opt["opt_value"].append(i['opt_value'])
                df_dict_opt["hl"].append(i['hl'])
                df_dict_opt["ll"].append(i['ll'])
                if i['ll'] >= 0 and i['hl'] >= 0:
                    if i['opt_value']>=i['ll'] * 0.98 and i['opt_value']<=i['hl'] * 1.02:
                        df_dict_opt["isLimit"].append('True')
                    else:
                        df_dict_opt["isLimit"].append('False')
                elif i['ll'] < 0 and i['hl'] >= 0:
                    if i['opt_value'] >= i['ll'] * 1.02 and i['opt_value'] <= i['hl'] * 1.02:
                        df_dict_opt["isLimit"].append('True')
                    else:
                        df_dict_opt["isLimit"].append('False')
                elif i['ll'] >= 0 and i['hl'] < 0:
                    if i['opt_value'] >= i['ll'] * 0.98 and i['opt_value'] <= i['hl'] * 0.98:
                        df_dict_opt["isLimit"].append('True')
                    else:
                        df_dict_opt["isLimit"].append('False')
                else:
                    if i['opt_value'] >= i['ll'] * 1.02 and i['opt_value'] <= i['hl'] * 0.98:
                        df_dict_opt["isLimit"].append('True')
                    else:
                        df_dict_opt["isLimit"].append('False')
            elif i['isConstraint'] == True:
                df_dict_con["tag"].append(i['tag'])
                df_dict_con["value"].append(i['value'])
                df_dict_con["opt_value"].append(i['opt_value'])
                df_dict_con["hl"].append(i['hl'])
                df_dict_con["ll"].append(i['ll'])
                if i['ll'] >= 0 and i['hl'] >= 0:
                    if i['opt_value']>=i['ll'] * 0.98 and i['opt_value']<=i['hl'] * 1.02:
                        df_dict_con["isLimit"].append('True')
                    else:
                        df_dict_con["isLimit"].append('False')
                elif i['ll'] < 0 and i['hl'] >= 0:
                    if i['opt_value']>=i['ll'] * 1.02 and i['opt_value']<=i['hl'] * 1.02:
                        df_dict_con["isLimit"].append('True')
                    else:
                        df_dict_con["isLimit"].append('False')
                elif i['ll'] >= 0 and i['hl'] < 0:
                    if i['opt_value']>=i['ll'] * 0.98 and i['opt_value']<=i['hl'] * 0.98:
                        df_dict_con["isLimit"].append('True')
                    else:
                        df_dict_con["isLimit"].append('False')
                else:
                    if i['opt_value']>=i['ll'] * 1.02 and i['opt_value']<=i['hl'] * 0.98:
                        df_dict_con["isLimit"].append('True')
                    else:
                        df_dict_con["isLimit"].append('False')
        return df_dict_opt,df_dict_con

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    name_from_db = CRUD.get_name()
    variable_name = st.selectbox("Выберите имя набора", get_name(name_from_db))
    name_from_db = CRUD.get_optimizer_descript()
    opt_description = st.selectbox("Выберите оптимизацию", get_name(name_from_db))
    but = st.button('Начать расчет')
    if but:
        with st.spinner('Подождите, идёт оптимизация...'):
            start_date = datetime.now()
            data = CRUD.get_optimization(variable_name)
            variables = ast.literal_eval(data.variables)
            matrix = ast.literal_eval(data.matrix)
            options = ast.literal_eval(data.options)
            new_option = list()
            for option in options:
                if option['isActive']:
                    option['value'] = float(option['value'])
                    new_option.append(option)

            print(new_option)
            #matrix_coef_not_zero = []
            #for element in matrix:
                #if element["coef"] != 0:
                    #matrix_coef_not_zero.append(element)
            matrix_coef_not_zero = matrix
            optimizer = CRUD.get_optimizer_by_descript(opt_description).name
            obj = data.obj
            form = {'obj': obj,
                    'variables': variables,
                    'matrix': matrix_coef_not_zero,
                    'optimizer': optimizer,
                    'name': data.name,
                    'options': new_option}

            json_form = json.dumps(form)
            # my_file = open("jsonForm.txt", "w")
            # my_file.write(json_form)
            # my_file.close()
            data_value = requests.post(url=settings.URL_OPTIMIZATION, data=json_form,
                                       headers={'content-type': 'application/json'}).json()
            data_value = json.loads(data_value)

            # print(type(data_value))
            # dict_opt_data = [mod.dict() for mod in data_value[variables]]
            df_dict_opt, df_dict_con = parse_opt_out(data_value["variables"])
            all_seconds = (datetime.now() - start_date).seconds
            minutes = all_seconds // 60
            seconds = all_seconds % 60
            st.metric(f'На оптимизацию было потрачено:', f'{minutes} минут(ы) {seconds} секунд(ы)')

        st.text(f'Статус расчета: {data_value["status"]["text"]}')
        # percent = ((data_value['objOpt'] - data_value['objBase'])*100)/data_value['objBase']
        # percent_rounding = round(percent, 1)
        col1, col2 = st.columns(2)
        col1.metric(f"Целевая функция до оптимизации:", round(data_value['objBase'], 1))
        col2.metric(f"Целевая функция после оптимизации:", round(data_value['objOpt'], 1))
        st.text('Решение по оптимизационным параметрам')
        df1 = pd.DataFrame(df_dict_opt)
        df1_style = pd.DataFrame(df_dict_opt).style.applymap(color_boolean)
        st.dataframe(df1_style, width=1000)
        st.text('Решение по ограничениям')
        df2 = pd.DataFrame(df_dict_con)
        df2_style = pd.DataFrame(df_dict_con).style.applymap(color_boolean)
        st.dataframe(df2_style, width=1000)
        df_merged = df1.append(df2, ignore_index=True).style.applymap(color_boolean)
        buffer = io.BytesIO()
        df_merged.to_excel(buffer, encoding='utf-8', sheet_name='Лист1', index=False, header=True)
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode()
        link = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="output.xlsx">Сохранить оптимизацию в Excel-файл</a>'
        st.markdown(link, unsafe_allow_html=True)
        with open('/home/user/optimizer-webapi/IPOPT.out', 'rb') as f:
            st.download_button('Download outputs', f, file_name='out.txt')
        # with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        #     df_merged.to_excel(writer, sheet_name='Лист1', index=False)
        #     writer.save()
        #     st.download_button(label="Сохранить оптимизацию в Excel", data=buffer, file_name="output.xlsx",
        #                    mime='application/vnd.ms-excel')



        # @st.cache
        # def convert_df(df_merged):
        #     # IMPORTANT: Cache the conversion to prevent computation on every rerun
        #     return df_merged.to_excel().encode('utf-8')
        #
        # excel = convert_df(df_merged)
        #
        # st.download_button(
        #     label="Download data as excel",
        #     data=excel,
        #     file_name='output.xlsx',
        #     mime='text/xlsx',
        # )
