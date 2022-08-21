import re

from marshmallow import Schema, ValidationError, fields, validates

from src.app.models.inventory import Inventory
from src.app.models.schemas.error_messages import set_error_message
from src.app.models.user import User


class InventoryCreateSchema(Schema):
        user_id=fields.Integer(Required=False)
        product_category_id= fields.Integer(required=True, error_messages=set_error_message('product_category_id'))
        title=fields.Str(required=True, error_messages=set_error_message('title'))
        value=fields.Float(required=True, error_messages=set_error_message('value'))
        brand=fields.Str(required=True, error_messages=set_error_message('brand'))
        template=fields.Str(required=True, error_messages=set_error_message('template'))
        description=fields.Str(required=True, error_messages=set_error_message('description'))
        product_code=fields.Integer(required=True, error_messages=set_error_message('product_code'))
        
        @validates('product_code')
        def validate_product_code(self, value):
            if Inventory.query.filter_by(product_code=value).first():
                raise ValidationError('Código já registrado')
            if value < 0:
                raise ValidationError('Código inválido')
        
        @validates('value')
        def validate_value(self, value):
            if value <= 0:
                raise ValidationError('Valor inválido')
    
        @validates('template')
        def validate_template(self, value):
            if re.match(r'^https://.*', value) is None:
                raise ValidationError('Template inválido')
        
        @validates('user_id')
        def exists_user_id(self, value):
            if not User.query.get(value):
                raise ValidationError("Usuário não encontrado.")
        
        @validates('product_category_id')
        def exists_product_category_id(self, value):
            if not User.query.get(value):
                raise ValidationError("Categoria não encontrada.")
            
inventory_create_schema = InventoryCreateSchema()        
            