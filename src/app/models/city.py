from src.app import DB, MA
from src.app.models import State, state_share_schema

class City(DB.Model):
    __tablename__ = 'cities'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    state_id = DB.Column(DB.Integer, DB.ForeignKey(State.id), nullable = False)
    name = DB.Column(DB.String(128), nullable = False)

    state = DB.relationship("State", foreign_keys=[state_id])

    def __init__(self, name, state):  
      self.state = state
      self.name = name

class CitySchema(MA.Schema):
    state = MA.Nested(state_share_schema)

    class Meta: 
        fields = ('id', 'name', "state")

city_share_schema = CitySchema()
citys_share_schema = CitySchema(many = True)