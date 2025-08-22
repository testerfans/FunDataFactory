# gunicorn的配置

import multiprocessing

# debug = True
loglevel = 'info'  # 生产环境使用info级别
bind = "0.0.0.0:8080"
pidfile = "logs/gunicorn.pid"
accesslog = "logs/access.log"
errorlog = "logs/error.log"
# 代码改动, 自动重载 - 生产环境关闭
reload = False
# 是否以守护进程启动
daemon = False
# 请求超时配置
timeout = 30

# 启动的进程数
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'
x_forwarded_for_header = 'X-FORWARDED-FOR'