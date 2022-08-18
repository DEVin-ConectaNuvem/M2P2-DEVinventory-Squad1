import os
import requests
import json

from flask.globals import session
from flask.wrappers import Response
from flask import Blueprint, request, jsonify, current_app

from src.app.utils import exist_key, generate_jwt
from src.app.services.users_service import create_user, login_user, get_user_by_email


user = Blueprint('user', __name__, url_prefix="/user")


@user.route('/login', methods = ["POST"])
def login():
  list_keys = ["email", "password"]

  data = exist_key(request.get_json(), list_keys)

  response = login_user(data["email"], data["password"])

  if "error" in response:
    return Response(
      response=json.dumps({"error": response['error']}),
      status=response['status_code'],
      mimetype='application/json'
    )

  return Response(
      response=json.dumps(response),
      status=200,
      mimetype='application/json'
  )


@user.route("/logout", methods = ["POST"])
def logout():

  session.clear()
  return Response(
      response=json.dumps({"message":"Você foi deslogado."}),
      status=202,
      mimetype='application/json'
    )
  
