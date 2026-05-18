# -*- coding: utf-8 -*- 
# @Time : 2026/4/28
# @File : settings.py

from datetime import datetime
from sqlalchemy import Column, String, INT, DATETIME, Text
from app.models import Base


class SystemSettings(Base):
    __tablename__ = "data_factory_system_settings"

    id = Column(INT, primary_key=True, comment="主键id")
    setting_key = Column(String(64), unique=True, nullable=False, comment="设置键")
    setting_value = Column(Text, nullable=True, comment="设置值")
    description = Column(String(255), nullable=True, comment="描述")
    create_time = Column(DATETIME, nullable=False, comment="创建时间")
    update_time = Column(DATETIME, nullable=False, comment="更新时间")

    def __init__(self, setting_key: str, setting_value: str = None, description: str = None):
        self.setting_key = setting_key
        self.setting_value = setting_value
        self.description = description
        self.create_time = datetime.now()
        self.update_time = datetime.now()
