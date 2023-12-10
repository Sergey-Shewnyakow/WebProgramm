import streamlit as st
import pandas as pd
import requests
import json
from back_end import url

class AdminApp:
    def __init__(self):
        self.passes_data = pd.DataFrame(columns=["ID", "Имя", "E-mail", "Роль"])
        self.check_passes_data = pd.DataFrame(columns=["ID", "Имя", "E-mail"])
        self.histori_passes_data = pd.DataFrame(columns=["ID входа", "Имя", "Дата"])
        admin_name = st.text_input("Введите имя", "")
        admin_password = st.text_input("Введите пароль", "", type="password")
        ente = False
        if len(admin_name)!= 0 and len(admin_password) != 0:
            response_data = requests.get(url +"/user/"+f"?username={admin_name}")
            data = json.loads(response_data.text)
            if len(data) == 3 or data['_roles'] == None:
                st.warning("Данного пользавателя не существует")
            elif "admin" in data['_roles'] and admin_password == data['_password'] :
                st.success("Успешный вход")
                ente = True
            else:
                    st.warning("Данный пользаватель не имеет такой привилегий")
        if ente:
            self.admin_functions()
    def admin_functions(self):
        admin_choice = st.sidebar.selectbox("Выберите функцию",
                                            ["Пропуска ожидают подтверждения", "Все пользователи", "История входов"])

        if admin_choice == "Пропуска ожидают подтверждения":
            self.all_propusk()
            self.view_pending_approvals()
        elif admin_choice == "Все пользователи":
            self.view_all_passes()
        elif admin_choice == "История входов":
            self.histori_pass()

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

    def histori_pass(self):
        st.subheader("История входов")
        self.histori_pass_d()
        st.table(self.histori_passes_data)
    def histori_pass_d(self):
        response_data = requests.get(url + "/entrance")
        data = json.loads(response_data.text)
        for item in data:
            resp = requests.get(url+"/user/"+item["trustees"])
            resp_data = json.loads(resp.text)
            self.histori_passes_data.loc[len(self.histori_passes_data)] = [item["id"], resp_data['username'], item["created_at"]]

    def all_propusk(self):
        response_data = requests.get(url + "/user")
        data = json.loads(response_data.text)
        for item in data:
            if item["roles"] != None:
                self.passes_data.loc[len(self.passes_data)] = [item["id"], item["username"], item["email"],", ".join(item["roles"])]

    def check_propusk(self):
        response_data = requests.get(url+"/user")
        data = json.loads(response_data.text)
        for item in data:
            if item["roles"] == None:
                self.check_passes_data.loc[len(self.check_passes_data)] = [item["id"], item["username"], item["email"]]

if __name__ == "__main__":
    admin = AdminApp()