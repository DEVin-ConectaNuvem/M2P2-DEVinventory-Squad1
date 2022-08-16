from src.app import DB, MA


class Role(DB.Model):
    __tablename__ = 'roles'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    description = DB.Column(DB.String(128), nullable = False)

    def __init__(self, description):  
      self.description = description

class RoleSchema(MA.Schema):
    class Meta: 
        fields = ('id', 'description')

role_share_schema = RoleSchema()
roles_share_schema = RoleSchema(many = True)