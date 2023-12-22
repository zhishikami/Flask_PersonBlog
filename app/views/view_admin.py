import time

from ..forms import RegisterForm, get_email_captcha, validate_captcha
from flask import Blueprint, render_template, request, redirect, jsonify
from ..models import *

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

        user = AdminUserModel.query.filter_by(name=username).first()
        if user.check_password(userpwd):
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


# ---------------------------用户注册路由--------------------------------------#
@admin.route('/admin/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data

        if form.get_cap.data:
            print('获取验证码！')
            get_email_captcha(email)
        elif form.submit.data:
            print('注册！')
            captcha = form.captcha.data
            name = form.username.data
            password = form.password.data
            password_confirm = form.password_confirm.data
            email = form.email.data
            new_user = AdminUserModel(name=name, password=password, email=email)
            if not new_user.check_name(name):
                return '该用户名已被注册~注册失败~'
            if not new_user.check_email(email):
                return '该邮箱已被注册~注册失败~'
            if validate_captcha(email, captcha):
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect('/admin/login/')  # 注册成功后重定向到登录页面
                except Exception as e:
                    db.session.rollback()
                    return f"错误：{e}。注册失败。"  # 处理注册失败情况
            else:
                return '验证码错误~注册失败~'
    return render_template('admin/verify2.html',
                           form=form,
                           )


@admin.route('/admin/send_verification', methods=['POST'])
def send_verification():
    email = request.json.get('email')  # 获取传递过来的邮箱
    result = get_email_captcha(email)  # 调用发送验证码的函数

    if result:
        return '验证码已发送'
    else:
        return '验证码发送失败，请稍后重试'


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