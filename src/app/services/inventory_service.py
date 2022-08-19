from src.app.models.inventory import Inventory


def create_product(product_category_id, user_id,product_code, title, value, brand, template, description):
    try:
        inventory = Inventory.seed(
            product_category_id=product_category_id,
            user_id=user_id,
            product_code=product_code,
            title=title,
            value=value,
            brand=brand,
            template=template,
            description=description)
        

        return {'message': 'Produto criado com sucesso'}
    
    except Exception as e:
        return {'error': str(e)}

    
def verifica_existencia_produto(product_code):
    try:
        inventory = Inventory.query.filter_by(product_code=product_code).first()
        if inventory:
            return True
        else:
            return False
    except Exception as e:
        return {'error': str(e)}
    
def valida_valor_produto(value):
    if value < 0:
        return False
    else:
        return True