from src.app.models.inventory import Inventory, inventory_share_schema
from src.app.models.schemas.inventory_schema import inventory_create_schema


def create_product(data):
    try:
        inventory_create_schema.load(data)
        inventory = Inventory.seed(data)
        result = inventory_share_schema.dump(inventory)
        return result
    except Exception as e:
        return {"error": f"{e}", "status_code": 500}


def update_product(data, id):
    fields_not_allowed = ["id", "product_code", "product_category_id"]

    product = Inventory.query.get(id)

    if not product:
        return {"error": "Produto não encontrado", "status_code": 404}

    for field in fields_not_allowed:
        if field in data:
            return {
                "error": f"Campo '{field}' não permite alteração",
                "status_code": 400,
            }

    try:
        inventory_create_schema.load(data, partial=True)
        product.update(data)
        result = inventory_share_schema.dump(product)
        return result
    except Exception as e:
        return {"error": f"{e}", "status_code": 500}
