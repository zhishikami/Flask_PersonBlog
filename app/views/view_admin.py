from flask import Blueprint, render_template, request, redirect, jsonify

from ..exts import mail
from ..models.models_admin import *
from ..models.models import *
from flask_mail import Message

admin = Blueprint('admin', __name__)

user_blueprint = Blueprint('user', __name__)

# 装饰器：登录验证
from functools import wraps


def login_required(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        # 判断是否判断
        user_id = request.cookies.get('user_id', None)
        if user_id:
            user = AdminUserModel.query.get(user_id)
            request.user = user

            return fn(*args, **kwargs)
        else:
            return redirect('/admin/login/')

    return inner


# 后台管理首页
@admin.route('/admin/')
@admin.route('/admin/index/')
@login_required
def index():
    user = request.user
    categrorys = CategoryModel.query.filter()
    articles = ArticleModel.query.filter()
    photos = PhotoModel.query.filter()
    return render_template('admin/index.html',
                           username=user.name,
                           categrorys=categrorys,
                           articles=articles,
                           photos=photos)


# 后台管理
@admin.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        userpwd = request.form.get('userpwd')

        user = AdminUserModel.query.filter_by(name=username,
                                              password=userpwd).first()
        if user:
            response = redirect('/admin/index/')
            response.set_cookie('user_id',
                                str(user.id),
                                max_age=7 * 24 * 3600)
            return response
        else:
            return 'Login Failed'


@admin.route('/admin/logout/')
def admin_logout():
    response = redirect('/admin/login/')
    response.delete_cookie('user_id')
    return response


# @admin.route("/register")
# def register():
#     # 验证用户提交的邮箱和验证码是否对应且正确
#     return render_template("register.html")


# bp.route: 如果没有指定methods参数，默认就是GET请求
# @admin.route("/captcha/email")
# def get_email_captcha():
#     # url传参数
#     # /captcha/emial?email=xxx@qq.com
#     email = request.args.get("email")
#     print(email)
#     # 6位，数字和字母的组成
#     source = string.digits * 6
#     captcha = random.sample(source, 6)
#     # 列表变成字符串
#     captcha = "".join(captcha)  # 965083
#     print(captcha)
#
#     # I/O 操作
#     message = Message(subject="菜鸡学安全", recipients=[email], body=f"您的验证码是:{captcha}")
#     mail.send(message)
#
#     # 使用数据库存储
#     email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
#     db.session.add(email_captcha)
#     db.session.commit()
#
#     # RESTful API，这是一个格式
#     # {code:200/400/500, message: "xxx", data: {}}
#
#     return jsonify({"code": 200, "message": "", "data": None})
#
#     # memcached 和redis 适合存储验证，这里扩展，这里暂用数据库来存储


@admin.route("/admin/mail/test")
def mail_test():
    # recipients是接收人，是一个数组可以给多人同时发送邮件
    message = Message(subject="菜鸡学安全1111", recipients=['w2530622506@163.com'], body="这是一条测试邮件！！！")
    mail.send(message)
    return "邮件发送成功"


# 用户注册路由
@admin.route('/admin/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('admin/register.html')  # 创建一个 register.html 模板用于注册表单
    elif request.method == 'POST':
        # 从表单中获取用户详细信息
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # 检查用户名或邮箱是否已经存在于数据库中
        existing_user = UserModel.query.filter_by(username=username).first()
        existing_email = UserModel.query.filter_by(email=email).first()

        if existing_user:
            return '用户名已存在，请选择不同的用户名。'
        elif existing_email:
            return '邮箱已存在，请使用不同的邮箱。'

        # 创建一个新的用户实例
        new_user = UserModel(username=username, password=password, email=email)

        try:
            # 将新用户添加到数据库中
            db.session.add(new_user)
            db.session.commit()
            return redirect('/admin/login/')  # 注册成功后重定向到登录页面
        except Exception as e:
            db.session.rollback()
            return f"错误：{e}。注册失败。"  # 处理注册失败情况

    return '无效请求'


# ------------------------分类管理----------------------------------
# 分类管理
@admin.route('/admin/category/')
@login_required
def admin_category():
    categrorys = CategoryModel.query.all()
    return render_template('admin/category.html',
                           username=request.user.name,
                           categrorys=categrorys
                           )


# 后台管理-添加分类
@admin.route('/admin/addcategory/', methods=['GET', 'POST'])
@login_required
def admin_addcategory():
    user = request.user
    if request.method == 'POST':
        # 添加分类
        name = request.form.get('name')
        describe = request.form.get('describe')

        category = CategoryModel()
        category.name = name
        category.describe = describe

        try:
            db.session.add(category)
            db.session.commit()
        except Exception as e:
            print('e:', e)
            db.session.rollback()
        # 刷新页面
        return redirect('/admin/category/')

    return '请求方式错误！'


# 后台管理-删除分类
@admin.route('/admin/delcategory/', methods=['GET', 'POST'])
@login_required
def admin_delcategory():
    user = request.user
    if request.method == 'POST':
        id = request.form.get('id')
        category = CategoryModel.query.get(id)
        # 删除
        try:
            db.session.delete(category)
            db.session.commit()
        except Exception as e:
            print('e', e)

        return jsonify({'code': 200, 'msg': '删除成功！'})
    else:
        return jsonify({'code': 400, 'msg': '请求方式错误！'})


# 后台管理-修改分类
@admin.route('/admin/updatecategory/<id>/', methods=['GET', 'POST'])
@login_required
def admin_updatecategory(id):
    if request.method == 'GET':
        category = CategoryModel.query.get(id)
        return render_template('admin/category_update.html',
                               username=request.user.name,
                               category=category)
    elif request.method == 'POST':
        name = request.form.get('name')
        describe = request.form.get('describe')

        # 修改
        category = CategoryModel.query.get(id)
        category.name = name
        category.describe = describe
        try:
            db.session.commit()
        except Exception as e:
            print('e', e)
        return redirect('/admin/category/')
    else:
        return '请求方式错误！'


# ----------------------文章管理-------------------------#
# 后台管理-文章管理
@admin.route('/admin/article/')
@login_required
def admin_article():
    articles = ArticleModel.query.all()
    return render_template('admin/article.html',
                           username=request.user.name,
                           articles=articles
                           )


# 后台管理-添加文章
@admin.route('/admin/addarticle/', methods=['GET', 'POST'])
@login_required
def admin_addarticle():
    if request.method == 'GET':

        categorys = CategoryModel.query.all()
        articles = ArticleModel.query.all()
        return render_template('admin/article_add.html',
                               username=request.user.name,
                               articles=articles,
                               categorys=categorys
                               )
    elif request.method == 'POST':
        # 添加文章
        name = request.form.get('name')
        keywords = request.form.get('keywords')
        content = request.form.get('content')
        category = request.form.get('category')
        img = request.files.get('img')
        # print('img', img)
        # print('img.filename', img.filename)

        # 图片存储路径
        img_name = f'{time.time()}-{img.filename}'
        img_url = f'/static/home/uploads/{img_name}'

        # 添加文章
        try:
            article = ArticleModel()
            article.name = name
            article.keyword = keywords
            article.content = content
            article.category_id = category
            article.img = img_url

            db.session.add(article)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            print('e:', e)
        else:
            # 如果数据库加入成功则，手动保存数据
            img_data = img.read()
            with open(f'app/{img_url}', 'wb') as fp:
                fp.write(img_data)
                fp.flush()

        return redirect('/admin/article/')


# 后台管理-修改文章
@admin.route('/admin/updatearticle/', methods=['GET', 'POST'])
@login_required
def admin_updatearticle():
    return render_template('admin/article_update.html',
                           username=request.user.name
                           )


# 后台管理-删除文章
@admin.route('/admin/delarticle/', methods=['GET', 'POST'])
@login_required
def admin_delarticle():
    if request.method == 'POST':
        id = request.form.get('id')
        article = ArticleModel.query.get(id)
        try:
            db.session.delete(article)
            db.session.commit()
        except Exception as e:
            print('e', e)
            return jsonify({'code': 500, 'msg': '删除失败！'})

        return jsonify({'code': 200, 'msg': '删除成功！'})

    return jsonify({'code': 400, 'msg': '请求方式错误！'})
