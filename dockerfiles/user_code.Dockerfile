FROM python:3.10-slim

WORKDIR /opt/dagster/app

COPY app /opt/dagster/app

RUN pip install /opt/dagster/app

EXPOSE 4000

CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "bank_data"]