from werkzeug.security import check_password_hash, generate_password_hash

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
    password_hash = DB.Column(DB.String(255), nullable = True)
    cep = DB.Column(DB.Integer, nullable=True)
    street = DB.Column(DB.String(128), nullable=True)
    district = DB.Column(DB.String(128), nullable=True)
    complement = DB.Column(DB.String(64), nullable=True)
    landmark = DB.Column(DB.String(64), nullable=True)
    number_street = DB.Column(DB.Integer, nullable=True) 
    
    city = DB.relationship("City", foreign_keys=[city_id])
    gender = DB.relationship("Gender", foreign_keys=[gender_id])
    roles = DB.relationship("Role", foreign_keys=[role_id])
    
    @property
    def password(self):
        raise AttributeError('Senha não é um atributo legível')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    
    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
            self.save()
        return self
    
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
