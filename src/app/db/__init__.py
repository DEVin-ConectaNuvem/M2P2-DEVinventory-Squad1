import requests
from sqlalchemy.sql.expression import func

from src.app.models.country import Country, country_share_schema


def populate_db_country():
    country = Country.query.first()
    if country == None:
        Country.seed('Brazil' , 'Português')



# Função final que vai chamar as demais funções de inserção de dados
def populate_db():
    populate_db_country()
