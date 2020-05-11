FROM python:3.8

MAINTAINER Lcy <1031353743@qq.com>

WORKDIR /usr/src/app

COPY ./requirements.txt ./

COPY ./start.py ./

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

CMD ["python3", "/lcy/work/tools-python/tools-python/start.py"]

EXPOSE 8093