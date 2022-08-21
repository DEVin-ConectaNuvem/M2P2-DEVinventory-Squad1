import re
from datetime import datetime, timedelta

from src.app.models.role import Role, role_share_schema
from src.app.models.user import User, user_share_schema
from src.app.utils import excludeNone, generate_jwt


def login_user(email, password: str):
    try:
        user_query = User.query.filter_by(email = email).first_or_404()
       
        if user_query.validate_password(password, senha=user_dict['password']):
            return { "error": "Suas credênciais estão incorretas!", "status_code": 401 }
          
        user_dict = user_share_schema.dump(user_query)
        
        payload = {
          "user_id": user_query.id,
          "exp": datetime.utcnow() + timedelta(days=1),
          "roles": user_dict["roles"]
        }

        token = generate_jwt(payload)

        return { "token": token, "status_code": 200 }

    except:
        return { "error": "Algo deu errado!", "status_code": 500 }


def create_user(city_id, gender_id, role_id,  name, age, email, phone, password, cep, street, district, complement, landmark, number_street):
      try:
      
        # validação telefone e senha
        regex_ca = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        regex_number_phone = re.compile('^[1-9]{2}(9[1-9])[0-9]{3}[0-9]{4}$')

        if len(phone) != 11 or not regex_number_phone.search(phone):
          return {"error": "Telefone incorreto"}
        if len(password) != 8 or not regex_ca.search(password):
          return {"error": "Senha incorreto"}

        User.seed(
          city_id,
          gender_id,
          role_id,
          name, 
          age, 
          email, 
          phone,
          password, 
          cep,
          street,
          district,
          complement,
          landmark,
          number_street
        )
        exist_user = get_user_by_email(email)

        if exist_user:
          return {"error": "Não é possivel cadastrar, usuário já existe"}
        return {"message": "Usuário foi criado com sucesso."}
      except:
        return {"error": "Algo deu errado!"}


def get_user_by_email(email):
  try:
      user_query = User.query.filter_by(email = email).first_or_404()
      user_dict = user_share_schema.dump(user_query)
      return { "id": user_dict['id'], "roles": user_dict["roles"] }
  except:
      return { "error": "Algo deu errado!", "status_code": 500 }


def get_user_by_id(id):
  try:
      user = User.query.get(id)
      return user
  except:
      return { "error": "Algo deu errado!", "status_code": 404 }


def update_user_by_id(user, request_json):
  user = get_user_by_id(user['id'])
  user.update(request_json)


def validate_fields_nulls(request_json, list_keys):
  excludeNone(request_json)
      
  if not request_json:
    return {"error": "Não é possivel realizar operação, não há campos não preenchidos"}
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
        "role": role["name"]
    }

