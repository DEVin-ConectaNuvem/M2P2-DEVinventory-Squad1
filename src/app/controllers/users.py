from crypt import methods
import os
import requests
import json

from flask.globals import session
from flask.wrappers import Response
from flask import Blueprint, request, jsonify, current_app

from google_auth_oauthlib.flow import Flow

user = Blueprint('user', __name__, url_prefix="/user")

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
  