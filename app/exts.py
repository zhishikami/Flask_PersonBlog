# 插件管理
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import moment
from flask_mail import Mail
from sqlalchemy import MetaData
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

# class EmailCaptchaModel(db.Model):
#     # metadata = MetaData()
#     __tablename__ = "eamil_captcha"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     email = db.Column(db.String(100), nullable=False)
#     captcha = db.Column(db.String(100), nullable=False)
# class AdminUserModel(db.Model):
#     __tablename__ = 'tb_adminuser'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(30), unique=True)
#     password = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#
#     def __init__(self, username, password, email):
#         self.username = username
#         self.password = generate_password_hash(password)  # 对密码进行哈希加密存储
#         self.email = email
#
#     def check_password(self, password):
#         return check_password_hash(self.password, password)  # 验证密码是否匹配哈希值
#
#
#
#
# class CategoryModel(db.Model):
#     __tablename__ = 'category'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(30), unique=True)
#     describe = db.Column(db.Text(), default='describe')
#     # 所有文章
#     aticles = db.relationship('ArticleModel', backref='category', lazy='dynamic')
#
#
# # 文章
# class ArticleModel(db.Model):
#     __tablename__ = 'tb_article'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(30), unique=True)
#     keyword = db.Column(db.String(255), default='keyword')
#     content = db.Column(db.Text(), default='content')
#     img = db.Column(db.Text(), default='img')
#     # 所属外键
#     category_id = db.Column(db.Integer, db.ForeignKey(CategoryModel.id))
#
#
# class PhotoModel(db.Model):
#     __tablename__ = 'tb_photo'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     url = db.Column(db.Text())
#     name = db.Column(db.String(30), unique=True)
#     describe = db.Column(db.Text(), default='describe')






# --------------------------------------------------------------------------------#
def init_exts(app):
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    mail.init_app(app=app)
    Bootstrap(app)
    moment(app)
