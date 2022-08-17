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

    @classmethod
    def seed(cls, state_id, name):
        city = City(
        state_id = state_id,
        name = name
        )
        city.save()

    def save(self): 
        DB.session.add(self)
        DB.session.commit()


class CitySchema(MA.Schema):
    class Meta: 
        fields = ('id', 'state_id', 'name', 'state')

city_share_schema = CitySchema()
citys_share_schema = CitySchema(many = True)