import random
import string
from flask import jsonify
from flask_mail import Message
import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, EqualTo, DataRequired
from .models.models_admin import AdminUserModel, EmailCaptchaModel
from .exts import db, mail
# 后端校验,验证器
# 继承自wtfforms中的表单功能直接使用
class RegisterForm(FlaskForm):
    # 验证器validators
    email = wtforms.StringField(validators=[DataRequired(message='邮箱不能为空')])
    username = wtforms.StringField(validators=[DataRequired(message='用户名不能为空')])
    password = wtforms.StringField(validators=[DataRequired(message='密码不能为空')])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致，请重新输入！")])
    captcha = wtforms.StringField(validators=[DataRequired(message='验证码不能为空')])
    get_cap = wtforms.SubmitField('获取验证码')
    submit = wtforms.SubmitField('注册')


def validate_captcha(email, captcha):
    captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
    if not captcha_model:
        return False
    return True
 #生成验证码
def get_email_captcha(email):
    source = string.digits * 6
    captcha = random.sample(source, 6)
    captcha = "".join(captcha)
    message = Message(subject="验证邮箱", recipients=[email], body=f"您的验证码是:{captcha}")
    mail.send(message)
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return True
    # TODO 检查用户名或邮箱是否已经存在于数据库中
    # existing_user = UserModel.query.filter_by(username=username).first()
    # existing_email = UserModel.query.filter_by(email=email).first()