def is_table_empty(query):
    if query == None:
        return True
    else:
        return False

# verificar se todas as chaves obrigatorias estão sendo enviadas
def exist_key(request_json,list_keys):
    keys_missing = []

    for key in list_keys:
        if key in request_json:
            continue
        else:
            keys_missing.append(key)
    if len(keys_missing) == 0:
        return request_json
    
    return {"error": f"Está faltando o item {keys_missing}"}
