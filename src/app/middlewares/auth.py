from functools import wraps
from jwt import decode
from flask import request, jsonify, current_app

def jwt_required(current_func):
    @wraps(current_func)
    def wrapper(*args, **kwargs):
      token = None

      if 'authorization' in request.headers:
        token = request.headers['authorization']