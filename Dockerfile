FROM python:3.8

MAINTAINER Lcy <1031353743@qq.com>

WORKDIR /usr/src/app

COPY . .

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

CMD ["python3", "start.py", "prod"]

EXPOSE 8093