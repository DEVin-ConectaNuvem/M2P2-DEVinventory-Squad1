import requests

from flask import json
from sqlalchemy.sql.expression import func

from src.app.models.city import City, citys_share_schema
from src.app.models.country import Country, country_share_schema
from src.app.models.state import State, states_share_schema
from src.app.models.permission import Permission
from src.app.models.role import Role
from src.app.models.user import User
from src.app.models.gender import Gender, genders_share_schema


#Populando o banco com API externa
def populate_db_country():
    country = Country.query.first()
    if country == None:
        Country.seed('Brazil' , 'Português')
       
def populate_db_states_cities_users():
    brasil_code = 76
    countries_data = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/paises/{brasil_code}")
    states_data = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    cities_data = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/municipios")

    country_name = countries_data.json()[0]['nome']
    Country.seed(country_name, 'Português') # Seed utilizada para salvar dados

    country = Country.query.first() # Query para verificar se existe dados salvos
    country_dict = country_share_schema.dump(country) # Método para serializar o dado

    for stateObject in states_data.json(): # For para criar dados em massa dos estados
        State.seed(
        country_dict['id'],
        stateObject['nome'],
        stateObject['sigla']
        )

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

    cities = City.query.order_by(City.name.asc()).all()
    cities_dict = citys_share_schema.dump(cities)

    genders = Gender.query.order_by(Gender.description.asc()).all()
    genders_dict = genders_share_schema.dump(genders)

    # trabalahndo com usuários
    users = requests.get('https://randomuser.me/api?nat=br&results=50') # definir a quantidade de usuários

    permissions = ['DELETE', 'READ', 'WRITE', 'UPDATE']
    roles = ['Administrador do Sistema','Desenvolvedor Frontend', 'Desenvolvedor Backend', 'Coordenador']
    gender_create_data = ['male','female']

    # criando as permissions no banco de dados
    for permission in permissions:
        Permission.seed(
        permission
        )
    
    for gender in gender_create_data:
        Gender.seed(
            gender
        )
    
    # O ADM do sistema tem todas as permissões
    permission_adm_sistema = Permission.query.all()

    for index, role in enumerate(roles):
        if index == 0:
            Role.seed(
                role, 
                permission_adm_sistema
            )
        else:
            permission_one = Permission.query.order_by(func.random()).limit(2).all() 
            Role.seed(
                role,
                permission_one       
            )

    # usuários
    for user in users.json()['results']:
        city_id = 2
        roles_one = Role.query.order_by(func.random()).limit(1).all()
        for city_object in cities_dict:
            if user['location']['city'] == city_object['name']:
                city_id = city_object['id']
        for gender_object in genders_dict:
            if user['gender'] == gender_object['description']:
                gender_id = gender_object['id']
        User.seed(
            city_id,
            gender_id,
            roles_one, 
            user['name']['first'] + ' ' + user['name']['last'], # primiero e ultimo nome
            user['registered']['age'],
            user['email'],
            user['phone'],
            user['login']['password'],
            user['location']['postcode'],
            user['location']['street']['name'],
            user['location'],
            None,
            None,
            user['location']['street']['number'],
        )


# Função final que vai chamar as demais funções de inserção de dados
def populate_db():
    populate_db_country()
    populate_db_states_cities_users()
