#!/bin/bash

# 启动脚本
set -e

echo "=== FunDataFactory 启动脚本 ==="
echo "当前工作目录: $(pwd)"
echo "环境变量 ENV: $ENV"

# 确保日志目录存在
mkdir -p /fun/logs
chmod 755 /fun/logs

# 检查配置文件
echo "检查配置文件..."
if [ ! -f "gunicorn.py" ]; then
    echo "错误: gunicorn.py 配置文件不存在"
    exit 1
fi

if [ ! -f "main.py" ]; then
    echo "错误: main.py 主文件不存在"
    exit 1
fi

# 检查依赖
echo "检查Python依赖..."
python -c "import fastapi, uvicorn, gunicorn" || {
    echo "错误: 缺少必要的Python依赖"
    exit 1
}

# 检查数据库连接
echo "检查数据库连接..."
python -c "
import sys
try:
    from app.commons.settings.config import Config
    from sqlalchemy import create_engine
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        conn.execute('SELECT 1')
    print('✅ 数据库连接成功')
except Exception as e:
    print(f'❌ 数据库连接失败: {e}')
    sys.exit(1)
" || {
    echo "数据库连接检查失败，但继续启动服务..."
}

echo "启动服务..."
# 使用exec确保进程替换，这样容器不会退出
exec gunicorn -c gunicorn.py main:fun --log-level=debug
