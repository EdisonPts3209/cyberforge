from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, moderator, admin, owner
    avatar = db.Column(db.String(200), default=None)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_owner(self):
        return self.role == 'owner'

    def is_admin(self):
        return self.role in ['admin', 'owner']

    def is_moderator(self):
        return self.role in ['moderator', 'admin', 'owner']