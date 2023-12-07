# 插件管理
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import smtplib
from email.mime.text import MIMEText

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

# 邮箱配置
MAIL_SERVER = "smtp.163.com"
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_PORT = 465
# 你个人的邮箱
MAIL_USERNAME = "w2530622506@163.com"

# 刚刚获取到的授权码填在这里
# MAIL_PASSWORD = "embfclpflderdidf"

MAIL_PASSWORD = "TAKSLEWCAMCDWQGU"
# 你的邮箱名字可以和MAIL_USERNAME一样
MAIL_DEFAULT_SENDER = "w2530622506@163.com"


def init_exts(app):
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    mail.init_app(app=app)
