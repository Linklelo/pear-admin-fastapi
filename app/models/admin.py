import datetime
from sqlalchemy import Column, Integer, String, VARCHAR, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import declarative_base, relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

# 创建中间表
user_role = Table(
    "admin_user_role",  # 中间表名称
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    Column("user_id", Integer, ForeignKey("admin_user.id"), comment='用户编号'),  # 属性 外键
    Column("role_id", Integer, ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
)

class User(Base):
    __tablename__ = 'admin_user'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = Column(String(20), comment='用户名')
    realname =Column(String(20), comment='真实名字')
    password_hash = Column(String(128), comment='哈希密码')
    enable = Column(Integer, default=0, comment='启用')
    create_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='创建时间')
    role = relationship('Role', secondary=user_role, backref=backref('user'), lazy = 'dynamic')
    # power = relationship('Power',secondary="admin_user_role", backref=backref('user'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

# 创建中间表
role_power = Table(
    "admin_role_power",  # 中间表名称
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    Column("power_id", Integer, ForeignKey("admin_power.id"), comment='用户编号'),  # 属性 外键
    Column("role_id", Integer, ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
)

class Role(Base):
    __tablename__ = 'admin_role'
    id = Column(Integer, primary_key=True, comment='角色ID')
    name = Column(String(255), comment='角色名称')
    code = Column(String(255), comment='角色标识')
    enable = Column(Integer, comment='是否启用')
    remark = Column(String(255), comment='备注')
    details = Column(String(255), comment='详情')
    sort = Column(Integer, comment='排序')
    create_time = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')
    power = relationship('Power', secondary=role_power, backref=backref('role'))


class Power(Base):
    __tablename__ = 'admin_power'
    id = Column(Integer, primary_key=True, comment='权限编号')
    name = Column(String(255), comment='权限名称')
    type = Column(String(1), comment='权限类型')
    code = Column(String(30), comment='权限标识')
    url = Column(String(255), comment='权限路径')
    open_type = Column(String(10), comment='打开方式')
    parent_id = Column(Integer, comment='父类编号')
    icon = Column(String(128), comment='图标')
    sort = Column(Integer, comment='排序')
    create_time = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')
    enable = Column(Integer, comment='是否开启')


class AdminLog(Base):
    __tablename__ = 'admin_admin_log'
    id = Column(Integer, primary_key=True)
    method = Column(String(10))
    uid = Column(Integer)
    url = Column(String(255))
    desc = Column(Text)
    ip = Column(String(255))
    success = Column(Integer)
    user_agent = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)


class Photo(Base):
    __tablename__ = 'admin_photo'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    href = Column(String(255))
    mime = Column(VARCHAR(50), nullable=False)
    size = Column(VARCHAR(30), nullable=False)
    create_time = Column(DateTime, default=datetime.datetime.now)
