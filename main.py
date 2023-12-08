import streamlit as st
from user import UserApp
from admin import AdminApp
from back_end import backend_url
import requests



response = requests.get(f"{backend_url}/entrance")

def main():
    st.title("Система управления пропусками")

    menu_options = ["Пользователь", "Администратор"]
    selected_menu_option = st.sidebar.selectbox("Выбор уровня доступа", menu_options)

    if selected_menu_option == "Пользователь":
        user = UserApp()
    elif selected_menu_option == "Администратор":
        admin = AdminApp()

if __name__ == "__main__":
    main()