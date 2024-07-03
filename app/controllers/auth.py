import bcrypt

def hash_password(password: str) -> str:
    enocoded_password = password.encode()
    hashed_password = bcrypt.hashpw(password=enocoded_password, salt= bcrypt.gensalt())
    return hashed_password.decode()

def check_password(password : str, hashed_password : str)-> bool:
    is_password_true = bcrypt.checkpw(password, hashed_password)
    return is_password_true




