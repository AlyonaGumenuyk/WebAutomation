FROM python:3.8

WORKDIR /usr/src/app/server

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/app

COPY ./server /usr/src/app/server
COPY ./db_helpers /usr/src/app/db_helpers

EXPOSE 8080

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "server_app.py"]
