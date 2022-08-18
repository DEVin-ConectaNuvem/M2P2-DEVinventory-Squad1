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
from src.app.utils import is_table_empty

# inventory , user , role

inventory = [
    {""}
    ]


def populate_db_country():
    if is_table_empty(Country.query.first()):
        Country.seed('Brazil' , 'Português')

def populate_db_state():
    if is_table_empty(State.query.first()):
        country = Country.query.first()
        country_dict = country_share_schema.dump(country)
        states_data = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
        for stateObject in states_data.json(): # For para criar dados em massa dos estados
            State.seed(
            country_dict['id'],
            stateObject['nome'],
            stateObject['sigla']
            )

def populate_db_city():
    if is_table_empty(City.query.first()):
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

def populate_db_gender():
    if is_table_empty(Gender.query.first()):
        genders = ['male','female' , 'trans' , 'other']
        for gender in genders:
            Gender.seed(
                gender
            )

def populate_db_permission():
        if is_table_empty(Permission.query.first()):
            permissions = ['DELETE', 'READ', 'WRITE', 'UPDATE']
            for permission in permissions:
                Permission.seed(
                    permission
                )

def populate_db_product_category():
    if is_table_empty(Product_Categories.query.first()):
        categories = ['Computador', 'Celular', 'Tablet', 'Cadeira', 'Mesa', 'Teclado', 'Mouse', 'Televisao']
        for category in categories:
            Product_Categories.seed(
            category
            )

# def populate_db_role():
#     if is_table_empty(Role.query.first()):    
#         permission_adm_sistema = Permission.query.all()
#         roles = ['Administrador do Sistema','Desenvolvedor Frontend', 'Desenvolvedor Backend', 'Coordenador']
#         for index, role in enumerate(roles):
#             if index == 0:
#                 Role.seed(
#                     role, 
#                     permission_adm_sistema
#                 )
#             else:
#                 permission_one = Permission.query.order_by(func.random()).limit(2).all() 
#                 Role.seed(
#                     role,
#                     permission_one       
#                 )

def populate_db_permission():
        if is_table_empty(Permission.query.first()):
            permissions = ['DELETE', 'READ', 'WRITE', 'UPDATE']
            for permission in permissions:
                Permission.seed(
                    permission
                )

# Função final que vai chamar as demais funções de inserção de dados
def populate_db():
    populate_db_country()
    populate_db_state()
    populate_db_city()
    populate_db_gender()
    populate_db_permission()
    populate_db_product_category()