# -*- coding: utf-8 -*- 
# @Time : 2026/4/28
# @File : settings_api.py

from app.logic.settings_logic.settings_logic import system_settings_logic
from app.commons.responses.response_model import ResponseDto
from app.routers.settings.request_model.settings_in import UpdateSettingsBody
import os
import uuid
from fastapi import UploadFile, File
from PIL import Image
from io import BytesIO

# 图片约束
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
LOGIN_BG_MIN_WIDTH = 1280
LOGIN_BG_MIN_HEIGHT = 720
LOGO_MAX_WIDTH = 400
LOGO_MAX_HEIGHT = 80
ALLOWED_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/webp"]
ALLOWED_LOGO_TYPES = ["image/png", "image/svg+xml"]
ALLOWED_FAVICON_TYPES = ["image/png", "image/svg+xml", "image/x-icon", "image/vnd.microsoft.icon"]


def get_system_settings():
    """获取系统设置（公开接口，无需登录）"""
    settings = system_settings_logic.get_all_settings()
    return ResponseDto(data=settings)


def update_system_settings(body: UpdateSettingsBody):
    """更新系统设置（需要管理员权限）"""
    update_dict = {}
    if body.system_name is not None:
        update_dict["system_name"] = body.system_name
    if body.login_background is not None:
        update_dict["login_background"] = body.login_background
    if body.company_logo is not None:
        update_dict["company_logo"] = body.company_logo
    if body.favicon is not None:
        update_dict["favicon"] = body.favicon
    
    if not update_dict:
        return ResponseDto(msg="没有需要更新的设置")
    
    settings = system_settings_logic.update_settings(update_dict)
    return ResponseDto(data=settings, msg="设置更新成功")


def _validate_image_dimensions(file_data: bytes, img_type: str):
    """验证图片尺寸是否符合要求"""
    try:
        img = Image.open(BytesIO(file_data))
        width, height = img.size
        if img_type == "login_background":
            if width < LOGIN_BG_MIN_WIDTH or height < LOGIN_BG_MIN_HEIGHT:
                return False, f"登录背景图尺寸至少 {LOGIN_BG_MIN_WIDTH}×{LOGIN_BG_MIN_HEIGHT}，当前 {width}×{height}"
        elif img_type == "company_logo":
            if width > LOGO_MAX_WIDTH or height > LOGO_MAX_HEIGHT:
                return False, f"公司Logo尺寸不超过 {LOGO_MAX_WIDTH}×{LOGO_MAX_HEIGHT}，当前 {width}×{height}"
        return True, ""
    except Exception:
        return False, "无法解析图片尺寸，请确认文件为有效图片"


def upload_setting_image(file: UploadFile = File(...)):
    """上传系统设置图片（登录背景/公司Logo）"""
    # 检查文件大小
    file_data = file.file.read()
    if len(file_data) > MAX_FILE_SIZE:
        return ResponseDto(code=400, msg=f"图片大小不能超过 5MB，当前 {len(file_data) / 1024 / 1024:.1f}MB")
    
    # 检查文件类型
    if file.content_type not in ALLOWED_TYPES + ALLOWED_LOGO_TYPES + ALLOWED_FAVICON_TYPES:
        return ResponseDto(code=400, msg="不支持的文件类型，登录背景仅支持 PNG/JPG/WebP，Logo 支持 PNG/SVG，图标支持 ICO/PNG/SVG")
    
    # 生成唯一文件名
    ext = os.path.splitext(file.filename)[1] if file.filename else ".png"
    unique_name = f"{uuid.uuid4().hex}{ext}"
    
    # 保存到 uploads 目录
    from pathlib import Path
    uploads_dir = Path(__file__).parent.parent.parent.parent.parent / "uploads"
    uploads_dir.mkdir(exist_ok=True)
    
    file_path = uploads_dir / unique_name
    with open(file_path, "wb") as f:
        f.write(file_data)
    
    url = f"/uploads/{unique_name}"
    return ResponseDto(data={"url": url}, msg="上传成功")


def validate_upload_image(file: UploadFile = File(...), img_type: str = ""):
    """上传前验证图片尺寸（前端调用此接口预检）"""
    file_data = file.file.read()
    if len(file_data) > MAX_FILE_SIZE:
        return ResponseDto(code=400, msg=f"图片大小不能超过 5MB")
    
    if img_type == "login_background":
        allowed = ALLOWED_TYPES
    elif img_type == "company_logo":
        allowed = ALLOWED_LOGO_TYPES
    elif img_type == "favicon":
        allowed = ALLOWED_FAVICON_TYPES
    else:
        allowed = ALLOWED_TYPES + ALLOWED_LOGO_TYPES + ALLOWED_FAVICON_TYPES
    
    if file.content_type not in allowed:
        return ResponseDto(code=400, msg=f"不支持的文件类型 {file.content_type}")
    
    valid, msg = _validate_image_dimensions(file_data, img_type)
    if not valid:
        return ResponseDto(code=400, msg=msg)
    
    return ResponseDto(data={"valid": True}, msg="图片验证通过")
