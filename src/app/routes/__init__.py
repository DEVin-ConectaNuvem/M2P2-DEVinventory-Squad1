from flask import Flask

from src.app.controllers.inventory import inventory
from src.app.controllers.users import user


def routes(app: Flask):
  app.register_blueprint(user)
  app.register_blueprint(inventory)
