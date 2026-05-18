# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 00:00 
# @Author : junjie
# @File : main.py

from app import fun, init_logging, register_routers
from app.logic.project_logic.project_logic import start_init_project_logic
from loguru import logger


@fun.on_event('startup')
async def startup_event():
    """项目启动时，要做的事情"""
    # 注意：中间件和异常处理器已在 app/__init__.py 模块级注册
    #       新版 Starlette 不允许在 lifespan 中添加中间件

    # step1 初始化项目日志器
    init_logging()
    logger.info('logging is init success！！！')

    # step2 注册路由
    await register_routers(fun)
    logger.info('routers is register success！！！')

    # step3 执行数据库迁移（替代 create_all）
    from alembic.config import Config as AlembicConfig
    from alembic import command
    from pathlib import Path
    alembic_cfg = AlembicConfig(str(Path(__file__).parent / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")
    logger.info('db migration is success！！！')

    # step4 初始化项目
    start_init_project_logic()
    logger.info('project is init success！！！')

    logger.info('FunDataFactory is start success！！！')