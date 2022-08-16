from src.app import DB, MA


class User(DB.Model):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    #city_id = DB.Column(DB.Integer, DB.ForeignKey(City.id), nullable = False)
    #gender_id = DB.Column(DB.Integer, DB.ForeignKey(Gender.id), nullable = False)
    #role_id = DB.Column(DB.Integer, DB.ForeignKey(Role.id), nullable = False)
    name = DB.Column(DB.String(128), nullable = False)
    age = DB.Column(DB.Integer, nullable = False)
    email = DB.Column(DB.String(128), nullable = False)
    phone = DB.Column(DB.String(128), nullable = False)
    password = DB.Column(DB.String(84), nullable = False)
    cep = DB.Column(DB.String(9), nullable=False)
    street = DB.Column(DB.String(128), nullable=False)
    district = DB.Column(DB.String(128), nullable=False)
    complement = DB.Column(DB.String(64), nullable=True)
    landmark = DB.Column(DB.String(64), nullable=True)
    number_street = DB.Column(DB.Integer, nullable=True) 
    
    #city = DB.relationship("City", foreign_keys=[city_id])
    #gender = DB.relationship("Gender", foreign_keys=[gender_id])
    #roles = DB.relationship("Role", foreign_keys=[role_id])

    
    def __init__(self, name, age, email, phone, password, cep, street, district, complement, landmark, number_street):
      #self.city_id = city_id
      #self.gender_id = gender_id
      #self.role_id = role_id
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
      #self.city = city
      #self.gender = gender
      #self.roles = roles

class UserSchema(MA.Schema):
    #city = MA.Nested(city_share_schema)
    #roles = MA.Nested(roles_share_schema)

    class Meta: 
        fields = ('id', 'name', 'age', 'email', "phone", 'password', "cep", "street", "disctict", "complement", "landmark", 'number_street')

user_share_schema = UserSchema()
users_share_schema = UserSchema(many = True)