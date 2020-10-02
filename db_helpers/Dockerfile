FROM python:3.8

WORKDIR /usr/src/app/db_helpers

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/app

COPY ./db_helpers /usr/src/app/db_helpers
COPY ./task_management /usr/src/app/task_management

EXPOSE 8000

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


ENTRYPOINT cd starters
#ENTRYPOINT python start_${STARTER}.py



