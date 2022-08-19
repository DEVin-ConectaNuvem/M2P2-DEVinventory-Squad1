import bcrypt

from src.app import DB, MA
from src.app.models.city import City, city_share_schema
from src.app.models.gender import Gender, gender_share_schema
from src.app.models.role import Role, role_share_schema


class User(DB.Model):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    city_id = DB.Column(DB.Integer, DB.ForeignKey(City.id), nullable = False)
    gender_id = DB.Column(DB.Integer, DB.ForeignKey(Gender.id), nullable = False)
    role_id = DB.Column(DB.Integer, DB.ForeignKey(Role.id), nullable = False)
    name = DB.Column(DB.String(128), nullable = False)
    age = DB.Column(DB.DateTime, nullable = True)
    email = DB.Column(DB.String(128), unique=True, nullable = False)
    phone = DB.Column(DB.String(128), nullable = True)
    password = DB.Column(DB.String(84), nullable = True)
    cep = DB.Column(DB.Integer, nullable=True)
    street = DB.Column(DB.String(128), nullable=True)
    district = DB.Column(DB.String(128), nullable=True)
    complement = DB.Column(DB.String(64), nullable=True)
    landmark = DB.Column(DB.String(64), nullable=True)
    number_street = DB.Column(DB.Integer, nullable=True) 
    
    city = DB.relationship("City", foreign_keys=[city_id])
    gender = DB.relationship("Gender", foreign_keys=[gender_id])
    roles = DB.relationship("Role", foreign_keys=[role_id])

    
    def __init__(self, city_id, gender_id, role_id,  name, age, email, phone, password, cep, street, district, complement, landmark, number_street):
      self.city_id = city_id
      self.gender_id = gender_id
      self.role_id = role_id
      self.name = name
      self.age = age
      self.email = email
      self.phone = phone
      self.password = password
      self.cep = cep
      self.street = street
      self.district = district
      self.complement = complement
      self.landmark = landmark
      self.number_street = number_street
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
    
    @classmethod
    def seed(cls, city_id, gender_id, role_id,  name, age, email, phone, password, cep, street, district, complement=None, landmark=None, number_street=None):
        user = User(
            city_id=city_id,
            gender_id=gender_id,
            role_id=role_id,
            name=name,
            age=age,
            email=email,
            phone=phone,
            password=User.encrypt_password(password=password),
            cep=cep,
            street=street,
            district=district,
            complement=complement,
            landmark=landmark,
            number_street=number_street
        )
        user.save()
        return user

    @staticmethod
    def encrypt_password(password):
        return bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
    
    def save(self):
        DB.session.add(self)
        DB.session.commit()

class UserSchema(MA.Schema):
    city = MA.Nested(city_share_schema)
    gender = MA.Nested(gender_share_schema)
    roles = MA.Nested(role_share_schema)
    class Meta: 
        fields = ('id', 'city_id', 'gender_id', 'role_id', 'name', 'age', 'email', "phone", 'password', "cep", "street", "disctict", "complement", "landmark", 'number_street', "city", "gender", "roles")

user_share_schema = UserSchema()
users_share_schema = UserSchema(many = True)
