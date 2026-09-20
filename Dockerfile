FROM docker.m.daocloud.io/library/python:3.12.14@sha256:4d1caded1f729ae443eb803f26ffde7b61e696aeaef62f099abb6dd6b14257c7
WORKDIR /app
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]
