from app.models.models import User
from app.db import db


class UserRepository:
    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def create_user(self, username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user
