import streamlit as st
import pandas as pd
from back_end import backend_url

class AdminApp:
    def __init__(self):
        self.passes_data = pd.DataFrame(columns=["ID", "Имя", "E-mail", "Статус"])
        st.title("Система управления пропусками")
        admin_password = st.text_input("Введите пароль для доступа к административной панели", "", type="password")

        if admin_password == "1111":
            st.success("Пароль верный. Доступ к административной панели разрешен.")
            self.admin_functions()
        elif admin_password != "":
            st.warning("Неверный пароль. Попробуйте снова.")

    def admin_functions(self):
        admin_choice = st.sidebar.selectbox("Выберите функцию",
                                            ["Пропуска ожидают подтверждения", "Все пропуски", "Добавить пропуск"])

        if admin_choice == "Пропуска ожидают подтверждения":
            self.load_test_data()
            self.view_pending_approvals()
        elif admin_choice == "Все пропуски":
            self.view_all_passes()
        elif admin_choice == "Добавить пропуск":
            self.add_pass()

    def view_pending_approvals(self):
        st.subheader("Пропуска ожидают подтверждения")

        if self.passes_data.empty or "Статус" not in self.passes_data.columns:
            st.info("Нет пропусков, ожидающих подтверждения.")
            return

        pending_approvals = self.passes_data[self.passes_data["Статус"] == "Ожидает подтверждения"]

        selected_pass = st.selectbox("Выберите пропуск для проверки", pending_approvals["ID"].tolist())

        if st.button("Показать выбранный пропуск"):
            self.show_selected_pass(selected_pass)

        st.table(pending_approvals[["ID", "Имя", "E-mail"]])

    def show_selected_pass(self, pass_id):
        st.subheader(f"Информация по пропуску ID {pass_id}")

        selected_pass_info = self.passes_data.loc[self.passes_data["ID"] == pass_id]
        st.table(selected_pass_info[["ID", "Имя", "E-mail", "Статус"]])

        action = st.radio("Выберите действие", ["Подтвердить", "Отклонить", "Редактировать"])

        if st.button(f"{action} пропуск", key=f"manage_pass_{pass_id}"):
            if action == "Подтвердить":
                self.confirm_pass(pass_id)
            elif action == "Отклонить":
                self.reject_pass(pass_id)
            elif action == "Редактировать":
                self.edit_pass(pass_id)

    def view_all_passes(self):
        st.subheader("Все пропуски")

        if self.passes_data.empty:
            st.info("Нет зарегистрированных пропусков.")
            return

        st.table(self.passes_data[["ID", "Имя", "E-mail", "Статус"]])

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

    def load_test_data(self):
        self.passes_data.loc[len(self.passes_data)] = [1, "Тестовый Пользователь", "Тестовый E-mail",
                                                       "Ожидает подтверждения"]


if __name__ == "__main__":
    admin = AdminApp()