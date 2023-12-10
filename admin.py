import streamlit as st
import pandas as pd
import requests
import json
from back_end import url

class AdminApp:
    def __init__(self):
        self.passes_data = pd.DataFrame(columns=["ID", "Имя", "E-mail"])
        self.check_passes_data = pd.DataFrame(columns=["ID", "Имя", "E-mail"])
        admin_password = st.text_input("Введите пароль для доступа к административной панели", "", type="password")

        if admin_password == "1111":
            st.success("Пароль верный. Доступ к административной панели разрешен.")
            self.admin_functions()
        elif admin_password != "":
            st.warning("Неверный пароль. Попробуйте снова.")

    def admin_functions(self):
        admin_choice = st.sidebar.selectbox("Выберите функцию",
                                            ["Пропуска ожидают подтверждения", "Все пользователи", "Добавить пропуск"])

        if admin_choice == "Пропуска ожидают подтверждения":
            self.all_propusk()
            self.view_pending_approvals()
        elif admin_choice == "Все пользователи":
            self.view_all_passes()
        elif admin_choice == "Добавить пропуск":
            self.add_pass()

    def view_pending_approvals(self):
        st.subheader("Пропуска ожидают подтверждения")


        self.check_propusk()
        st.table(self.check_passes_data)
        st.subheader("Подтверждение по ID")
        user_id = st.text_input("Введите ID для подтверждения:")
        accept_button = st.button("Подтвердить")
        if accept_button:
            self.accept_user(user_id)

    def accept_user(self, user_id):
        data = {
            "id": f"{user_id}",
            "roles": ["user"]
        }
        requests.put(url + "/user/role", json=data)
        self.check_propusk()
        st.experimental_rerun()

    def view_all_passes(self):
        st.subheader("Все пользователи")
        self.all_propusk()

        st.table(self.passes_data)

        if self.passes_data.empty:
            st.info("Нет зарегистрированных пропусков.")
            return
        st.subheader("Удаление пользователя по ID")
        user_id_to_delete = st.text_input("Введите ID для удаления:")
        delete_button = st.button("Удалить пользователя")
        if delete_button:
            self.delete_pass_by_id(user_id_to_delete)

    def delete_pass_by_id(self, pass_id):
        requests.delete(url + "/user/" + f"{pass_id}")
        self.all_propusk()
        st.experimental_rerun()

    def add_pass(self):
        st.subheader("Добавление пропуска")

        full_name = st.text_input("Введите ФИО (Фамилия Имя Отчество)", "")
        email = st.text_input("Введите e-mail", "")

        if st.button("Добавить пропуск", key="add_pass"):
            if not full_name or not email:
                st.warning("Пожалуйста, введите ФИО и E-mail перед добавлением пропуска.")
                return

            name_parts = full_name.split()
            if len(name_parts) != 3:
                st.warning("Пожалуйста, введите полное ФИО (Фамилия Имя Отчество).")
                return

            pass_id = len(self.passes_data) + 1
            self.passes_data.loc[len(self.passes_data)] = [pass_id, full_name, email, "Ожидает подтверждения"]
            st.success(f"Пропуск для {full_name} добавлен с ID {pass_id} и ожидает подтверждения.")

    def all_propusk(self):
        response_data = requests.get(url + "/user")
        data = json.loads(response_data.text)
        for item in data:
            if item["roles"] != None:
                self.passes_data.loc[len(self.passes_data)] = [item["id"], item["username"], item["email"]]

    def check_propusk(self):
        response_data = requests.get(url+"/user")
        data = json.loads(response_data.text)
        for item in data:
            if item["roles"] == None:
                self.check_passes_data.loc[len(self.check_passes_data)] = [item["id"], item["username"], item["email"]]

if __name__ == "__main__":
    admin = AdminApp()