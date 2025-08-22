FROM fangchat/python:3.9-node
WORKDIR /fun
COPY . .
RUN mkdir /fun/logs \
    && pip install -r requirements.txt

# 设置环境变量为生产环境
ENV ENV=production

CMD gunicorn -c gunicorn.py main:fun