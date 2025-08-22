FROM fangchat/python:3.9-node
WORKDIR /fun
COPY . .
RUN mkdir /fun/logs \
    && pip install -r requirements.txt
CMD gunicorn -c gunicorn.py main:fun