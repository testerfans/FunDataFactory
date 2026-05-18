# -*- coding: utf-8 -*- 
# @Time : 2026/4/28
# @File : settings_logic.py

from app.crud.settings import SystemSettingsCrud
from app.commons.exceptions.global_exception import BusinessException
from app.models.settings import SystemSettings
from sqlalchemy import update as sql_update
from app.models import Session, engine

# 默认系统设置
DEFAULT_SETTINGS = {
    "system_name": {
        "value": "数据构造平台",
        "description": "系统名称，显示在登录页和浏览器标题"
    },
    "login_background": {
        "value": "/static/logincover.png",
        "description": "登录页背景图片路径"
    },
    "company_logo": {
        "value": "",
        "description": "公司Logo图片路径（侧边栏显示，空则使用默认图标）"
    },
    "favicon": {
        "value": "",
        "description": "浏览器图标路径（空则使用默认图标）"
    }
}


class SystemSettingsLogic:

    @staticmethod
    def init_default_settings():
        """初始化默认系统设置（如果不存在则创建）"""
        # 兼容旧版：将 logo_image 迁移为 company_logo
        try:
            from sqlalchemy import text
            with Session() as session:
                # 检查是否存在旧的 logo_image 记录
                old = session.execute(text(
                    "SELECT id, setting_value FROM data_factory_system_settings WHERE setting_key='logo_image'"
                )).fetchone()
                if old:
                    old_id, old_value = old[0], old[1]
                    # 检查 company_logo 是否已存在
                    existing = session.execute(text(
                        "SELECT id FROM data_factory_system_settings WHERE setting_key='company_logo'"
                    )).fetchone()
                    if existing:
                        # company_logo 已存在：合并值（旧值非空则更新）
                        if old_value:
                            session.execute(text(
                                "UPDATE data_factory_system_settings SET setting_value=:val "
                                "WHERE setting_key='company_logo'"
                            ), {"val": old_value})
                        # 删除旧的 logo_image 行
                        session.execute(text(
                            "DELETE FROM data_factory_system_settings WHERE setting_key='logo_image'"
                        ))
                    else:
                        # company_logo 不存在：直接重命名
                        session.execute(text(
                            "UPDATE data_factory_system_settings SET setting_key='company_logo', "
                            "description='公司Logo图片路径（侧边栏显示，空则使用默认图标）' "
                            "WHERE id=:id"
                        ), {"id": old_id})
                    session.commit()
        except Exception:
            pass  # 迁移失败不影响启动

        for key, config in DEFAULT_SETTINGS.items():
            existing = SystemSettingsCrud.get_with_existed(setting_key=key)
            if not existing:
                setting = SystemSettings(
                    setting_key=key,
                    setting_value=config["value"],
                    description=config["description"]
                )
                SystemSettingsCrud.insert_by_model(model_obj=setting)

    @staticmethod
    def get_all_settings() -> dict:
        """获取所有系统设置，返回字典"""
        SystemSettingsLogic.init_default_settings()
        settings_list = SystemSettingsCrud.get_with_params()
        result = {}
        for s in settings_list:
            result[s.setting_key] = {
                "id": s.id,
                "value": s.setting_value,
                "description": s.description
            }
        # 确保所有默认key都存在
        for key, config in DEFAULT_SETTINGS.items():
            if key not in result:
                result[key] = {
                    "id": None,
                    "value": config["value"],
                    "description": config["description"]
                }
        return result

    @staticmethod
    def update_settings(settings_dict: dict, user: dict = None) -> dict:
        """批量更新系统设置"""
        for key, value in settings_dict.items():
            existing = SystemSettingsCrud.get_with_first(setting_key=key)
            if existing:
                # 更新现有记录
                SystemSettingsCrud.update_by_id(
                    model={"id": existing.id, "setting_value": str(value)},
                    user=user
                )
            else:
                # 创建新记录
                new_setting = SystemSettings(
                    setting_key=key,
                    setting_value=str(value),
                    description=DEFAULT_SETTINGS.get(key, {}).get("description", "")
                )
                SystemSettingsCrud.insert_by_model(model_obj=new_setting)
        return SystemSettingsLogic.get_all_settings()


system_settings_logic = SystemSettingsLogic()
