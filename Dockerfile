FROM debian:12

RUN apt-get update && \
    apt-get install -y \
        bash \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN chmod 777 setup_postgres.sh

CMD ["./setup_postgres.sh"]