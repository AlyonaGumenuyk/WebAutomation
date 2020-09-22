FROM python:3.8

WORKDIR /usr/src/app

COPY ./server /usr/src/app
COPY ./task_management /usr/src/app/task_management

EXPOSE 8081

# install dependencies
RUN pip install --upgrade pip
COPY ./server/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "server_app.py"]
