import re

import yaml

database: dict = {}

user: tuple = ()

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
date_regex = re.compile(r'^\d((0[1-9]|1[0-2])/{4})$')


def load():
    global database
    with open("database.yaml") as file:
        database = yaml.load(file, Loader=yaml.Loader)


def save():
    global database
    with open("database.yaml", "w") as file:
        database = yaml.dump(database, file)


def get_name(email: str):
    return database[email][0]


def get_date(email: str):
    return database[email][1]


def set(email: str, name: str, date: str):
    database[email] = [name, date]


def set_name(email: str, name: str):
    database[email][0] = name


def set_date(email: str, date: str):
    database[email][1] = date


def set_user(email: str, name: str, date: str):
    global user
    user = (email, name, date)


def delete(email: str):
    database.pop(email)


def update_user():
    set(user[0], user[1], user[2])


def is_valid_email(text):
    return email_regex.fullmatch(text)


def is_valid_date(text):
    return date_regex.fullmatch(text)

