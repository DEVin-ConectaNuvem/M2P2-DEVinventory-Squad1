from src.app import DB, MA


class Gender(DB.Model):
    __tablename__ = 'genders'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    name = DB.Column(DB.String(128), nullable = False)

    def __init__(self, id, name):  
      self.id = id
      self.name = name

class GenderSchema(MA.Schema):
    class Meta: 
        fields = ('id', 'name')

user_share_schema = GenderSchema()
users_share_schema = GenderSchema(many = True)