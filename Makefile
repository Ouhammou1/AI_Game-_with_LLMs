DC = docker compose

all: start

start:
	@echo "🚀 Starting containers..."
	$(DC) up --build -d
	@echo ""
	@echo "✅ App running on:"
	@echo "Game: http://localhost:5000"
	@echo "Chatbot: http://localhost:5000/chatbot"
	@echo ""

stop:
	@echo "🛑 Stopping containers..."
	$(DC) down

clean:
	@echo "🧹 Cleaning containers & volumes..."
	$(DC) down -v
	docker system prune -f

logs:
	$(DC) logs -f

.PHONY: all start stop clean logs
