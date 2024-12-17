from app.repositories.user_repository import UserRepository
from app.utils.jwt_handler import JWTHandler
from werkzeug.security import check_password_hash, generate_password_hash


class AuthService:
    def __init__(self, user_repository: UserRepository, jwt_handler: JWTHandler):
        self.user_repository = user_repository
        self.jwt_handler = jwt_handler

    def register(self, username, password):
        existing_user = self.user_repository.get_user_by_username(username)
        if existing_user:
            raise ValueError("User already exists.")
        hashed_password = generate_password_hash(password)
        return self.user_repository.create_user(username, hashed_password)

    def login(self, username, password):
        user = self.user_repository.get_user_by_username(username)
        if not user or not check_password_hash(user.password, password):
            raise ValueError("Invalid credentials.")
        return self.jwt_handler.create_token(
            {"user_id": user.id, "username": user.username}
        )
