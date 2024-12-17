from flask import Blueprint
from app.controller.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/register', methods=['POST'])(AuthController.register)
auth_bp.route('/login', methods=['POST'])(AuthController.login)
