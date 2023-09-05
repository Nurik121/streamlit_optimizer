import streamlit as st
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
from generate_keys import names, usernames
import multipages.create_variables as create_var
import multipages.change_variables as change_var
import multipages.delete_variables as delete_var
import multipages.change_the_matrix as change_matrix
import multipages.target_function as target_func
import multipages.optimization as opt
import multipages.create_opt as create_opt
import multipages.delete_opt as delete_opt
import multipages.options as create_options
from PIL import Image

image = Image.open('icon.jpg')

st.image(image)

create_var = create_var.create_variables
change_var = change_var.change_variables
delete_var = delete_var.delete_variables
change_matrix = change_matrix.change_the_matrix
target_func = target_func.target_func
opt = opt.opt
create_opt = create_opt.create_opt
delete_opt = delete_opt.delete_opt
create_options = create_options.create_options

page_names_to_user = {
    "Создание переменных": create_var,
    "Изменение переменных": change_var,
    "Удаление переменных": delete_var,
    "Изменение матрицы": change_matrix,
    "Целевая функция": target_func,
    "Добавление настроек оптимизации": create_options,
    "Оптимизация": opt,
}

page_names_to_admin = {
    "Создание переменных": create_var,
    "Изменение переменных": change_var,
    "Удаление переменных": delete_var,
    "Изменение матрицы": change_matrix,
    "Целевая функция": target_func,
    "Добавление настроек оптимизации": create_options,
    "Оптимизация": opt,
    "Создание оптимизации": create_opt,
    "Удаление оптимизации": delete_opt,
}


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'cookie_optimizer',
                                    'keyfromcookieab', cookie_expiry_days=10)

name, authentication_status, username = authenticator.login('Вход', 'main')


if authentication_status:
    if username == 'rto_user':
        selected_page = st.sidebar.selectbox("Выбрать страницу", page_names_to_user.keys())
        page_names_to_user[selected_page]()
    elif username == 'admin':
        selected_page = st.sidebar.selectbox("Выбрать страницу", page_names_to_admin.keys())
        page_names_to_admin[selected_page]()
    authenticator.logout('Выйти из системы', 'sidebar')

elif authentication_status == False:
    st.warning('Username/password были некорректно введены')
elif authentication_status == None:
    st.warning('Пожалуйста, введите Username и Password для входа в систему')

