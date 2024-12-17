import jwt
from datetime import datetime, timedelta
from app.config import Config


class JWTHandler:
    def create_token(self, data):
        expiration = datetime.utcnow() + timedelta(hours=1)
        data["exp"] = expiration
        return jwt.encode(data, Config.SECRET_KEY, algorithm="HS256")

    def decode_token(self, token):
        try:
            return jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token.")
