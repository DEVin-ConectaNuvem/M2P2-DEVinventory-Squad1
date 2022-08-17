import requests
from sqlalchemy.sql.expression import func

from src.app.models.country import Country, country_share_schema
from src.app.models.user import User, user_share_schema


def populate_db_country():
    country = Country.query.first()
    if country == None:
        Country.seed('Brazil' , 'Português')

def populate_db_user():
    user = User.query.first()
    if user == None:
        User.seed('1', '1', '6', 'João Victor', 'joao@email.com', '(48) 99999-9999', 'adminadmin', '80130780', 'Rua Almeida', 'dasdas', 'Casa', 'fábrica', '45')
        User.seed('2', '2', '8', 'Ana Júlia', 'ana@email.com', '(48) 88888-8888', 'ana.$águias', '90140890', 'Avenida Águias', 'dasdas', 'Apartamento', 'Restaurante', '88')
        User.seed('3', '1', '9', 'Lucas Silva', 'lucas@email.com', '(48) 77777-7777', 'lucas@4899', '70589180', 'Rua Rubens Ramos', 'dasdas', 'Condominio', 'Posto de Gasolina', '76')
        User.seed('4', '1', '10', 'Beatriz Carla', 'beatriz@email.com', '(48) 77777-7777', 'beatriz#beaztriz', '90881762', 'Avenida Torres', 'dasdas', 'Casa', 'Parque', '66')

# Função final que vai chamar as demais funções de inserção de dados
def populate_db():
    populate_db_country()
