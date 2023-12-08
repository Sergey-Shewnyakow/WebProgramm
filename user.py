import streamlit as st
from back_end import backend_url
class UserApp:
    def __init__(self):
        st.title("Система управления пропусками")
        self.user_functions()

    def user_functions(self):
        user_choice = st.radio("Выберите функцию", ["Открыть точку доступа", "Запросить пропуск"])

        if user_choice == "Открыть точку доступа":
            self.open_gate()
        elif user_choice == "Запросить пропуск":
            self.request_pass()

    def open_gate(self):
        st.subheader("Открытие точки доступа")
        st.write("Точка доступа открыта. Добро пожаловать!")

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
                    st.success("Ваш запрос отправлен. Ожидайте подтверждения.")
            else:
                st.warning("Пожалуйста, введите все необходимые данные перед запросом.")
        else:
            st.warning("Пожалуйста, введите ФИО в правильном формате (Фамилия Имя Отчество).")

if __name__ == "__main__":
    user= UserApp()