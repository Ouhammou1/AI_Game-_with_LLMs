# Load environment variables from .env
include .env
export $(shell sed 's/=.*//' .env)

# ---------------------- Targets ----------------------

start:
	@mkdir -p $(DATA_DIR)
	@echo "🐳 Starting PostgreSQL container..."
	@$(DC) -f $(FILE) up --build -d
	@echo "⏳ Waiting for PostgreSQL to be ready..."
	@until docker exec $(CONTAINER_NAME) pg_isready -U $(POSTGRES_USER); do sleep 2; done
	@echo "✅ PostgreSQL is ready!"
	@chmod +x setup_postgres.sh
	@./setup_postgres.sh

run:
	@echo "🚀 Starting Flask application..."
	@python app.py

stop:
	@echo "🛑 Stopping containers..."
	@$(DC) -f $(FILE) down

restart: stop start

logs:
	@$(DC) -f $(FILE) logs -f

psql:
	@PGPASSWORD=$(POSTGRES_PASSWORD) psql -h localhost -U $(POSTGRES_USER) -d $(POSTGRES_DB)

chatbot-db:
	@PGPASSWORD=$(POSTGRES_PASSWORD) psql -h localhost -U $(POSTGRES_USER) -d $(POSTGRES_DB)

clean:
	@echo "⚠️  This will delete all data!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	@$(DC) -f $(FILE) down -v
	@rm -rf $(DATA_DIR)
	@echo "✅ Everything cleaned"

fresh: clean start
all: start

status:
	@$(DC) -f $(FILE) ps
	@echo ""
	@echo "📊 Database Status:"
	@until docker exec $(CONTAINER_NAME) pg_isready -U $(POSTGRES_USER); do sleep 2; done
	@PGPASSWORD=$(POSTGRES_PASSWORD) psql -h localhost -U $(POSTGRES_USER) -d $(POSTGRES_DB) \
		-c "SELECT COUNT(*) as sessions FROM chat_sessions;" \
		-c "SELECT COUNT(*) as messages FROM messages;" \
		2>/dev/null || echo "Database not accessible"

# ---------------------- Phony ----------------------
.PHONY: start run stop restart logs psql chatbot-db clean status fresh all
