import requests as rq
from app import config
import sys

URL = config.URL


def authorisation():
    login = input("Введите логин:")
    password = input("Введите пароль:")
    payload = {'login':login, 'password':password}
    post = rq.post(str(URL) + '/login', json=payload)
    message = post.json()
    print(message["message"])
    if post.status_code is not 200:
        print("Попробуйте еще раз.")
        authorisation()
    else:
        return True


def register():
    login = input("Введите логин:")
    password = input("Введите пароль:")
    payload = {'login': login, 'password': password}
    post = rq.post(str(URL) + '/register', json=payload)
    return post.status_code

def end():
    print('До свидания!')
    sys.exit()


def entrance():
    print('Добро пожаловать!')
    print('1. Вход\n2. Регистрация\n3. Выход')
    action = input('Выберите действие:')
    while action not in ["1", "2", "3"]:
        action = input('Try again:')
    if action == "3":
        end()
    elif action == "1":
        authorisation()
        if authorisation is True:
            print('Menu"')
    elif action == "2":
        register()
