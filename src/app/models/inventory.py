from datetime import datetime

from src.app import DB, MA
from src.app.models.product_categories import (Product_Categories,
                                               product_category_share_schema)
from src.app.models.user import User, user_share_schema


class Inventory(DB.Model):
    __tablename__ = "inventories"
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    product_category_id = DB.Column(
        DB.Integer, DB.ForeignKey(Product_Categories.id), nullable=False
    )
    user_id = DB.Column(DB.Integer, DB.ForeignKey(User.id), nullable=True)
    product_code = DB.Column(DB.Integer, nullable=False, unique=True)
    title = DB.Column(DB.String(255), nullable=False)
    brand = DB.Column(DB.String(255), nullable=False)
    template = DB.Column(DB.String(255), nullable=False)
    description = DB.Column(DB.String(1000), nullable=False)
    value = DB.Column(DB.Float, nullable=False)

    product_category = DB.relationship(
        "Product_Categories", foreign_keys=[product_category_id]
    )
    user = DB.relationship("User", foreign_keys=[user_id])

    @classmethod
    def seed(cls, data):
        inventory = Inventory()
        for key, value in data.items():
            setattr(inventory, key, value)
        inventory.save()
        return inventory

    def update(self, data):
        try:
            for key, value in data.items():
                setattr(self, key, value)
            self.save()
            return self
        except Exception:
            return {"error": "Erro ao atualizar o produto"}

    def save(self):
        DB.session.add(self)
        DB.session.commit()

    def format(self):
        return {
            "id": self.id,
            "product_code": self.product_code,
            "title": self.title,
            "product_category": self.product_category.name,
            "user": {
                "name": self.user.name if self.user else "Na empresa",
                "id": self.user.id if self.user else None,
            },
        }


class InventorySchema(MA.Schema):
    product_category = MA.Nested(product_category_share_schema)
    user = MA.Nested(user_share_schema)

    class Meta:
        fields = (
            "id",
            "product_category_id",
            "user_id",
            "title",
            "product_code",
            "value",
            "brand",
            "template",
            "description",
        )


inventory_share_schema = InventorySchema()
inventories_share_schema = InventorySchema(many=True)
