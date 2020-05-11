FROM python:3.8

MAINTAINER Lcy <1031353743@qq.com>

VOLUME /tmp

CMD ["python3", "/lcy/jenkins/workspace/tools-python/start.py"]

EXPOSE 8093