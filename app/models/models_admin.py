from werkzeug.security import generate_password_hash, check_password_hash
from ..exts import db
from sqlalchemy import MetaData


class AdminUserModel(db.Model):
    __tablename__ = 'tb_adminuser'
    metadata = MetaData()
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100), nullable=False)
    password_confirm=db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name, password, email):
        self.name = name
        self.password = generate_password_hash(password)  # 对密码进行哈希加密存储

        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password, password)  # 验证密码是否匹配哈希值

    def check_name(self, name):
        existing_user = AdminUserModel.query.filter_by(name=name).first()
        return existing_user is None

    def check_email(self, email):
        existing_email = AdminUserModel.query.filter_by(email=email).first()
        return existing_email is None


class EmailCaptchaModel(db.Model):
    __tablename__ = "eamil_captcha"
    metadata = MetaData()
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
