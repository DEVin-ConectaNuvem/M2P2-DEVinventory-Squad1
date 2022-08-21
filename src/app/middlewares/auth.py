from functools import wraps

from flask import current_app, jsonify, request
from jwt import decode

from src.app.models.user import User, user_share_schema


def requires_access_level(permissions):
    def jwt_required(function_current):
        @wraps(function_current)
        def wrapper(*args, **kwargs):
            token = None
            
            token = request.headers.get("Authorization")
                
            if not token:
                return jsonify({"error": "Você não tem permissão"}), 403

            if not "Bearer" in token:
                return jsonify({"error": "Você não tem permissão"}), 401

            try:
                token_pure = token.replace("Bearer ", "")
                decoded = decode(token_pure, current_app.config["SECRET_KEY"], "HS256")
                current_user = User.query.get(decoded["user_id"])
            except:
                return jsonify({"error": "O Token é inválido"}), 403

            user = user_share_schema.dump(current_user)
            user_permissions = user["roles"].get("permissions")
            list_permissions_user = []
            
            for permission in user_permissions:
                list_permissions_user.append(permission["description"])
  
            for permission in permissions:
                if permission not in list_permissions_user:
                    print(permission)
                    return jsonify({"error": "Você não tem permissão"}), 403

            return function_current(*args, **kwargs)
        return wrapper
    return jwt_required

def logged_in():
    def jwt_required(function_current):
        @wraps(function_current)
        def wrapper(*args, **kwargs):
            token = None
            token = request.headers.get("Authorization")
            
            if not token:
                return function_current(*args, **kwargs)
            else:
                return jsonify({"error": "Você já está logado"}), 403

        return wrapper
    return jwt_required

            