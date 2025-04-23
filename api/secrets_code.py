import secrets

def create_code():
    code = secrets.token_hex(8)
    return code

