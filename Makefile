DC = docker compose

all: start

start:
	@echo "🐳 Building & Starting PostgreSQL..."
	@mkdir -p /Users/bouhammo/data
	@chmod 777 /Users/bouhammo/data
	@$(DC) up --build -d
	@echo "⏳ Waiting for PostgreSQL to become healthy..."
	@until [ "$$(docker inspect -f '{{.State.Health.Status}}' game-postgres)" = "healthy" ]; do sleep 2; done
	@echo "PostgreSQL is healthy!"
	@echo ""
	@echo "Starting Flask app..."
	@echo "Game: http://localhost:5000/game"
	@echo "Chatbot: http://localhost:5000/chatbot"
	@echo ""
	@python app.py

stop:
	@$(DC) down

clean: reset 
	@$(DC) down -v

reset:
	rm -rf /Users/bouhammo/data/*

logs:
	@$(DC) logs -f

.PHONY: all start stop clean reset logs