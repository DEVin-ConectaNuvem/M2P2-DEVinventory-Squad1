from src.app import DB, MA
from src.app.models import Country, country_share_schema

class State(DB.Model):
    __tablename__ = 'states'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    country_id = DB.Column(DB.Integer, DB.ForeignKey(Country.id), nullable = False)
    name = DB.Column(DB.String(128), nullable = False)
    initials = DB.Column(DB.String(2), nullable=False)

    country = DB.relationship("country", foreign_keys=[country_id])

    def __init__(self, name, initials, country):  
      self.name = name
      self.initials = initials
      self.country = country

class StateSchema(MA.Schema):
    country = MA.Nested(country_share_schema)

    class Meta: 
        fields = ('id', 'description', "state")

State_share_schema = StateSchema()
States_share_schema = StateSchema(many = True)