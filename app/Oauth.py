from datetime import datetime, timedelta
from jose import JWTError, jwt

Secret_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

Algorithm = "HS256"

Token_Expiration = 60


def AccessToken(data: dict):
    encode = data.copy()

    expiration = datetime.now() + timedelta(minutes=Token_Expiration)
    encode.update({"exp": expiration})

    encoded_jwt = jwt.encode(encode, Secret_key, algorithm=Algorithm)

    return encoded_jwt
