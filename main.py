import streamlit as st
from user import UserApp
from admin import AdminApp
from FirstPage import reg_and_auto
from back_end import url
import requests


def main():
    st.title("Система управления доступом")

    menu_options = ["Пользователь", "Администратор"]
    selected_menu_option = st.sidebar.selectbox("Выбор уровня доступа", menu_options)

    if selected_menu_option == "Пользователь":
        user = UserApp()
    elif selected_menu_option == "Администратор":
        admin = AdminApp()

if __name__ == "__main__":
    main()