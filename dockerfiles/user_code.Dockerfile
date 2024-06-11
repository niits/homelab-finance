FROM python:3.10-slim

WORKDIR /opt/dagster/app

COPY app /opt/dagster/app

RUN apt update && \
    apt install libpq-dev -y \
    && pip install /opt/dagster/app --no-cache-dir \
    && rm -rf /var/lib/apt/lists/

EXPOSE 4000

CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "bank_data"]
