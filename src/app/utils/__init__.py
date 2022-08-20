import locale
import random
import re

import bcrypt
from flask import current_app
from jwt import encode


def is_table_empty(query):
    if query == None:
        return True
    else:
        return False

# verificar se todas as chaves obrigatorias estão sendo enviadas
def exist_key(request_json,list_keys):
    keys_missing = []

    for key in list_keys:
        if key in request_json:
            continue
        else:
            keys_missing.append(key)
    if len(keys_missing) == 0:
        return request_json
    
    return {"error": f"Está faltando o item {keys_missing}"}

def generate_jwt(payload):
    token = encode(payload, current_app.config["SECRET_KEY"], "HS256")

    return token

def random_or_none():
    factor = random.randint(0 , 10)
    mod = factor % 2
    if mod == 0:
        return None
    elif mod == 1:
        return random.randint(1 , 4)


def encrypt_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

def check_password(password: str, senha: str):
    return bcrypt.checkpw(password.encode("utf-8"), senha.encode("utf-8"))

def format_currency(value):
    locale.setlocale( locale.LC_ALL, 'pt_BR.UTF-8' )
    value = locale.currency(value, grouping=True)
    return value

def check_email_validate(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    else:
        return False
