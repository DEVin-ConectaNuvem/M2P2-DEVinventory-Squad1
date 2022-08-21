import re
from datetime import datetime

from marshmallow import Schema, ValidationError, fields, pre_load, validates

from src.app.models.city import City
from src.app.models.gender import Gender
from src.app.models.role import Role
from src.app.models.user import User
from src.app.utils import format_date


class UserCreateSchema(Schema):
    city_id = fields.Integer(required=True, error_messages={"required": "Cidade é obrigatório."})
    gender_id = fields.Integer(required=True, error_messages={"required": "Gênero é obrigatório."})
    role_id = fields.Integer(required=True, error_messages={"required": "Função é obrigatório."})
    name= fields.Str(required=True, error_messages={"required": "Nome é obrigatório."})
    age= fields.DateTime(error_messages={"invalid": "A data informada está incorreta."})
    email=fields.Email(required=True, error_messages={"required": "Email é obrigatório."})
    phone=fields.Str()
    password=fields.Str(required=True, error_messages={"required": "Senha é obrigatório."})
    cep=fields.Str()
    street=fields.Str()
    district=fields.Str()
    complement=fields.Str()
    landmark=fields.Str()
    number_street=fields.Integer()
    
    @pre_load
    def format_data(self, data, **kwargs):
        data["age"] = format_date(data["age"])
        return data
   
    @validates("city_id")
    def exists_city_id(self, value):
        if not City.query.get(value):
            raise ValidationError("Cidade não encontrada.")

    @validates("gender_id")
    def exists_gender_id(self, value):
        if not Gender.query.get(value):
            raise ValidationError("Gênero não encontrado.")
        
    @validates("role_id")
    def exists_role_id(self, value):
        if not Role.query.get(value):
            raise ValidationError("Função não encontrada.")   
    
    @validates('email')
    def validate_email(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError('Email já registrado')
    
    @validates('phone')
    def validate_phone(self, value):
        if re.match(r'^\d{11}$', value) is None:
            raise ValidationError('Telefone inválido')
        
    @validates('password')
    def strong_password(self, value):
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', value) is None:
            raise ValidationError('Senha fraca, utilize letras maiúsculas, minúsculas, números e caracteres especiais')
        
    @validates('cep')
    def validate_cep(self, value):
        if re.match(r'^\d{8}$', value) is None:
            raise ValidationError('CEP inválido')
    
    @validates('number_street')
    def validate_number_street(self, value):
        if value is None or value < 0:
            raise ValidationError('Número da rua inválido')
    
    @validates('age')
    def validate_birthday(self, value):
        if value > datetime.now():
            raise ValidationError('Data de nascimento inválida')
    

user_create_schema = UserCreateSchema()   
 
    