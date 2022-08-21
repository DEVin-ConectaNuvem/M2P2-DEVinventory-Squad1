import json

from flask import Blueprint, abort, jsonify, request
from flask.wrappers import Response

from src.app import DB
from src.app.middlewares.auth import requires_access_level
from src.app.models.inventory import (Inventory, inventories_share_schema,
                                      inventory_share_schema)
from src.app.models.user import User
from src.app.services.inventory_service import (create_product,
                                                valida_valor_produto,
                                                verifica_existencia_produto)
from src.app.utils import exist_key, format_currency

inventory = Blueprint("inventory", __name__, url_prefix="/inventory")


@inventory.route("/", methods=["POST"])
@requires_access_level(["WRITE"])
def add_new_product():
    if not request.json:
        abort(400)

    list_keys = [
        "product_category_id",
        "user_id",
        "product_code",
        "title",
        "value",
        "brand",
        "template",
        "description",
    ]

    data = exist_key(request.get_json(), list_keys)
    if "error" in data:
        return jsonify(data), 400

    if verifica_existencia_produto(data["product_code"]):
        return jsonify({"message": "Produto já existente no banco de dados"}), 400

    if not valida_valor_produto(data["value"]):
        return jsonify({"message": "Valor inválido"}), 400

    if "error" in data:
        return jsonify(data), 400

    result = create_product(
        data["product_category_id"],
        data["user_id"],
        data["product_code"],
        data["title"],
        data["value"],
        data["brand"],
        data["template"],
        data["description"],
    )

    if "error" in result:
        return jsonify({"status": "Erro na criação do produto"}), 400
    else:
        return (
            jsonify({"status": "Produto criado com sucesso", "product": result}),
            201,
        )


@inventory.route("/", methods=["GET"])
@requires_access_level(["READ"])
def get_product_by_user_name():
    page = request.args.get("page", 1, type=int)
    per_page = 20

    if not request.args.get("name"):
        query = DB.session.query(Inventory).slice(
            (page - 1) * per_page, page * per_page
        )
        result = []
        for product in query:
            result.append(product.format())

        if not result:
            return jsonify({"Status": "Dados não encontrados"}), 204
        else:
            return jsonify({"Status": "Sucesso", "Dados": result}), 200
    else:
        query = (
            DB.session.query(Inventory)
            .join(User)
            .filter(User.name.ilike("%" + request.args.get("name") + "%"))
            .slice((page - 1) * per_page, page * per_page)
        )
        result = []
        for item in query:
            result.append(item.format())

        if not result:
            return jsonify({"Status": "Dados não encontrados"}), 204
        else:
            return jsonify({"Status": "Sucesso", "Dados": result}), 200


@inventory.route("/results", methods=["GET"])
@requires_access_level(["READ"])
def get_all_products():
    products = Inventory.query.all()
    users = User.query.all()

    resultado = {
        "numero de usuários": len(users),
        "quantidade de produtos": len(products),
        "valor total de itens": format_currency(
            sum([product.value for product in products])
        ),
        "itens emprestados": len(
            [
                product.user_id
                for product in products
                if product.user_id is not None or product.user_id == 0
            ]
        ),
    }

    return jsonify(resultado), 200


@inventory.route("/<int:id>", methods=["PATCH"])
@requires_access_level(["UPDATE"])
def update_product(id):
    if id is None or id == 0:
        abort(400)
    
    if not request.json:
        abort(400)
        
    fields_not_allowed = ["product_category_id", "product_code"]
    for field in fields_not_allowed:
        if field in request.json:
            return jsonify({"error": f"Campo {field} não pode ser alterado"}), 400
    
    for field in request.json:
        if field not in inventories_share_schema.fields:
            return jsonify({"error": f"Campo {field} não existe"}), 400
        if field == "value":
            if not valida_valor_produto(request.json[field]):
                return jsonify({"error": "Valor inválido"}), 400
        if field != "user_id":
            if request.json[field] is None or request.json[field] == 0 or request.json[field] == "":
                return jsonify({"error": f"O campo '{field} não pode ser nulo"}), 400

    product = Inventory.query.get(id)
    product.update(request.json)

    product = inventory_share_schema.dump(product)

    return jsonify({"status": "Produto atualizado com sucesso!", "Dados": product}), 204
