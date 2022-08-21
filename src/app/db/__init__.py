from json import loads
from random import randint

import requests
from sqlalchemy.sql.expression import func

from src.app.models.city import City, cities_share_schema
from src.app.models.country import Country, country_share_schema
from src.app.models.gender import Gender, genders_share_schema
from src.app.models.inventory import Inventory, inventories_share_schema
from src.app.models.permission import Permission, permissions_share_schema
from src.app.models.product_categories import (Product_Categories,
                                               product_categories_share_schema)
from src.app.models.role import Role, roles_share_schema
from src.app.models.state import State, states_share_schema
from src.app.models.user import User, users_share_schema
from src.app.utils import is_table_empty, random_or_none

inventory = [
    {""}
    ]
users = [
    {"city_id": 1566, "gender_id" : 1, "role_id" : 1 , "name" : "João Victor", 
    "age" : "1996-04-08" , "email" : 'joao@email.com',"phone" : '48999999999', "password" : "Abcd@123",
    "cep" : 80130780, "street" : "Almeida street", "district" : "Capoeiras", "complement" : None,
    "landmark" : None, "number_street" : 210},

    {"city_id": 2600, "gender_id" : 2, "role_id" : 2,  "name" : "Ana Luiza",
    "age" : "1998-05-12" , "email" : 'ana@email.com', "phone" : '48998889866', "password" : "Xyzw#123",
    "cep" : 881150989, "street" : "Borges street", "district" : "Centro", "complement" : None,
    "landmark" : None, "number_street" : 150},

    {"city_id": 2000, "gender_id" : 3, "role_id" : 3,  "name" : "Pablo Willow",
    "age" : "1990-08-15" , "email" : 'pablo@email.com', "phone" : '48988887777', "password" : "Dev&0001",
    "cep" : 88110210, "street" : "Gama street", "district" : "Ingleses", "complement" : None,
    "landmark" : None, "number_street" : 999},

    {"city_id": 3000, "gender_id" : 4, "role_id" : 4,  "name" : "Juca Flint",
    "age" : "2000-10-01" , "email" : 'juca@email.com', "phone" : '48977771234', "password" : "Toor&456",
    "cep" : 88050558, "street" : "Delta street", "district" : "Areias", "complement" : None,
    "landmark" : None, "number_street" : 1052}
]
roles = [
    {"name" : "Administrador do Sistema", "description" : "SYSTEM_ADMIN"},
    {"name" : "Desenvolvedor Front-end", "description" : "FRONTEND_DEVELOPER"},
    {"name" : "Desenvolvedor Back-end", "description" : "BACKEND_DEVELOPER"},
    {"name" : "Coordenador", "description" : "COORDINATOR"}
]


def populate_db_country():
    if is_table_empty(Country.query.first(), 'countries'):
        Country.seed('Brazil' , 'Português')
        print('Countries populated')

def populate_db_state():
    if is_table_empty(State.query.first(), 'states'):
        country = Country.query.first()
        country_dict = country_share_schema.dump(country)
        states_data = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
        for stateObject in states_data.json(): # For para criar dados em massa dos estados
            State.seed(
            country_dict['id'],
            stateObject['nome'],
            stateObject['sigla']
            )
        print('States populated')

def populate_db_city():
    if is_table_empty(City.query.first(), 'cities'):
        cities_data = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/municipios")
        state = State.query.order_by(State.name.asc()).all()
        state_dict = states_share_schema.dump(state)

        for city_object in cities_data.json():
            state_id = 0
            for state_object in state_dict:
                if state_object['initials'] == city_object['microrregiao']['mesorregiao']['UF']['sigla']:
                    state_id = state_object['id']
            City.seed(
            state_id,
            city_object['nome']
            )
        print('Cities populated')

def populate_db_gender():
    if is_table_empty(Gender.query.first(), 'genders'):
        genders = ['male','female' , 'trans' , 'other']
        for gender in genders:
            Gender.seed(
                gender
            )
        print("Genders populated")

def populate_db_permission():
        if is_table_empty(Permission.query.first(), 'permissions'):
            permissions = ['DELETE', 'READ', 'WRITE', 'UPDATE']
            for permission in permissions:
                Permission.seed(
                    permission
                )
            print('Permissions populated')

def populate_db_product_category():
    if is_table_empty(Product_Categories.query.first(), 'product_categories'):
        categories = ['Computador', 'Celular', 'Tablet', 'Cadeira', 'Mesa', 'Teclado', 'Mouse', 'Televisao']
        for category in categories:
            Product_Categories.seed(
            category
            )
        print('Product Categories populated')

def populate_db_permission():
        if is_table_empty(Permission.query.first(), 'permissions'):
            permissions = ['DELETE', 'READ', 'WRITE', 'UPDATE']
            for permission in permissions:
                Permission.seed(
                    permission
                )
            print('Permissions populated')

def populate_db_role():
        permissions = [
            {"role" : "admin" , "permissions" : Permission.query.all()},
            {"role" : "fe" , "permissions" : Permission.query.filter(Permission.description.in_(['READ', 'WRITE'])).all()},
            {"role" : "be" , "permissions" : Permission.query.filter(Permission.description.in_(['READ', 'WRITE'])).all()},
            {"role" : "coord" , "permissions" : Permission.query.filter(Permission.description.in_(['READ', 'WRITE' , 'UPDATE'])).all()}
        ]
        
        if is_table_empty(Role.query.first(), 'roles'):
            for index , role in enumerate(roles):
                Role.seed(
                    role['description'],
                    role['name'],
                    permissions[index]['permissions']
                )
            print("Roles populated")
        
def populate_db_user():
    if is_table_empty(User.query.first(), 'users'):
        for user in users:
            User.seed(
                user['city_id'], user['gender_id'], user['role_id'],  user['name'], user['age'],
                user['email'], user['phone'], user['password'], user['cep'], user['street'], user['district'],
                user['complement'], user['landmark'], user['number_street']
            )
        print("Users populated")

def populate_db_inventory():
    if is_table_empty(Inventory.query.first(), 'inventories'):
        number_seed_limit = 30
        data_products = []
        
        with open("src/app/db/data_faker.json") as f:
            data = loads(f.read())
            
            for key, value in data.items():
                data_products.append(value)

        print(data_products[randint(1 , 9)])
        while number_seed_limit > 0:
            for index in range(number_seed_limit):
                if len(data_products) > 0:
                    data = data_products[randint(0 , 8)]
                    Inventory.seed(
                        product_category_id=data['product_category_id'],
                        user_id=random_or_none(),
                        title=data['title'],
                        product_code=index + 1,
                        value=float(data['value']),
                        brand=data['brand'],
                        template=data['template'],
                        description=data['description']
                )
                    number_seed_limit -= 1
        print("Populating inventory done")

# Função final que vai chamar as demais funções de inserção de dados
def populate_db():
    populate_db_country()
    populate_db_state()
    populate_db_city()
    populate_db_gender()
    populate_db_permission()
    populate_db_product_category()
    populate_db_role()
    populate_db_user()
    populate_db_inventory()
