from src.app import DB, MA


class Permission(DB.Model):
    __tablename__ = 'permissions'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    description = DB.Column(DB.String(128), nullable = False)

    def __init__(self, id, description):  
      self.description = description

class PermissionSchema(MA.Schema):
    class Meta: 
        fields = ('id', 'description')

Permission_share_schema = PermissionSchema()
Permissions_share_schema = PermissionSchema(many = True)