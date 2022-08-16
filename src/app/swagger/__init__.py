from flasgger import Swagger
from flask import Flask


def create_swagger(app: Flask):
  app.config['SWAGGER'] = {
    'openapi': '3.0.0',
    'title': 'DEVinventory',
    'description': "Aplicação para controle de empréstimo de itens a colaboradores"
  }

  Swagger(app)