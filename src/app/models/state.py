from state import Country

from src.app import DB, MA


class State(DB.Model):
    __tablename__ = 'states'
    id = DB.Column(DB.Integer, autoincrement = True, primary_key = True)
    country_id = DB.Column(DB.Integer, DB.ForeignKey(Country.id), nullable = False)
    name = DB.Column(DB.String(128), nullable = False)
    initials = DB.Column(DB.String(2), nullable=False)

    country = DB.relationship("country", foreign_keys=[country_id])

    def __init__(self, country_id, name, initials):
      self.country_id = country_id
      self.name = name
      self.initials = initials

class StateSchema(MA.Schema):
    class Meta: 
        fields = ('id', 'country_id', 'name', 'initials')

State_share_schema = StateSchema()
States_share_schema = StateSchema(many = True)