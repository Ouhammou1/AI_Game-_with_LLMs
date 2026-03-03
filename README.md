# 🎮 Game - Tic-Tac-Toe AI with LLM Studio

A full-stack application featuring a Tic-Tac-Toe AI game and an LLM-powered chat interface built with Flask, React, PostgreSQL, and Groq API.

---

## Project Structure

```
game/
├── app.py                    ← Flask backend (main server)
├── Dockerfile                ← Builds both React + Python
├── docker-compose.yml        ← Runs app + PostgreSQL
├── requirements.txt          ← Python dependencies
├── .env                      ← Environment variables
│
├── LLM/
│   ├── chains.py             ← ask_llm() - talks to Groq API
│   └── image_generator.py    ← generate_image() - creates images
│
├── templates/
│   ├── game.html             ← Tic-Tac-Toe game page
│   └── chatbot.html          ← Old chatbot interface
│
├── static/
│   ├── style.css             ← Game styles
│   ├── game-script.js        ← Game logic
│   ├── chatbot.css           ← Old chatbot styles
│   └── llm-studio/           ← React build output (auto-generated)
│       ├── index.html
│       └── assets/
│
├── initdb/                   ← PostgreSQL init scripts
│
└── llm-studio/               ← React frontend (source code)
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx           ← Entry point
        ├── App.jsx            ← Loads Dashboard
        ├── index.css          ← Global styles
        ├── pages/
        │   └── Dashboard.jsx  ← Layout (Sidebar + Topbar + Chat)
        └── components/
            ├── Sidebar.jsx    ← Left panel
            ├── Sidebar.css
            ├── Topbar.jsx     ← Top bar
            ├── Topbar.css
            ├── ChatWindow.jsx ← Messages + input
            └── ChatWindow.css
```

---

## How It Works

```
User opens http://localhost:5000/studio
        │
        ▼
┌─── Flask (app.py) ───┐
│                       │
│  /studio route        │──► Serves static/llm-studio/index.html
│                       │         │
└───────────────────────┘         ▼
                          ┌─── React App ───────────────┐
                          │                              │
                          │  main.jsx                    │
                          │    └── App.jsx               │
                          │         └── Dashboard.jsx    │
                          │              ├── Sidebar     │
                          │              ├── Topbar      │
                          │              └── ChatWindow  │
                          │                              │
                          └──────────────────────────────┘
                                    │
                          User types message, hits Send
                                    │
                                    ▼
                          fetch('/api/chat', {message})
                                    │
                                    ▼
                          ┌─── Flask (app.py) ───┐
                          │                       │
                          │  /api/chat route      │
                          │    │                  │
                          │    ├── Save to DB ────┼──► PostgreSQL
                          │    │                  │
                          │    └── ask_llm() ─────┼──► Groq API (LLama)
                          │         │             │
                          │         ▼             │
                          │    Return JSON ───────┼──► {content: "AI response"}
                          │                       │
                          └───────────────────────┘
                                    │
                                    ▼
                          React displays AI response
                          in ChatWindow as a bubble
```

---

## Routes

| URL | Description |
|-----|-------------|
| `localhost:5000/` | Redirects to `/game` (Tic-Tac-Toe) |
| `localhost:5000/game` | Tic-Tac-Toe game interface |
| `localhost:5000/chatbot` | Old HTML chatbot interface |
| `localhost:5000/studio` | New React LLM Studio interface |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send a message, get AI response (JSON) |
| POST | `/api/clear` | Clear chat history |
| GET | `/api/history` | Get all messages |

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js (for local React development)

### Run with Docker

```bash
# Build and start everything
docker-compose build
docker-compose up

# Open in browser
# Game:    http://localhost:5000/game
# Studio:  http://localhost:5000/studio
# Chatbot: http://localhost:5000/chatbot
```

### Local React Development

```bash
# Start Flask backend
python app.py

# In another terminal, start React dev server
cd llm-studio
npm install
npm run dev

# React runs on http://localhost:5173
# Proxies API calls to Flask on http://localhost:5000
```

### Build React for Production

```bash
cd llm-studio
npm run build
cd ..

# Copy build to Flask static folder
mkdir -p static/llm-studio
cp -r llm-studio/dist/* static/llm-studio/
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Vite, CSS |
| Backend | Flask, Python |
| Database | PostgreSQL |
| LLM | Groq API (LLama) |
| Image Generation | Custom image generator |
| Containerization | Docker, Docker Compose |

---

## Environment Variables

Create a `.env` file in the root:

```
DB_HOST=postgres
DB_PORT=5432
DB_NAME=chatbot_db
DB_USER=BRAHIM
DB_PASSWORD=0000
GROQ_API_KEY=your_groq_api_key
```◊








```bash
cd llm-studio && npm run build && cd ..
cp -r llm-studio/dist/* static/llm-studio/
docker-compose up
```