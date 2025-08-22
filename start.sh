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

echo "启动服务..."
exec gunicorn -c gunicorn.py main:fun
