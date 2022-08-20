from src.app import DB, MA


class Product_Categories(DB.Model):
    __tablename__ = 'product_categories'
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    name = DB.Column(DB.String(84), nullable=False)
     
    @classmethod
    def seed(cls , name):
        product_categories = Product_Categories(
            name = name ,
            )
        product_categories.save()
        return product_categories
    
    def save(self):
        DB.session.add(self)
        DB.session.commit()

class Product_CategoriesSchema(MA.Schema):
    class Meta:
        fields = ['id' , 'name']


product_category_share_schema = Product_CategoriesSchema()
product_categories_share_schema = Product_CategoriesSchema(many = True)