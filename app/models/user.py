# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 16:16 
# @Author : junjie
# @File : user.py

from datetime import datetime
from sqlalchemy import Column, String, INT, DATETIME, SMALLINT, func, Boolean
from app.models import Base
from app.const.enums import PermissionEnum
from app.routers.user.request_model.user_in import RegisterUserBody

class DataFactoryUser(Base):
    __tablename__ = "data_factory_user"

    id = Column(INT, primary_key=True, autoincrement=True, comment="主键id")
    create_time = Column(DATETIME, nullable=False, comment="创建时间")
    update_time = Column(DATETIME, onupdate=func.now(), nullable=False, comment="更新时间")
    del_flag = Column(SMALLINT, default=0, nullable=False, comment="0: 未删除 1: 已删除")
    create_id = Column(INT, nullable=False, default=0, comment="创建人id")
    create_name = Column(String(20), nullable=False, default='', comment="创建人")
    update_id = Column(INT, nullable=True, comment="更新人id")
    update_name = Column(String(20), nullable=True, comment="更新人")
    username = Column(String(20), nullable=False, comment="用户名")
    password = Column(String(64), nullable=False, comment="密码(md5加密)")
    name = Column(String(20), nullable=False, comment="姓名")
    email = Column(String(32), nullable=False, comment="邮箱号")
    role = Column(SMALLINT, default=0, nullable=False, comment="0: 普通用户 1: 组长 2: 超管")
    is_valid = Column(Boolean, nullable=False, default=True, comment="是否有效")
    last_login_time = Column(DATETIME, nullable=True, comment="上次登录时间")

    def __init__(self, form: RegisterUserBody, **kwargs):
        super().__init__(**kwargs)
        self.username = form.username
        self.name = form.name
        self.password = form.password
        self.email = form.email
        self.role = form.role.value if hasattr(form, 'role') and form.role is not None else PermissionEnum.members.value
        self.is_valid = True
        self.del_flag = 0
        self.create_time = datetime.now()
        self.update_time = datetime.now()
        self.last_login_time = datetime.now()
        self.create_id = 0
        self.create_name = form.name or ''
