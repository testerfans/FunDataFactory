#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试环境配置脚本
"""

import os
from app.commons.settings.config import Config

def test_config():
    """测试配置"""
    print("=== 环境配置测试 ===")
    print(f"当前环境变量 ENV: {os.getenv('ENV', 'development')}")
    print(f"数据库主机: {Config.HOST}")
    print(f"数据库端口: {Config.PORT}")
    print(f"数据库用户: {Config.USER}")
    print(f"数据库名称: {Config.DBNAME}")
    print(f"生产模式: {Config.PRO}")
    print(f"数据库连接字符串: {Config.SQLALCHEMY_DATABASE_URI}")
    print("==================")

if __name__ == "__main__":
    test_config()
