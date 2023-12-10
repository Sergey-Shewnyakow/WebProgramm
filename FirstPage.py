import streamlit as st

def avtoreg():
    st.title("Авторизация")

    username = st.text_input("Имя")
    password = st.text_input("Пароль", type="password")


    if st.button("Войти"):
        if username == "ваш_логин" and password == "ваш_пароль":
            st.success("Успешная авторизация!")
            # Здесь вы можете добавить код для перехода к другим разделам приложения
        else:
            st.error("Неверные логин или пароль")

def registration():
    st.title("Регистрация")


    name = st.text_input("Имя")
    email = st.text_input("Электронная почта")
    password = st.text_input("Пароль", type="password")

    confirm_password = st.text_input("Повторите пароль", type="password")


    if password != confirm_password:
        st.error("Пароль и его подтверждение не совпадают")

    # Кнопка для отправки данных
    if st.button("Зарегистрироваться"):

        st.success(f"Регистрация успешна! Добро пожаловать, {name}!")

def reg_and_auto():
    st.title("Система контроля доступом")

    choice = st.radio("Выберите действие", ["Авторизация", "Регистрация"])

    if choice == "Авторизация":
        avtoreg()

    elif choice == "Регистрация":
        registration()



