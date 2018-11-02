import requests as rq
import pandas as pd
from app import config
import sys
import json


URL = config.URL


def authorisation():
    flag = False
    global cookie
    while flag is False:
        login = input("Введите логин:")
        password = input("Введите пароль:")
        payload = {'login':login, 'password':password}
        post = rq.post(URL + '/login', json=payload)
        message = post.json()
        print(message["message"])
        if post.status_code is 200:
            flag = True
            cookie = post.cookies
        else:
            print("Попробуйте еще раз.")
    return True


def register():
    flag = False
    while flag is False:
        login = input("Введите логин:")
        password = input("Введите пароль:")
        payload = {'login': login, 'password': password}
        post = rq.post(URL + '/register', json=payload)
        message = post.json()
        print(message["message"])
        if post.status_code is 200:
            flag = True
        else:
            print("Попробуйте еще раз.")
    return True


def end():
    rq.get(URL + "/logout")
    print('До свидания!')
    sys.exit()


def my_accounts():
    get = rq.get(URL + "/accounts", cookies=cookie)
    code = get.status_code
    if code == 200:
        print("\n"*50, "Список ваших счетов")
        payload = get.json()
        print(table(payload))
        print("Введите b, чтобы вернуться в Главное меню\nВведите x для выхода")
        action = input("Выберите действие:")
        while action not in ["x", "b"]:
            action = input('Попробуйте еще раз:')
        if action == "x":
            sys.exit()
        elif action == "b":
            menu()

def history():
    get = rq.get(URL + "/history", cookies=cookie)
    payload = get.json()
    print(table(payload))
    print("Введите b, чтобы вернуться в Главное меню\nВведите x для выхода")
    action = input("Выберите действие:")
    while action not in ["x", "b"]:
        action = input('Попробуйте еще раз:')
    if action == "x":
        sys.exit()
    elif action == "b":
        menu()

def table(payload):
    header = []
    for i in range(len(payload)):
        dictionary = payload[i]
        for key in dictionary:
            if key not in header:
                header.append(key)
    print(header)
    table = pd.DataFrame(payload)
    return table


def menu():
    print("\n"*50)
    print("Добро пожаловать в Главное меню.\nВыберите действие:")
    print("1. Мои счета\n2. Операции\n3. История\n4. Выход")
    action = input('Выберите действие:')
    while action not in ["1", "2", "3", "4"]:
        action = input('Попробуйте еще раз:')
    if action == "1":
        my_accounts()
    elif action == "2":
        operations()
    elif action == "3":
        history()
    elif action == "4":
        end()


def entrance():
    print('Добро пожаловать!')
    print('1. Вход\n2. Регистрация\n3. Выход')
    action = input('Выберите действие:')
    while action not in ["1", "2", "3"]:
        action = input('Попробуйте еще раз:')
    if action == "3":
        end()
    elif action == "1":
        if authorisation() is True:
            menu()
    elif action == "2":
        if register() is True:
            print("Выполните вход.")
            if authorisation() is True:
                menu()
