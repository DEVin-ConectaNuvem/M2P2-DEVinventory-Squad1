    
def set_error_message(field):
    error_messages = {
        "required": f"{field} é obrigatório.",
        "invalid": f"{field} inválido.",
        "exists": f"{field} não encontrado.",
        "unknown": f"{field} não encontrado.",
        "unique": f"{field} já registrado.",
        "type": f"tipo do campo {field} é inválido.",
        "value": f"valor do campo {field} é inválido."
    }
    
    return error_messages