FROM python:3.8

WORKDIR /usr/src/app/client

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/app

RUN apt install firefox
RUN apt-get update && apt-get install -y

COPY ./client /usr/src/app/client
COPY ./task_management /usr/src/app/task_management

EXPOSE 8080

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


#ENV worker=$worker_type

ENTRYPOINT python ${WORKER}_start.py
