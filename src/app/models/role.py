from src.app import DB, MA


class Role(DB.Model):
    __tablename__ = 'roles'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    description = DB.Column(DB.String(128), nullable = False)
    name = DB.Column(DB.String(128), nullable = False)
    

    def __init__(self, description, name):  
      self.description = description
      self.name = name
    
    @classmethod
    def seed(cls, description, name):
        role = Role(
            description=description,
            name=name
        )
        role.save()
        return role
    
    def save(self):
        DB.session.add(self)
        DB.session.commit()

class RoleSchema(MA.Schema):
    class Meta: 
        fields = ('id', 'description', 'name')

role_share_schema = RoleSchema()
roles_share_schema = RoleSchema(many = True)