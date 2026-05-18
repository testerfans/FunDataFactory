"""add system settings table

Revision ID: c1d2e3f4a5b6
Revises: a1b2c3d4e5f6
Create Date: 2026-04-28 21:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1d2e3f4a5b6'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('data_factory_system_settings',
        sa.Column('id', sa.INT(), autoincrement=True, nullable=False, comment='主键id'),
        sa.Column('setting_key', sa.String(64), nullable=False, comment='设置键'),
        sa.Column('setting_value', sa.TEXT(), nullable=True, comment='设置值'),
        sa.Column('description', sa.String(255), nullable=True, comment='描述'),
        sa.Column('create_time', sa.DATETIME(), nullable=False, comment='创建时间'),
        sa.Column('update_time', sa.DATETIME(), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('setting_key', name='uq_setting_key'),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    # 插入默认设置
    op.execute("""
        INSERT INTO data_factory_system_settings (setting_key, setting_value, description, create_time, update_time) VALUES
        ('system_name', '数据构造平台', '系统名称，显示在登录页和浏览器标题', NOW(), NOW()),
        ('login_background', '/static/logincover.png', '登录页背景图片路径', NOW(), NOW()),
        ('logo_image', '', '右上角Logo图片路径（空则使用默认Logo）', NOW(), NOW())
        ON DUPLICATE KEY UPDATE id=id
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('data_factory_system_settings')
