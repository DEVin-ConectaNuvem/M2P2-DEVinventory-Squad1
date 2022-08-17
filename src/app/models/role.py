from src.app import DB, MA
from src.app.models.permission import Permissions_share_schema

roles_permissions = DB.Table('roles_permissions',
                    DB.Column('role_id', DB.Interger, DB.ForeignKey('roles.id')),
                    DB.Column('permission_id', DB.Interger, DB.ForeignKey('permissions.id'))
                )


class Role(DB.Model):
    __tablename__ = 'roles'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    description = DB.Column(DB.String(128), nullable = False)
    name =  DB.Column(DB.String(128), nullable = False)

    permissions = DB.relationship('Permission', secondary = roles_permissions, backref= 'roles')

    def __init__(self, name, description, permissions):
        self.name = name  
        self.description = description
        self.permissions = permissions
    
    @classmethod
    def seed(cls,name,description, permissions):
        role = Role(
            name=name,
            description= description,
            permissions=permissions
        )


class RoleSchema(MA.Schema):
    permissions = MA.Nested(Permissions_share_schema)
    class Meta: 
        fields = ('id', 'description', 'permissions')

role_share_schema = RoleSchema()
roles_share_schema = RoleSchema(many = True)