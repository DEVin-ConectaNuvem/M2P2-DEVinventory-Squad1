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
