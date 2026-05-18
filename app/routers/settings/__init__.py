# -*- coding: utf-8 -*- 
# @Time : 2026/4/28
# @File : __init__.py

from fastapi import APIRouter
from app.commons.responses.response_model import ResponseDto
from app.routers.settings.apis import settings_api

router = APIRouter()

router.add_api_route("/public/settings",
                     settings_api.get_system_settings,
                     methods=["get"],
                     name="获取系统设置",
                     description="获取系统设置（公开接口）",
                     response_model=ResponseDto)

router.add_api_route("/settings",
                     settings_api.update_system_settings,
                     methods=["put"],
                     name="更新系统设置",
                     description="更新系统设置（需要管理员权限）",
                     response_model=ResponseDto)

router.add_api_route("/upload",
                     settings_api.upload_setting_image,
                     methods=["post"],
                     name="上传设置图片",
                     description="上传系统设置图片",
                     response_model=ResponseDto)

router.add_api_route("/upload/validate",
                     settings_api.validate_upload_image,
                     methods=["post"],
                     name="验证上传图片",
                     description="上传前验证图片尺寸和格式",
                     response_model=ResponseDto)
