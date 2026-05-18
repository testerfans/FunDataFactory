# -*- coding: utf-8 -*- 
# @Time : 2026/4/28
# @File : __init__.py

from app.models.settings import SystemSettings
from app.crud import BaseCrud


class SystemSettingsCrud(BaseCrud):
    model = SystemSettings
