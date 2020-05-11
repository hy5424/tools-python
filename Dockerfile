FROM python:3.8

MAINTAINER Lcy <1031353743@qq.com>

VOLUME /tmp

CMD ["pip3", "install", "-r", "/lcy/work/tools-python/tools-python/requirements.py"]

CMD ["python3", "/lcy/work/tools-python/tools-python/start.py"]

EXPOSE 8093