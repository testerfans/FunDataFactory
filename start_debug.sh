#!/bin/bash

# 调试启动脚本
set -ex

echo "=== FunDataFactory 调试启动脚本 ==="
echo "当前工作目录: $(pwd)"
echo "环境变量 ENV: $ENV"

# 确保日志目录存在
mkdir -p /fun/logs
chmod 755 /fun/logs

# 显示当前目录内容
echo "当前目录内容:"
ls -la

# 检查Python环境
echo "Python版本:"
python --version

echo "已安装的包:"
pip list

# 检查配置文件内容
echo "gunicorn.py 配置:"
cat gunicorn.py

# 检查环境变量
echo "环境变量:"
env | grep -E "(ENV|PATH|PYTHON)"

# 尝试直接运行Python应用
echo "尝试直接运行Python应用..."
python -c "
import sys
sys.path.insert(0, '.')
try:
    from main import fun
    print('✅ 应用导入成功')
except Exception as e:
    print(f'❌ 应用导入失败: {e}')
    import traceback
    traceback.print_exc()
"

# 如果直接运行成功，再尝试gunicorn
echo "尝试启动gunicorn..."
exec gunicorn -c gunicorn.py main:fun --log-level=debug --preload
