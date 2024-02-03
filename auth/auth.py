from fastapi import HTTPException
from jose import jwt, JWTError
from model.user_connection import UserConnection

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def authenticate_user(db: UserConnection, username: str, password: str):
    user = db.authenticate_user(username, password)
    print("User from authenticate_user:", user)
    
    if user and user[5] == password:  # Ajustar el índice según la posición de la contraseña en tu tupla
        token_data = {"sub": user[0]}
        token = create_jwt_token(token_data)
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
