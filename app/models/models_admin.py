from ..exts import db
from sqlalchemy import MetaData
class AdminUserModel(db.Model):
    __tablename__ = 'tb_adminuser'
    metadata = MetaData()
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(30))