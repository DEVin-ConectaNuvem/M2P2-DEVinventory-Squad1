from datetime import datetime, timedelta
import re
from src.app.models.role import Role
from src.app.models.user import User, user_share_schema
from src.app.utils import generate_jwt, check_password


def login_user(email, password: str):
    try:
        user_query = User.query.filter_by(email = email).first_or_404()
        user_dict = user_share_schema.dump(user_query)

        if not check_password(password, senha=user_dict['password']):
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
