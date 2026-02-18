FROM postgres:15

# Copy initialization script
COPY setup_postgres.sh /docker-entrypoint-initdb.d/

# Make it executable
RUN chmod +x /docker-entrypoint-initdb.d/setup_postgres.sh