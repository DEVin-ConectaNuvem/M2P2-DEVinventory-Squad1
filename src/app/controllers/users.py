import json
import os

import requests
from flask import Blueprint, current_app, jsonify, request
from flask.globals import session
from flask.wrappers import Response
from google import auth
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from werkzeug.utils import redirect

from src.app import DB, MA
from src.app.middlewares.auth import logged_in, requires_access_level
from src.app.models.user import User, user_share_schema, users_share_schema
from src.app.services.users_service import (create_user, format_print_user,
                                            get_user_by_email, get_user_by_id,
                                            login_user, validate_fields_nulls)
from src.app.utils import exist_key, generate_jwt

user = Blueprint("user", __name__, url_prefix="/user")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_secrets_file(
    client_secrets_file="src/app/db/client_secret.json",
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ],
    redirect_uri="http://localhost:5000/user/callback",
)


@user.route("/login", methods=["POST"])
@logged_in()
def login():
    
    list_keys = ["email", "password"]
    data = exist_key(request.get_json(), list_keys)
    if 'error' in data:
        return jsonify(data), 400

    response = login_user(data["email"], data["password"])
    if "error" in response:
        return jsonify(response), 400

    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@user.route("/auth/google", methods=["POST"])
def auth_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state

    return Response(
        response=json.dumps({"url": authorization_url}),
        status=200,
        mimetype="application/json",
    )


@user.route("/callback", methods=["GET"])
def callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = requests.session()
    token_google = auth.transport.requests.Request(session=request_session)

    user_google_dict = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request=token_google,
        audience=current_app.config["GOOGLE_CLIENT_ID"],
    )

    user = get_user_by_email(user_google_dict["email"])

    if "error" in user:
        new_user = {
            'city_id':1,
            'gender_id':1,
            'role_id':3,
            'name':user_google_dict["name"],
            'age':None,
            'email':user_google_dict["email"],
            'phone':None,
            'password':'senha123',
            'cep':None,
            'street':None,
            'district':None,
            'complement':None,
            'landmark':None,
            'number_street':None
        }
        user = create_user(new_user)
    
    user_google_dict["user_id"] = user["id"]
    user_google_dict["roles"] = user["roles"]
    session["google_id"] = user_google_dict.get("sub")
    del user_google_dict["aud"]
    del user_google_dict["azp"]

    token = generate_jwt(user_google_dict)

    return redirect(f"{current_app.config['FRONTEND_URL']}?jwt={token}")


@user.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Você foi deslogado"}), 200


@user.route("/", methods=["POST"])
@requires_access_level(["READ", "WRITE", "UPDATE", "DELETE"])
def create():
    data = request.get_json()
    response = create_user(data)
    
    if "error" in response:
        return jsonify(response), 400

    return jsonify(response), 201


@user.route("/<int:id>", methods=["GET"])
@requires_access_level(["READ"])
def get_user_by_name(id):
    page = request.args.get("page", 1, type=int)
    per_page = 20
    pager = User.query.paginate(page, per_page, error_out=False)

    if id is None or id == 0:
        users = users_share_schema.dump(pager.items)
        result = [format_print_user(result) for result in users]

        return jsonify({"Status": "Sucesso", "Dados": result}), 200

    user_query = User.query.filter(
        User.name.ilike("%" + id + "%")
    ).all()

    user = users_share_schema.dump(user_query)

    if not user:
        return Response(
            response=jsonify({"message": "Usuario nao encontrado."}),
            status=204,
            mimetype="application/json",
        )

    result = [format_print_user(result) for result in user]

    return jsonify({"Status": "Sucesso", "Dados": result}), 200


@user.route("/<int:id>", methods=["PATCH"])
@requires_access_level(["UPDATE"])
def update_user_by_id(id):
  user = get_user_by_id(id)
  data = request.get_json()
  list_keys = ["role_id", "gender_id", "city_id", "age", "name", "email", "phone", "password", "cep", "street", "district", "number_street", "complement", "landmark"]
  
  if not user:
    return Response(
        response=jsonify({"message": "Usuario nao encontrado."}),
        status=404,
        mimetype="application/json",
  )
  validate_values_keys = validate_fields_nulls(data, list_keys)
  if validate_values_keys is not None and 'error' in validate_values_keys:
    return Response(
        response=json.dumps(validate_values_keys), status=400, mimetype="application/json"
  )
  user.update(data)
  result = user_share_schema.dump(user)
  return Response(
      response=json.dumps(result), 
      status=204, 
      mimetype="application/json"
  )