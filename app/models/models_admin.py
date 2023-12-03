from werkzeug.security import generate_password_hash, check_password_hash

from ..exts import db
from sqlalchemy import MetaData


class AdminUserModel(db.Model):
    __tablename__ = 'tb_adminuser'
    metadata = MetaData()
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = generate_password_hash(password)  # 对密码进行哈希加密存储
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password, password)  # 验证密码是否匹配哈希值
