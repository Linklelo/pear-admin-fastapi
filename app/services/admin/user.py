from marshmallow import fields, Schema
from sqlalchemy import and_
from sqlalchemy.sql import exists

from fastapi_sqlalchemy import db
from app.models.admin import User, Role
from sqlalchemy.orm.dynamic import AppenderQuery

# 用户models的序列化类
class UserSchema(Schema):
    id = fields.Integer()
    username = fields.Str()
    realname = fields.Str()
    enable = fields.Integer()
    create_at = fields.DateTime()
    update_at = fields.DateTime()


'''
获取用户的sqlalchemy对象
分页器
'''


def get_user_data(page, limit, filters):
    user = db.session.query(User).filter(and_(*[getattr(User, k).like(v) for k, v in filters.items()])).offset((page-1)*limit).limit(limit).all()
    count = db.session.query(User).count()
    return user, count


'''
获取用户的dict数据
分页器
'''


def get_user_data_dict(page, limit, filters):
    user, count = get_user_data(page, limit, filters)
    user_schema = UserSchema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    output = user_schema.dump(user)  # 生成可序列化对象
    return output, count


'''
通过名称获取用户
'''


def get_user_by_name(username):
    return db.session.query(User).filter_by(username=username).first()
    

def get_user_by_id(id):
    return db.session.query(User).filter_by(id=id).first()

# 判断用户是否存在
def is_user_exists(username):
    res = db.session.query(User).filter_by(username=username).count()
    return bool(res)


# 增加用户
def add_user(username, realName, password):
    user = User(username=username, realname=realName)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user.id


# 增加用户角色
def add_user_role(id, roles_list):
    user = db.session.query(User).filter_by(id=id).first()
    roles = db.session.query(Role).filter(Role.id.in_(roles_list)).all()
    for r in roles:
        user.role.append(r)
    db.session.commit()


# 更新用户信息
def update_user(id, username, realname):
    user = db.session.query(User).filter_by(id=id).update({'username': username, 'realname': realname})
    db.session.commit()
    return user


def delete_by_id(id):
    user = db.session.query(User).filter_by(id=id).first()
    roles_id = []
    for role in user.role:
        roles_id.append(role.id)
    roles = db.session.query(Role).filter(Role.id.in_(roles_id)).all()
    for r in roles:
        user.role.remove(r)
    res = db.session.query(User).filter_by(id=id).delete()
    db.session.commit()
    return res


# 启动用户
def enable_status(id):
    enable = 1
    user = db.session.query(User).filter_by(id=id).update({"enable": enable})
    if user:
        db.session.commit()
        return True
    return False


# 停用用户
def disable_status(id):
    enable = 0
    user = db.session.query(User).filter_by(id=id).update({"enable": enable})
    if user:
        db.session.commit()
        return True
    return False


# 批量删除
def batch_remove(ids):
    for id in ids:
        delete_by_id(id)


def update_user_role(id, roles_list):
    user = db.session.query(User).filter_by(id=id).first()
    roles_id = []
    for role in user.role:
        roles_id.append(role.id)
    roles = db.session.query(Role).filter(Role.id.in_(roles_id)).all()
    for r in roles:
        user.role.remove(r)
    roles = db.session.query(Role).filter(Role.id.in_(roles_list)).all()
    for r in roles:
        user.role.append(r)
    db.session.commit()
