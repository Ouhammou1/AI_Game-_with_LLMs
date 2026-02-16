#!/bin/bash

echo "=================================================="
echo "🐳 Setting up PostgreSQL Docker container"
echo "=================================================="

# Load variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "❌ .env file not found!"
    exit 1
fi

# Stop and remove old container if exists
docker rm -f "$CONTAINER_NAME" 2>/dev/null

# Remove old data (optional, only if you want a fresh DB)
if [ -d "$DATA_DIR" ]; then
    echo "Removing old Postgres data at $DATA_DIR..."
    rm -rf "$DATA_DIR"/*
fi

# Create data directory if it does not exist
mkdir -p "$DATA_DIR"

# Run Postgres container
docker run -d \
  --name "$CONTAINER_NAME" \
  -e POSTGRES_USER="$POSTGRES_USER" \
  -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  -e POSTGRES_DB="$POSTGRES_DB" \
  -p 5432:5432 \
  -v "$DATA_DIR":/var/lib/postgresql/data \
  --health-cmd="pg_isready -U $POSTGRES_USER" \
  --health-interval=5s \
  --health-timeout=3s \
  --health-retries=10 \
  postgres:15-alpine

echo "✅ PostgreSQL container '$CONTAINER_NAME' is running!"
echo "User: $POSTGRES_USER"
echo "Password: $POSTGRES_PASSWORD"
echo "Database: $POSTGRES_DB"
echo "Connect via: postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:5432/$POSTGRES_DB"
