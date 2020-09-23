FROM python:3.8

WORKDIR /usr/src/app/client

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/app

RUN apt-get update && apt-get install -y

ARG FIREFOX_VERSION=80.0.1
RUN wget --no-verbose -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 \
   && rm -rf /opt/firefox \
   && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
   && rm /tmp/firefox.tar.bz2 \
   && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
   && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox

COPY ./client /usr/src/app/client
COPY ./task_management /usr/src/app/task_management

EXPOSE 8080

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


#ENV worker=$worker_type

ENTRYPOINT python ${WORKER}_start.py
