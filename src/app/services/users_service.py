import re
from datetime import datetime, timedelta, timezone

from src.app.models.role import Role, role_share_schema
from src.app.models.schemas.user_schema import user_create_schema
from src.app.models.user import User, user_share_schema
from src.app.utils import excludeNone, generate_jwt


def login_user(email: str, password: str):
    try:
        user = User.query.filter_by(email=email).first_or_404()

        if not user or not user.validate_password(password):
            return {"error": "Suas credênciais estão incorretas!", "status_code": 401}

        user_dict = user_share_schema.dump(user)

        payload = {
            "user_id": user.id,
            "exp": datetime.now(tz=timezone.utc) + timedelta(days=1),
            "roles": user_dict["roles"],
        }
        token = generate_jwt(payload)

        return {"token": token, "status_code": 200}

    except Exception as e:
        return {"error": f"{e}"}


def create_user(data):
    try:
        user_create_schema.load(data)
        new_user = User.seed(data)
        result = user_share_schema.dump(new_user)

        return result
    except Exception as e:
        return {"error": f"{e}", "status_code": 500}


def get_user_by_email(email):
    try:
        user_query = User.query.filter_by(email=email).first_or_404()
        user_dict = user_share_schema.dump(user_query)
        return {"id": user_dict["id"], "roles": user_dict["roles"]}
    except:
        return {"error": "Algo deu errado!", "status_code": 500}


def get_user_by_id(id):
    try:
        user = User.query.get(id)
        return user
    except:
        return {"error": "Algo deu errado!", "status_code": 404}


def update_user_by_id(user, request_json):
    user = get_user_by_id(user["id"])
    user.update(request_json)


def validate_fields_nulls(request_json, list_keys):
    excludeNone(request_json)

    if not request_json:
        return {
            "error": "Não é possivel realizar operação, não há campos não preenchidos"
        }
    for key in request_json:
        if key not in list_keys:
            return {f"error": f"Campo '{key}' não existe ou não pode ser alterado"}
        if request_json[key] == "" and list_keys[key] != None and list_keys[key] != "":
            return {f"error": f"Campo '{key}' não pode ser alterado para nulo"}


def format_print_user(self):
    id = self["role_id"]
    roles = Role.query.filter_by(id=id).first_or_404()
    role = role_share_schema.dump(roles)

    return {
        "id": self["id"],
        "name": self["name"],
        "email": self["email"],
        "phone": self["phone"],
        "role": role["name"],
    }
