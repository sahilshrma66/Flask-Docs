from flask import jsonify, request
from app.services.auth_services import AuthService
from app.repositories.user_repository import UserRepository
from app.utils.jwt_handler import JWTHandler

user_repository = UserRepository()
jwt_handler = JWTHandler()
auth_service = AuthService(user_repository, jwt_handler)


class AuthController:
    @staticmethod
    def register():
        data = request.get_json()
        try:
            user = auth_service.register(data["username"], data["password"])
            return jsonify({"message": "User registered successfully", "user": {"id": user.id, "username": user.username}})
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def login():
        data = request.get_json()
        try:
            token = auth_service.login(data["username"], data["password"])
            return jsonify({"token": token})
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
