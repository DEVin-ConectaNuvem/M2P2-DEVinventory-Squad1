from src.app import DB, MA

class Product_Categories(DB.Model):
    __tablename__ = 'product_categories'
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    name = DB.Column(DB.String(84), nullable=False)
     
    def __init__(self , name):
        self.name = name

    @classmethod
    def seed(cls , name):
        product_categorie = Product_Categories(
            name = name ,
            )
        product_categorie.save()
        return product_categorie
    
    def save(self):
        DB.session.add(self)
        DB.session.commit()

class Product_CategoriesSchema(MA.Schema):
    class Meta:
        fields = ['id' , 'name']


product_categorie_share_schema = Product_CategoriesSchema()
product_categorie_share_schema = Product_CategoriesSchema(many = True)