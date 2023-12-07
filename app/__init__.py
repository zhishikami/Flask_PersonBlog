import pdb
from flask import Flask
from .views.views import blog
from .views.view_admin import admin
from .exts import init_exts


def create_app():
    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(blueprint=blog)  # 博客前端页面
    app.register_blueprint(blueprint=admin)  # 后台管理系统
    # 配置数据库
    db_url = 'sqlite:///new2_sqlite3.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SOLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化插件
    init_exts(app=app)
    return app
