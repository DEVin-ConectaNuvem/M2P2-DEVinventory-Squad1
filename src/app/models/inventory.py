from src.app import DB, MA


class Inventory(DB.Model):
  __tablename__ = "inventory"
  id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
  # product_category_id = DB.Column(DB.Integer, DB.ForeignKey("product_category.id"))
  user_id = DB.Column(DB.Integer, DB.ForeignKey("user.id"))
  title = DB.Column(DB.String(255), nullable=False)
  product_code = DB.Column(DB.Integer, autoincrement=True, nullable=False, unique=True)
  value = DB.Column(DB.float, nullable=False)
  brand = DB.Column(DB.String(255), nullable=False)
  template = DB.Column(DB.String(255), nullable=False)
  description = DB.Column(DB.String(255), nullable=False)
  
  def __init__(self, product_category_id, user_id, title, product_code, value, brand, template, description):
    self.product_category_id = product_category_id
    self.user_id = user_id
    self.title = title
    self.product_code = product_code
    self.value = value
    self.brand = brand
    self.template = template
    self.description = description
    
  @classmethod
  def seed(cls, user_id, title, product_code, value, brand, template, description):
    inventory = Inventory(user_id, title, product_code, value, brand, template, description)
    inventory.save()
    return inventory
    
  def save(self):
    DB.session.add(self)
    DB.session.commit()

class InventorySchema(MA.Schema):
    class Meta: 
        fields = ('id', 'product_category_id', 'user_id', 'title', 'product_code', 'value', 'brand', 'template', 'description')

inventory_share_schema = InventorySchema()
Inventory_share_schema = InventorySchema(many = True) 