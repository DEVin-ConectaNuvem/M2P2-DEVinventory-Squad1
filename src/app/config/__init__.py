import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
NAME_DB = os.getenv('NAME_DB')
USER_DB = os.getenv('USER_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')

class Development(object):
  DEBUG = True
  TESTING = False
  SQLALCHEMY_DATABASE_URI = f"postgresql://{USER_DB}:{PASSWORD_DB}@localhost:5432/{NAME_DB}-development"
  SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
  SECRET_KEY = os.getenv('SECRET_KEY')
  GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
  OAUTHLIB_INSECURE_TRANSPORT = os.getenv('OAUTHLIB_INSECURE_TRANSPORT')
  BACKEND_URL = os.getenv('BACKEND_URL')
  FRONTEND_URL = os.getenv('FRONTEND_URL')

class Testing(object):
  DEBUG = False
  TESTING = True
  SQLALCHEMY_DATABASE_URI = f"postgresql://{USER_DB}:{PASSWORD_DB}@localhost:5432/{NAME_DB}-testing"
  SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
  SECRET_KEY = os.getenv('SECRET_KEY')
  GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
  OAUTHLIB_INSECURE_TRANSPORT = os.getenv('OAUTHLIB_INSECURE_TRANSPORT')
  BACKEND_URL = os.getenv('BACKEND_URL')
  FRONTEND_URL = os.getenv('FRONTEND_URL')

class Production(object):
  DEBUG = False
  TESTING = False
  SQLALCHEMY_DATABASE_URI = f"postgresql://{USER_DB}:{PASSWORD_DB}@localhost:5432/{NAME_DB}-production"
  SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
  SECRET_KEY = os.getenv('SECRET_KEY')
  GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
  OAUTHLIB_INSECURE_TRANSPORT = os.getenv('OAUTHLIB_INSECURE_TRANSPORT')
  BACKEND_URL = os.getenv('BACKEND_URL')
  FRONTEND_URL = os.getenv('FRONTEND_URL')

app_config = {
  "development": Development, 
  "testing": Testing,
  "production": Production
}