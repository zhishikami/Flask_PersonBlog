from ..exts import db
from sqlalchemy import MetaData
# 分类：文章 = 1： N

# 分类
class CategoryModel(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    describe = db.Column(db.Text(), default='describe')
    # 所有文章
    aticles = db.relationship('ArticleModel', backref='category', lazy='dynamic')


# 文章
class ArticleModel(db.Model):
    __tablename__ = 'tb_article'
    metadata = MetaData()
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    keyword = db.Column(db.String(255), default='keyword')
    content = db.Column(db.Text(), default='content')
    img = db.Column(db.Text(), default='img')
    # 所属外键
    category_id = db.Column(db.Integer, db.ForeignKey(CategoryModel.id))


class PhotoModel(db.Model):
    __tablename__ = 'tb_photo'
    metadata = MetaData()
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text())
    name = db.Column(db.String(30), unique=True)
    describe = db.Column(db.Text(), default='describe')
