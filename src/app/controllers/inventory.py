import json

from flask import Blueprint, abort, jsonify, request
from flask.wrappers import Response

from src.app import DB
from src.app.models.inventory import (Inventory, inventories_share_schema,
                                      inventory_share_schema)
from src.app.models.user import User
from src.app.services.inventory_service import (create_product,
                                                valida_valor_produto,
                                                verifica_existencia_produto)
from src.app.utils import exist_key, format_currency

inventory = Blueprint('inventory', __name__, url_prefix="/inventory")

@inventory.route('/create', methods = ["POST"])
def add_new_product():
  if not request.json:
        abort(400)
        
  list_keys = ["product_category_id", "user_id", 'product_code', "title", "value", "brand", "template", "description"]

  data = exist_key(request.get_json(), list_keys)
  
  if verifica_existencia_produto(data['product_code']):
    return Response(
      response=json.dumps({"error": 'Produto já existe'}),
      status=400,
      mimetype='application/json'
  )
  
  if not valida_valor_produto(data['value']):
    return Response(
      response=json.dumps({"error": 'Valor inválido, o valor deve ser maior que 0'}),
      status=400,
      mimetype='application/json'
  )
  
  if "error" in data:
    return jsonify(data), 400
  
  produto = create_product(
              data['product_category_id'],
              data['user_id'],
              data['product_code'],
              data['title'],
              data['value'],
              data['brand'],
              data['template'],
              data['description']   
  )

  if "error" in produto:
   return Response(
      response=json.dumps({"error": produto['error']}),
      status=401,
      mimetype='application/json'
    )
  else:
    return Response(
      response=json.dumps({"error": False, "message": "Produto criado com sucesso"}),
      status=200,
      mimetype='application/json'
    )
  
  
@inventory.route('/', methods = ["GET"])
def get_product_by_user_name():
  page =  request.args.get('page', 1, type=int)
  per_page =  20
  
  if not request.args.get('name'):
    query = DB.session.query(Inventory).slice((page-1)*per_page, page*per_page)
    result = []
    for product in query:
        result.append(product.format())
    
    if not result:
      return jsonify({"Status":"Dados não encontrados"}), 204
    else:
      return jsonify({"Status":"Sucesso", "Dados": result}), 200
  else:
    query = DB.session.query(Inventory).join(User).filter(User.name.ilike('%' + request.args.get('name') + '%')).slice((page-1)*per_page, page*per_page)
    result = []
    for item in query:
      result.append(item.format())
    
    if not result:
      return jsonify({"Status":"Dados não encontrados"}), 204
    else:
      return jsonify({"Status":"Sucesso", "Dados": result}), 200


@inventory.route('/results', methods = ["GET"])
def get_all_products():
  products = Inventory.query.all()
  users = User.query.all()
  
  resultado = {
      'numero de usuários': len(users),
      'quantidade de produtos': len(products),
      'valor total de itens': format_currency(sum([product.value for product in products])),
      'itens emprestados': len([product.user_id for product in products if product.user_id is not None or product.user_id != 0])}
  
  return Response(
    response=json.dumps(resultado),
    status=200,
    mimetype='application/json'
  )

@inventory.route('/', methods = ["PATCH"])
def update_product():
    fields_not_allowed = ['product_category_id', 'product_code']
    
    for field in fields_not_allowed:
      if field in request.json:
        return Response(
          response=json.dumps({"error": 'Campo ' + field + ' não pode ser alterado'}),
          status=400,
          mimetype='application/json'
        )
    
    if not request.args.get('id'):
        return Response(
          response=json.dumps({"error": 'ID do produto não informado'}),
          status=400,
          mimetype='application/json'
      )
    
    id = request.args.get('id')
    
    product = Inventory.query.get(id)
    product.update(request.json)
    
    product = inventory_share_schema.dump(product)
    
    return Response(
      response=json.dumps({"error": False, 
                           "message": "Produto atualizado com sucesso",
                           'dados': product
                           }),
      status=204,
      mimetype='application/json'
    )