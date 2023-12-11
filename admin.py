import streamlit as st
import pandas as pd
import requests
import json
from back_end import url

class AdminApp:
    def __init__(self):
        self.pass_data = pd.DataFrame(columns=["ID", "Имя", "Место"])
        self.all_pass_data = pd.DataFrame(columns=["ID", "Владелец", "Доступ к", "Дата создания"])
        self.passes_data = pd.DataFrame(columns=["ID", "Имя", "E-mail", "Роль"])
        self.check_passes_data = pd.DataFrame(columns=["ID", "Имя", "E-mail"])
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
                                            ["Пользователи ожидают подтверждения",
                                             "Все пользователи", "Пропуски ожидают подтверждения",
                                             "Все пропуски"])

        if admin_choice == "Пользователи ожидают подтверждения":
            self.all_propusk()
            self.view_pending_approvals()
        elif admin_choice == "Все пользователи":
            self.view_all_user()
        elif admin_choice == "Пропуски ожидают подтверждения":
            self.passes()
        elif admin_choice == "Все пропуски":
            self.view_all_passes()
    def view_pending_approvals(self):
        st.subheader("Пользователи ожидают подтверждения")


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

    def view_all_user(self):
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
        for item in json.loads(requests.get(url+"/pass").text):
            if item['requester_id'] == pass_id:
                requests.delete(url + "/pass/" + f"{item['id']}")
        requests.delete(url + "/user/" + f"{pass_id}")
        self.all_propusk()
        st.experimental_rerun()

    def passes(self):
        st.subheader("Пропуски ожидают подтверждения")

        self.check_passes()
        st.table(self.pass_data)

        pass_id = st.text_input("Введите ID для подтверждения:")
        accept_button = st.button("Подтвердить")
        if accept_button:
            self.accept_paass(pass_id)



    def check_passes(self):
        response_data = requests.get(url + "/pass")
        data = json.loads(response_data.text)
        for item in data:
            if item["status"] == None:
                self.pass_data.loc[len(self.pass_data)] = [item["id"],
                                                           json.loads((requests.get(
                                                               url + "/user/" + f"{item['requester_id']}")).text)['username'],
                                                           ",".join(str(entry) for entry in ( [json.loads(
                                                               requests.get(url + f"/entrance/{entrance_id}").text)['name']
                                                                                               for entrance_id in item['entrances']]))]

    def accept_paass(self, pass_id):
        requests.put(url + "/pass/" + pass_id +"/confirm")
        self.check_passes()
        st.experimental_rerun()


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


    def view_all_passes(self):
        st.subheader("Все пропуски")
        self.all_passes()

        st.table(self.all_pass_data)
    def all_passes(self):
        data = json.loads(requests.get(url+"/pass").text)
        for item in data:
            if item["status"] != None:
                self.all_pass_data.loc[len(self.all_pass_data)] = \
                    [item["id"], json.loads((requests.get(
                    url + "/user/" + f"{item['requester_id']}")).text)['username']
                    , ",".join(str(entry) for entry in ( [json.loads(
                    requests.get(url + f"/entrance/{entrance_id}").text)['name']
                    for entrance_id in item['entrances']])), item['created_at']]



if __name__ == "__main__":
    admin = AdminApp()