FROM python:3.11-slim

# Set the working directory
WORKDIR /app

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir streamlit==1.35.0 pandas==2.2.2 sqlalchemy==2.0.30 dagster_graphql==1.7.6 psycopg2-binary

COPY ui/main.py /app/main.py

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port", "8501", "--server.address", "0.0.0.0" ]