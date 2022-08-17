import os

from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from src.app.config import app_config
from src.app.swagger import create_swagger

DB = SQLAlchemy()
MA = Marshmallow()

def create_app():

  app = Flask(__name__)

  from src.app.models import role, gender, permission, country, state, city, product_categories, inventory, user

  app.config.from_object(app_config[os.getenv('FLASK_ENV')])
  DB.init_app(app)
  MA.init_app(app)
  Migrate(app=app, db=DB, directory='./src/app/migrations')
  create_swagger(app)
  CORS(app)
  app.config["Access-Control-Allow-Origin"] = "*"
  app.config["Access-Control-Allow-Headers"] = "Content-Type"
  from src.app.models import country
  CORS(app)
  app.config['Access-Control-Allow-Origin'] = '*'
  app.config["Access-Control-Allow-Headers"]="Content-Type"


  return app
