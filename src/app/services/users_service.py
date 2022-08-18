from datetime import datetime, timedelta
from src.app.utils import generate_jwt

from src.app.models.user import User, user_share_schema


def login_user(email, password):
  try:
    user_query = User.query.filter_by(email = email).first_or_404()
    user_dict = user_share_schema.dump(user_query)

    if not user_query.check_password(password):
      return { "error": "Suas credênciais estão incorretas!", "status_code": 401 }
    
    payload = {
      "user_id": user_query.id,
      "exp": datetime.utcnow() + timedelta(days=1),
      "roles": user_dict["roles"]
    }

    token = generate_jwt(payload)

    return { "token": token, "status_code": 200 }

  except:
    return { "error": "Algo deu errado!", "status_code": 500 }
