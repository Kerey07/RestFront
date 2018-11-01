import requests as rq
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
    rq.get(URL + "logout")
    print('До свидания!')
    sys.exit()


def my_accounts():
    get = rq.get(URL + "/accounts", cookies=cookie)
    code = get.status_code
    if code == 200:
        # print("\n"*50, "Список ваших счетов")
        payload = get.json()
        print(json.dumps(payload, indent=4))


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
    else:
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
