"""add like and collection tables

Revision ID: a1b2c3d4e5f6
Revises: 712dab49c09d
Create Date: 2026-04-28 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '712dab49c09d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 点赞表
    op.create_table('data_factory_cases_like',
        sa.Column('id', sa.INT(), autoincrement=True, nullable=False, comment='主键id'),
        sa.Column('create_time', sa.DATETIME(), nullable=False, comment='创建时间'),
        sa.Column('update_time', sa.DATETIME(), nullable=False, comment='更新时间'),
        sa.Column('del_flag', sa.SMALLINT(), nullable=False, server_default='0', comment='0: 未删除 1: 已删除'),
        sa.Column('create_id', sa.INT(), nullable=False, comment='创建人id'),
        sa.Column('create_name', sa.String(20), nullable=False, comment='创建人'),
        sa.Column('update_id', sa.INT(), nullable=True, comment='更新人id'),
        sa.Column('update_name', sa.String(20), nullable=True, comment='更新人'),
        sa.Column('cases_id', sa.INT(), nullable=False, comment='造数场景id'),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    # 收藏表
    op.create_table('data_factory_cases_collection',
        sa.Column('id', sa.INT(), autoincrement=True, nullable=False, comment='主键id'),
        sa.Column('create_time', sa.DATETIME(), nullable=False, comment='创建时间'),
        sa.Column('update_time', sa.DATETIME(), nullable=False, comment='更新时间'),
        sa.Column('del_flag', sa.SMALLINT(), nullable=False, server_default='0', comment='0: 未删除 1: 已删除'),
        sa.Column('create_id', sa.INT(), nullable=False, comment='创建人id'),
        sa.Column('create_name', sa.String(20), nullable=False, comment='创建人'),
        sa.Column('update_id', sa.INT(), nullable=True, comment='更新人id'),
        sa.Column('update_name', sa.String(20), nullable=True, comment='更新人'),
        sa.Column('cases_id', sa.INT(), nullable=False, comment='造数场景id'),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('data_factory_cases_collection')
    op.drop_table('data_factory_cases_like')
