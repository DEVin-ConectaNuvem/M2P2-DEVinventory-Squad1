from state import State

from src.app import DB, MA


class City(DB.Model):
    __tablename__ = 'cities'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    state_id = DB.Column(DB.Integer, DB.ForeignKey(State.id), nullable = False)
    name = DB.Column(DB.String(128), nullable = False)

    state = DB.relationship("State", foreign_keys=[state_id])

    def __init__(self, state_id, name):
      self.state_id = state_id
      self.name = name

class CitySchema(MA.Schema):
    class Meta: 
        fields = ('id', 'description', "state")

city_share_schema = CitySchema()
citys_share_schema = CitySchema(many = True)