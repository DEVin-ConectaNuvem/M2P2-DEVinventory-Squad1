from flask import current_app
from jwt import encode
import random
import bcrypt
from datetime import datetime
from random import randint
from faker.providers.address.pt_BR import Provider



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

def gen_age(min_year=1915, max_year=2005):
    # gera um datetime no formato yyyy-mm-dd hh:mm:ss.000000
    year = random.randint(min_year, max_year)
    month = random.randint(11, 12)
    day = random.randint(1, 28)
    date = datetime(year, month, day)
    return date

def gen_number_street():
    return randint(1, 1000)

def gen_landmark():
    landmark = ["Perto da farmácia", "Atrás do posto de gasolina", "Lado de agropecuaria", "Na frente do mar", "No fim da rua", "No inicio da rua", "perto da mercearia do Maneca", "No subsolo", "Acima da verdureira", "Atrás do mercadinho", "atrás da dona Gertrudes", "Na frente da igreja", "Do lado do bar", "Atrás da oficina Simas Turbo"]

    return landmark[randint(0, len(landmark) - 1)]

def gen_complement():
    complem = ["Apto01", "Apto02", "Casa dos fundos", "Bloco C Ap 201", "Bloco A 101", "Casa amarela", "Casa do portão verde", "Casa do cachorro bravo", "Prédio do Biriba"]

    return complem[randint(0, len(complem) -1)]

def gen_bairro():
    bairro = Provider.bairros
    return bairro[randint(0, len(bairro) - 1)]
