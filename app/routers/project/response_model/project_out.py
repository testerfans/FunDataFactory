# -*- coding: utf-8 -*- 
# @Time : 2022/8/8 22:01 
# @Author : junjie
# @File : project_out.py
from app.commons.responses.response_model import BaseDto
from datetime import datetime
from typing import Optional
from pydantic import Field


class ProjectSyncDto(BaseDto):
    id: int
    project_name: str

class ProjectListDto(ProjectSyncDto):
    description: Optional[str] = None
    owner: str
    update_time: datetime


class ProjectDetailDto(ProjectListDto):
    directory: str
    private: bool
    pull_type: int
    git_project: str
    git_url: str
    git_branch: str
    git_account: Optional[str] = Field(default=None)
    git_password: Optional[str] = Field(default=None)
    rsa_pub_key: Optional[str] = Field(default=None)


class RoleDto(BaseDto):
    id: int
    username: str
    name: str
    email: str
    project_role: int
    project_id: int
    user_id: int
    create_name: str
    create_time: datetime
