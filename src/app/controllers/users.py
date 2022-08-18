import json

import requests
from flask import Blueprint, current_app, jsonify, request
from flask.globals import session
from flask.wrappers import Response
from google_auth_oauthlib.flow import Flow

from src.app.services.users_service import login_user
from src.app.utils import exist_key, generate_jwt

user = Blueprint('user', __name__, url_prefix="/user")


@user.route('/login', methods = ["POST"])
def login():
  list_keys = ["email", "password"]

  data = exist_key(request.get_json(), list_keys)

  response = login_user(data["email"], data["password"])

  if "error" in response:
    return Response(
      response=json.dumps({"error": response['error']}),
      status=401,
      mimetype='application/json'
    )

  return Response(
      response=json.dumps(response),
      status=200,
      mimetype='application/json'
)

@user.route("/auth/google", methods=["POST"])
def auth_google():
  authorization_url, state = Flow.authorization_url()
  session["state"] = state

  return Response(
      response=json.dumps({'url':authorization_url}),
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
  

