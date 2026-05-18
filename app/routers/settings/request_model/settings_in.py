# -*- coding: utf-8 -*- 
# @Time : 2026/4/28
# @File : settings_in.py

from pydantic import BaseModel, Field
from typing import Optional


class UpdateSettingsBody(BaseModel):
    """更新系统设置请求体"""
    system_name: Optional[str] = Field(None, description="系统名称")
    login_background: Optional[str] = Field(None, description="登录页背景图路径")
    company_logo: Optional[str] = Field(None, description="公司Logo路径（侧边栏）")
    favicon: Optional[str] = Field(None, description="浏览器图标路径")
