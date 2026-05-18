"""initial

Revision ID: 712dab49c09d
Revises: 
Create Date: 2026-04-28 17:31:39.404191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '712dab49c09d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 项目表
    op.create_table('data_factory_project',
        sa.Column('id', sa.INT(), autoincrement=True, nullable=False, comment='主键id'),
        sa.Column('create_time', sa.DATETIME(), nullable=False, comment='创建时间'),
        sa.Column('update_time', sa.DATETIME(), nullable=False, comment='更新时间'),
        sa.Column('del_flag', sa.SMALLINT(), nullable=False, server_default='0', comment='0: 未删除 1: 已删除'),
        sa.Column('create_id', sa.INT(), nullable=False, comment='创建人id'),
        sa.Column('create_name', sa.String(20), nullable=False, comment='创建人'),
        sa.Column('update_id', sa.INT(), nullable=True, comment='更新人id'),
        sa.Column('update_name', sa.String(20), nullable=True, comment='更新人'),
        sa.Column('project_name', sa.String(64), nullable=False, comment='项目名称'),
        sa.Column('description', sa.String(64), nullable=True, comment='项目描述'),
        sa.Column('directory', sa.String(64), nullable=False, comment='脚本目录'),
        sa.Column('owner', sa.String(64), nullable=False, comment='项目负责人'),
        sa.Column('private', sa.BOOLEAN(), nullable=False, server_default='0', comment='是否私有'),
        sa.Column('pull_type', sa.SMALLINT(), nullable=False, server_default='0', comment='拉取方式, 0: http 1: ssh'),
        sa.Column('git_project', sa.String(64), nullable=False, comment='git项目名'),
        sa.Column('git_url', sa.String(255), nullable=False, comment='git地址'),
        sa.Column('git_branch', sa.String(32), nullable=False, comment='git分支名'),
        sa.Column('git_account', sa.String(32), nullable=True, comment='git账号'),
        sa.Column('git_password', sa.String(64), nullable=True, comment='git密码'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id', 'git_url', 'project_name', 'del_flag'),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    # 用户表
    op.create_table('data_factory_user',
        sa.Column('id', sa.INT(), autoincrement=True, nullable=False, comment='主键id'),
        sa.Column('create_time', sa.DATETIME(), nullable=False, comment='创建时间'),
        sa.Column('update_time', sa.DATETIME(), nullable=False, comment='更新时间'),
        sa.Column('del_flag', sa.SMALLINT(), nullable=False, server_default='0', comment='0: 未删除 1: 已删除'),
        sa.Column('create_id', sa.INT(), nullable=False, comment='创建人id'),
        sa.Column('create_name', sa.String(20), nullable=False, comment='创建人'),
        sa.Column('update_id', sa.INT(), nullable=True, comment='更新人id'),
        sa.Column('update_name', sa.String(20), nullable=True, comment='更新人'),
        sa.Column('username', sa.String(20), nullable=False, comment='用户名'),
        sa.Column('password', sa.String(64), nullable=False, comment='密码'),
        sa.Column('name', sa.String(20), nullable=False, comment='真实姓名'),
        sa.Column('email', sa.String(32), nullable=False, comment='电子邮箱'),
        sa.Column('role', sa.SMALLINT(), nullable=False, server_default='0', comment='权限: 0普通 1组长 2超管'),
        sa.Column('is_valid', sa.BOOLEAN(), nullable=False, server_default='1', comment='是否有效'),
        sa.Column('last_login_time', sa.DATETIME(), nullable=True, comment='最后登录时间'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username', 'del_flag'),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    # 角色表
    op.create_table('data_factory_project_role',
        sa.Column('id', sa.INT(), autoincrement=True, nullable=False, comment='主键id'),
        sa.Column('create_time', sa.DATETIME(), nullable=False, comment='创建时间'),
        sa.Column('update_time', sa.DATETIME(), nullable=False, comment='更新时间'),
        sa.Column('del_flag', sa.SMALLINT(), nullable=False, server_default='0', comment='0: 未删除 1: 已删除'),
        sa.Column('create_id', sa.INT(), nullable=False, comment='创建人id'),
        sa.Column('create_name', sa.String(20), nullable=False, comment='创建人'),
        sa.Column('update_id', sa.INT(), nullable=True, comment='更新人id'),
        sa.Column('update_name', sa.String(20), nullable=True, comment='更新人'),
        sa.Column('project_id', sa.INT(), nullable=False, comment='项目id'),
        sa.Column('project_role', sa.SMALLINT(), nullable=False, comment='角色权限'),
        sa.Column('user_id', sa.INT(), nullable=False, comment='用户id'),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    # 脚本表
    op.create_table('data_factory_cases',
        sa.Column('id', sa.INT(), autoincrement=True, nullable=False, comment='主键id'),
        sa.Column('create_time', sa.DATETIME(), nullable=False, comment='创建时间'),
        sa.Column('update_time', sa.DATETIME(), nullable=False, comment='更新时间'),
        sa.Column('del_flag', sa.SMALLINT(), nullable=False, server_default='0', comment='0: 未删除 1: 已删除'),
        sa.Column('create_id', sa.INT(), nullable=False, comment='创建人id'),
        sa.Column('create_name', sa.String(20), nullable=False, comment='创建人'),
        sa.Column('update_id', sa.INT(), nullable=True, comment='更新人id'),
        sa.Column('update_name', sa.String(20), nullable=True, comment='更新人'),
        sa.Column('project_id', sa.INT(), nullable=False, comment='项目id'),
        sa.Column('title', sa.String(255), nullable=False, comment='标题'),
        sa.Column('name', sa.String(255), nullable=False, comment='方法名'),
        sa.Column('description', sa.String(512), nullable=False, comment='描述信息'),
        sa.Column('group_name', sa.String(255), nullable=False, comment='分组名'),
        sa.Column('header', sa.Text(), nullable=True, comment='请求头'),
        sa.Column('owner', sa.String(255), nullable=False, comment='负责人'),
        sa.Column('path', sa.String(255), nullable=False, comment='脚本路径'),
        sa.Column('param_in', sa.Text(), nullable=True, comment='请求参数'),
        sa.Column('param_out', sa.Text(), nullable=True, comment='返回参数'),
        sa.Column('example_param_in', sa.Text(), nullable=True, comment='请求示例'),
        sa.Column('example_param_out', sa.Text(), nullable=True, comment='返回示例'),
        sa.Column('manual_execution_time', sa.INT(), nullable=False, server_default='0', comment='手动执行时间（秒）'),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    # 脚本参数组合表
    op.create_table('data_factory_cases_params',
        sa.Column('id', sa.INT(), autoincrement=True, nullable=False, comment='主键id'),
        sa.Column('create_time', sa.DATETIME(), nullable=False, comment='创建时间'),
        sa.Column('update_time', sa.DATETIME(), nullable=False, comment='更新时间'),
        sa.Column('del_flag', sa.SMALLINT(), nullable=False, server_default='0', comment='0: 未删除 1: 已删除'),
        sa.Column('create_id', sa.INT(), nullable=False, comment='创建人id'),
        sa.Column('create_name', sa.String(20), nullable=False, comment='创建人'),
        sa.Column('update_id', sa.INT(), nullable=True, comment='更新人id'),
        sa.Column('update_name', sa.String(20), nullable=True, comment='更新人'),
        sa.Column('name', sa.String(64), nullable=False, comment='参数组合名称'),
        sa.Column('cases_id', sa.INT(), nullable=False, comment='场景id'),
        sa.Column('params', sa.Text(), nullable=False, comment='参数值'),
        sa.Column('out_id', sa.String(32), nullable=True, comment='对外暴露id'),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    # 运行日志表
    op.create_table('data_factory_run_log',
        sa.Column('id', sa.INT(), autoincrement=True, nullable=False, comment='主键id'),
        sa.Column('create_time', sa.DATETIME(), nullable=False, comment='创建时间'),
        sa.Column('update_time', sa.DATETIME(), nullable=False, comment='更新时间'),
        sa.Column('del_flag', sa.SMALLINT(), nullable=False, server_default='0', comment='0: 未删除 1: 已删除'),
        sa.Column('create_id', sa.INT(), nullable=False, comment='创建人id'),
        sa.Column('create_name', sa.String(20), nullable=False, comment='创建人'),
        sa.Column('update_id', sa.INT(), nullable=True, comment='更新人id'),
        sa.Column('update_name', sa.String(20), nullable=True, comment='更新人'),
        sa.Column('cases_id', sa.INT(), nullable=False, comment='场景id'),
        sa.Column('requests_id', sa.String(64), nullable=False, server_default='', comment='请求id'),
        sa.Column('project_id', sa.INT(), nullable=False, server_default='0', comment='项目id'),
        sa.Column('run_status', sa.SMALLINT(), nullable=False, comment='运行状态: 0成功 1异常 2失败'),
        sa.Column('run_param_in', sa.Text(), nullable=True, comment='实际入参'),
        sa.Column('run_param_out', sa.Text(), nullable=True, comment='实际出参'),
        sa.Column('run_log', sa.Text(), nullable=True, comment='运行日志'),
        sa.Column('call_type', sa.SMALLINT(), nullable=False, server_default='0', comment='调用类型: 0平台 1外链 2RPC'),
        sa.Column('cost', sa.String(20), nullable=True, comment='执行时长（秒）'),
        sa.Column('sys_type', sa.String(20), nullable=True, comment='系统类型: git/platform'),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('data_factory_run_log')
    op.drop_table('data_factory_cases_params')
    op.drop_table('data_factory_cases')
    op.drop_table('data_factory_project_role')
    op.drop_table('data_factory_user')
    op.drop_table('data_factory_project')
