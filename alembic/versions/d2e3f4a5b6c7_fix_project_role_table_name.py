"""fix project role table name

Revision ID: d2e3f4a5b6c7
Revises: c1d2e3f4a5b6
Create Date: 2026-04-30 14:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'd2e3f4a5b6c7'
down_revision: Union[str, Sequence[str], None] = 'c1d2e3f4a5b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _create_project_role_table() -> None:
    op.create_table(
        'data_factory_project_role',
        sa.Column('id', sa.INT(), autoincrement=True, nullable=False, comment='主键id'),
        sa.Column('create_time', sa.DATETIME(), nullable=False, comment='创建时间'),
        sa.Column('update_time', sa.DATETIME(), nullable=False, comment='更新时间'),
        sa.Column('del_flag', sa.SMALLINT(), nullable=False, server_default='0', comment='0: 未删除 1: 已删除'),
        sa.Column('create_id', sa.INT(), nullable=False, comment='创建人id'),
        sa.Column('create_name', sa.String(20), nullable=False, comment='创建人'),
        sa.Column('update_id', sa.INT(), nullable=True, comment='更新人id'),
        sa.Column('update_name', sa.String(20), nullable=True, comment='更新人'),
        sa.Column('project_id', sa.INT(), nullable=False, comment='项目id'),
        sa.Column('project_role', sa.SMALLINT(), nullable=False, server_default='0', comment='0: 普通用户 1: 组长'),
        sa.Column('user_id', sa.INT(), nullable=False, comment='用户id'),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4',
    )


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    tables = inspect(bind).get_table_names()

    if 'data_factory_project_role' in tables:
        return

    if 'data_factory_role' in tables:
        op.rename_table('data_factory_role', 'data_factory_project_role')
        return

    _create_project_role_table()


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    tables = inspect(bind).get_table_names()

    if 'data_factory_project_role' in tables and 'data_factory_role' not in tables:
        op.rename_table('data_factory_project_role', 'data_factory_role')
