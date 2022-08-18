from functools import wraps

from flask import current_app, jsonify, request
from jwt import decode

from src.app.models.user import User


def requires_access_level(permission):
    def jwt_required(function_current):
        @wraps(function_current)
        def wrapper(*args, **kwargs):

            token = None

            if "Authorization" in request.headers:
                token = request.headers["Authorization"]

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

            found_permission = 0

            for role in current_user.roles:
                for permission_in_roles in role.permissions: 
                    if permission_in_roles.description == permission:
                        found_permission = found_permission + 1

            if found_permission == 0:
                return jsonify({"error": "Você não tem permissão para essa funcionalidade"}), 403

            return function_current(current_user=current_user, *args, **kwargs)
        return wrapper
    return jwt_required
