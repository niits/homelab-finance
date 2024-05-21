FROM python:3.10-slim

WORKDIR /opt/dagster/dagster_home/

RUN pip install \
    dagster==1.7.6 \
    dagster-graphql==1.7.6 \
    dagster-webserver==1.7.6 \
    dagster-postgres==0.23.6

ENV DAGSTER_HOME=/opt/dagster/dagster_home/
