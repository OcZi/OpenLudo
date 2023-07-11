import re

import yaml

database: dict = {}

user: tuple = ()

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
date_regex = re.compile(r'^(0?[1-9]|1[012])[/\-]\d{4}$')


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


def get_wins(email: str):
    return database[email][2]


def get_movements(email: str):
    return database[email][3]


def get_user(email: str):
    return database.get(email)


def create(email: str, name: str, date: str, wins: int, movements: list[int]):
    database[email] = [name, date, wins, movements]


def set_name(email: str, name: str):
    database[email][0] = name


def set_date(email: str, date: str):
    database[email][1] = date


def set_user(email: str, name: str, date: str):
    global user
    user = [email, name, date, 0, []]


def delete(email: str):
    database.pop(email)


def update_user():
    create(user[0], user[1], user[2], user[3], user[4])


def update_user_wins():
    global user
    user[3] += 1


def update_user_moves(moves: list):
    global user
    user[4] = list


def is_valid_email(text):
    return email_regex.fullmatch(text)


def is_valid_date(text):
    return date_regex.fullmatch(text)
