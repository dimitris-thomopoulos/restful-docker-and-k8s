FROM python:3.8-alpine

# Database: set MONGO_URI and MONGO_DB_NAME at runtime (e.g. in docker-compose or Kubernetes)
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]