import json
import requests

from flask import Blueprint, current_app, request, jsonify
from flask.globals import session
from flask.wrappers import Response
from werkzeug.utils import redirect
from google_auth_oauthlib.flow import Flow
from google import auth 
from google.oauth2 import id_token

from src.app.utils import exist_key, generate_jwt
from src.app.models.user import User, users_share_schema
from src.app.services.users_service import create_user, login_user, get_user_by_email
from src.app.middlewares.auth import requires_access_level
from src.app.models.role import Role, role_share_schema

user = Blueprint('user', __name__, url_prefix="/user")

flow = Flow.from_client_secrets_file(
  client_secrets_file="src/app/db/client_secret.json",
  scopes=[
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
  ],
  redirect_uri = "http://localhost:5000/user/callback"
)

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
  
@user.route('/create', methods = ["POST"])
@requires_access_level("WRITE")
def create():
  list_keys = ["city_id", "name", "age", "email", "password"]

  data = exist_key(request.get_json(), list_keys)

  roles = None

  if "roles" in data:
    roles = data['roles']
  
  response = create_user(
    data["city_id"],
    data["gender_id"],
    data["role_id"], 
    data["name"], 
    data["age"],
    data["email"],
    data["phone"],
    data["password"],
    data["cep"],
    data["street"],
    data["district"],
    data["complement"],
    data["landmark"],
    data["number_street"],
    roles
  )

  if "error" in response:
    return Response(
      response=json.dumps(response),
      status=400,
      mimetype='application/json'
    )

  return Response(
    response=json.dumps(response),
    status=201,
    mimetype='application/json'
  )

@user.route('/callback', methods = ["GET"])
def callback():

  flow.fetch_token(authorization_response = request.url)
  credentials = flow.credentials
  request_session = requests.session()
  token_google = auth.transport.requests.Request(session=request_session)

  user_google_dict = id_token.verify_oauth2_token(
    id_token = credentials.id_token,
    request=token_google,
    audience=current_app.config['GOOGLE_CLIENT_ID']
  )
  
  user = get_user_by_email(user_google_dict['email'])

  if "error" in user:
    user = create_user(
      50,
      user_google_dict['name'],
      25,
      user_google_dict['email'],
      "PASSWORD_DEFAULT",
      None
    )
  
  user_google_dict["user_id"] = user['id']
  user_google_dict["roles"] = user['roles']

  session["google_id"] = user_google_dict.get("sub")

  del user_google_dict['aud']
  del user_google_dict['azp']

  token = generate_jwt(user_google_dict)

  return redirect(f"{current_app.config['FRONTEND_URL']}?jwt={token}")


@user.route('/', methods = ["GET"])
#@requires_access_level("READ")
def get_user_by_name():
  page =  request.args.get('page', 1, type=int)
  per_page =  20
  pager = User.query.paginate(page, per_page, error_out=False)

  if not request.args.get('name'):
    users = users_share_schema.dump(pager.items)
    result = [format(result) for result in users]

    return jsonify({
        'Status': 'Sucesso',
        'Dados': result
    }), 200
  
  user_query = User.query.filter(User.name.ilike('%' + request.args.get('name') + '%')).all()
  user = users_share_schema.dump(user_query)

  if not user:
    return Response(
      response=jsonify({"message": "Usuario nao encontrado."}),
      status=204,
      mimetype='application/json'
    )
  
  result = [format(result) for result in user]

  return jsonify({
      'Status': 'Sucesso',
      'Dados': result
  }), 200


def format(self):
  id = self['role_id']
  roles = Role.query.filter_by(id=id).first_or_404()
  role = role_share_schema.dump(roles)
  
  return {
    'id': self['id'],
    'name': self['name'],
    'email': self['email'],
    'phone': self['phone'],
    'role': role['name']
  }
