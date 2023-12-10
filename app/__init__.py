import pdb
import os
from flask import Flask
from .views.views import blog
from .views.view_admin import admin
from .exts import init_exts
from app.models.models_admin import *
from app.models.models import *

def create_app():
    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(blueprint=blog)  # 博客前端页面
    app.register_blueprint(blueprint=admin)  # 后台管理系统
    # 配置数据库
    db_url = 'sqlite:///data.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SOLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 配置邮箱
    app.config['MAIL_SERVER'] = "smtp.qq.com"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = "2047639647@qq.com"
    app.config['MAIL_PASSWORD'] = "pxftlvadoezpeedg"
    app.config['MAIL_DEFAULT_SENDER'] = "2047639647@qq.com"

    #配置表单
    app.config['SECRET_KEY'] = 'your_secret_key'

    # 初始化插件
    init_exts(app=app)
    return app
