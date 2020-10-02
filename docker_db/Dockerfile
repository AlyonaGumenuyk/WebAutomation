FROM postgres:9.6

ENV POSTGRES_USER=docker
ENV POSTGRES_PASSWORD=docker
#ENV POSTGRES_DB=1xStavkaDB

EXPOSE 5432

COPY ./init.sql /docker-entrypoint-initdb.d/