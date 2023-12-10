import requests
import streamlit as st
from back_end import user_url
import json
class UserApp:
    def __init__(self):
        st.title("Система управления пропусками")
        self.user_functions()

    def user_functions(self):
        user_choice = st.radio("Выберите функцию", ["Открыть точку доступа", "Запросить пропуск","Мои пропуска"])

        if user_choice == "Открыть точку доступа":
            self.open_gate()
        elif user_choice == "Запросить пропуск":
            self.request_pass()
        elif user_choice == "Мои пропуска":
            self.my_pass()

    def open_gate(self):
        if st.button("Открыть точку доступа"):
            st.subheader("Открытие точки доступа")
            st.write("Точка доступа открыта")

    def request_pass(self):
        st.subheader("Запрос пропуска")
        full_name = st.text_input("Введите ФИО (Фамилия Имя Отчество)", "")
        password = st.text_input("Введите пароль", "")
        e_mail = st.text_input("Введите e-mail", "")

        if full_name and len(full_name.split()) == 3:
            last_name, first_name, middle_name = full_name.split()
            st.write("Пропуск запрошен")
            st.write(f"Фамилия: {last_name}")
            st.write(f"Имя: {first_name}")
            st.write(f"Отчество: {middle_name}")
            st.write(f"E-mail: {e_mail}")

            if last_name and first_name and middle_name and e_mail:
                if st.button("Запросить", key="request_button"):
                    response_data = requests.get(user_url)
                    data = json.loads(response_data.text)
                    last_move = True
                    for item in data:
                        if item["username"] == full_name and item["email"] == e_mail or item["email"] == e_mail:
                            st.warning("Такой пользователь уже имеет пропуск")
                            last_move = False
                    if last_move:
                        st.success("Ваш запрос отправлен. Ожидайте подтверждения.")
                        nw_user_data ={
                             "username": f"{full_name}",
                             "password":f"{password}",
                             "email": f"{e_mail}",
                             "roles": None,
                         }
                        requests.post(user_url, json = nw_user_data )
                    else:
                        st.warning("Пожалуйста, введите другие данные.")
            else:
                st.warning("Пожалуйста, введите все необходимые данные перед запросом.")
        else:
            st.warning("Пожалуйста, введите ФИО в правильном формате (Фамилия Имя Отчество).")
    def my_pass(self):
        st.subheader("Мои пропуска")
        full_name = st.text_input("Введите ФИО (Фамилия Имя Отчество)", "")
        password = st.text_input("Введите пароль", "")
        if full_name and password:
            if st.button("Посмотретsь", key="request_button"):
                response_data = requests.get(user_url)
                data = json.loads(response_data.text)
                last_move = True
                for item in data:
                    if item["username"] == full_name and item["password"] == password:
                        st.success(item["id"])
        else:
            st.warning("Пожалуйста, введите все необходимые данные перед запросом.")

if __name__ == "__main__":
    user = UserApp()