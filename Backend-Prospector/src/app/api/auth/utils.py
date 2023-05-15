
# from flask_jwt_extended import current_user
def hash_password(password: str) -> str:
    return password + "hash"
