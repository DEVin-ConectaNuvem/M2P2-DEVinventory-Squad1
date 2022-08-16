from src.app import DB, MA
from src.app.models.city import City
from src.app.models.gender import Gender
from src.app.models.role import Role


class User(DB.Model):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    city_id = DB.Column(DB.Integer, DB.ForeignKey(City.id), nullable = False)
    gender_id = DB.Column(DB.Integer, DB.ForeignKey(Gender.id), nullable = False)
    role_id = DB.Column(DB.Integer, DB.ForeignKey(Role.id), nullable = False)
    name = DB.Column(DB.String(128), nullable = False)
    age = DB.Column(DB.Datetime, nullable = False)
    email = DB.Column(DB.String(128), unique=True, nullable = False)
    phone = DB.Column(DB.String(128), nullable = False)
    password = DB.Column(DB.String(84), nullable = False)
    cep = DB.Column(DB.String(9), nullable=False)
    street = DB.Column(DB.String(128), nullable=False)
    district = DB.Column(DB.String(128), nullable=False)
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
    
    @classmethod
    def seed(cls, city_id, gender_id, role_id,  name, age, email, phone, password, cep, street, district, complement, landmark, number_street):
        user = User(
            city_id=city_id,
            gender_id=gender_id,
            role_id=role_id,
            name=name,
            age=age,
            email=email,
            phone=phone,
            password=password,
            cep=cep,
            street=street,
            district=district,
            complement=complement,
            landmark=landmark,
            number_street=number_street
        )
        user.save()
        return user
    
    def save(self):
        DB.session.add(self)
        DB.session.commit()

class UserSchema(MA.Schema):
    class Meta: 
        fields = ('id', 'city_id', 'gender_id', 'role_id', 'name', 'age', 'email', "phone", 'password', "cep", "street", "disctict", "complement", "landmark", 'number_street')

user_share_schema = UserSchema()
users_share_schema = UserSchema(many = True)