import os
import requests
import json

from flask.globals import session
from flask.wrappers import Response
from flask import Blueprint, request, jsonify, current_app

user = Blueprint('user', __name__, url_prefix="/user")

@user.route("/logout", methods = ["POST"])
def logout():

  session.clear()
  return Response(
      response=json.dumps({"message":"Você foi deslogado."}),
      status=202,
      mimetype='application/json'
    )
  