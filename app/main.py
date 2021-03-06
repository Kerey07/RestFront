import sys

import pandas as pd
import requests as rq

from app import config

URL = config.URL


def authorisation():
    flag = False
    global cookie
    while flag is False:
        login = input("Введите логин:")
        password = input("Введите пароль:")
        payload = {'login': login, 'password': password}
        post = rq.post(URL + '/login', json=payload)
        message = post.json()
        print(message["message"])
        if post.status_code is 200:
            flag = True
            cookie = post.cookies
        else:
            print("Попробуйте еще раз.")
    return True


def ender():
    action = input("Выберите действие:")
    while action not in ["x", "b"]:
        action = input('Попробуйте еще раз:')
    if action == "x":
        sys.exit()
    elif action == "b":
        menu()


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
    payload = get.json()
    if code == 200:
        print("\n" * 50, "Список ваших счетов")
        print(table(payload, 'accounts'))
        print("Введите b, чтобы вернуться в Главное меню\nВведите x для выхода")
        ender()
    else:
        print(payload["message"])
        ender()


def history():
    get = rq.get(URL + "/history", cookies=cookie)
    payload = get.json()
    print("\n" * 50, "История ваших операций")
    print(table(payload, 'history'))
    print("Введите b, чтобы вернуться в Главное меню\nВведите x для выхода")
    ender()


def operation_rq(**payload):
    post = rq.post(URL+'/operations', cookies=cookie, json=payload)
    message = post.json()
    print(message["message"])
    print("Введите b, чтобы вернуться в Главное меню\nВведите x для выхода")
    ender()


def operations():
    print("\n" * 50)
    print(
        "Выберите тип операции:\n1. Внесение средств.\n2. Снятие средств.\n3. Перевод средств.\n4. Создание нового счета")
    print("\nВведите b, чтобы вернуться в Главное меню.\nВведите x для выхода.")
    action = input("Выберите действие:")
    while action not in ["x", "b", "1", "2", "3", "4"]:
        action = input('Попробуйте еще раз:')
    if action == "x":
        sys.exit()
    elif action == "b":
        menu()
    elif action == "1":
        operation_type = "PURCHASE"
        user_account = input("Введите номер своего счета:")
        value = input("Введите сумму:")
        operation_rq(user_account=user_account, operation_type=operation_type, value=value)
    elif action == "2":
        user_account = input("Введите номер своего счета:")
        operation_type = "WITHDRAWAL"
        value = input("Введите сумму:")
        operation_rq(user_account=user_account, operation_type=operation_type, value=value)
    elif action == "3":
        operation_type = "TRANSFER"
        user_account = input("Введите номер своего счета:")
        recipient = input("Введите счет получателя:")
        value = input("Введите сумму:")
        operation_rq(user_account=user_account, recipient_account=recipient, operation_type=operation_type, value=value)
    elif action == "4":
        operation_type = "CREATE"
        value = input("Введите сумму:")
        operation_rq(operation_type=operation_type, value=value)


def table(payload, type):
    df = pd.DataFrame(payload)
    pd.set_option('display.width', None)
    pd.set_option('display.max_rows', None)
    df = df.fillna('')
    if type == 'history':
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df = df[['account', 'recipient', 'type', 'value', 'timestamp']]
        df.columns = ['Номер счета', 'Счет-получатель', 'Тип операции', 'Сумма операции', 'Время']
        return df
    else:
        df.columns = ['Номер счета', 'Балланс']
        return df


def menu():
    print("\n" * 50)
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
