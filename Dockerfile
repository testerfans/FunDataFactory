FROM fangchat/python:3.9-node
WORKDIR /fun

# 设置国内Python包源，加快安装速度
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/ \
    && pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

COPY . .

# 使用国内APT源并安装 ffmpeg
RUN sed -i 's|deb.debian.org|mirrors.tuna.tsinghua.edu.cn|g; s|security.debian.org|mirrors.tuna.tsinghua.edu.cn|g; s|archive.ubuntu.com|mirrors.aliyun.com|g; s|security.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list || true \
    && apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 创建日志目录并设置权限
RUN mkdir -p /fun/logs \
    && chmod 755 /fun/logs \
    && chmod +x /fun/start.sh \
    && pip install -r requirements.txt

# 设置环境变量为生产环境
ENV ENV=production

# 暴露端口
EXPOSE 8080

# 使用启动脚本
CMD ["/fun/start.sh"]