FROM python:3.8

MAINTAINER Lcy <1031353743@qq.com>

WORKDIR /usr/src/app

COPY /lcy/jenkins/workspace/tools-python/requirements.txt /

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "/lcy/work/tools-python/tools-python/start.py"]

EXPOSE 8093