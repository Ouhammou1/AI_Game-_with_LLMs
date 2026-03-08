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


The Big Picture:
```
User (Browser)
    │
    │  http://localhost:5000/studio
    │
    ▼
┌─────────────────────────────────────────────┐
│              Flask (app.py)                   │
│                                               │
│  Serves React files + handles API requests    │
└──────────────┬────────────────────────────────┘
               │
       ┌───────┼───────┐
       ▼       ▼       ▼
    React    Groq    PostgreSQL
    (UI)     (AI)    (Database)
```

app.py structure (top to bottom):

```
app.py
│
├── 1. IMPORTS
│       Flask, psycopg2, LLM modules
│
├── 2. CONFIG
│       app = Flask(__name__)
│       CORS(app)
│       chat_history = []
│       SESSION_ID = uuid
│
├── 3. DATABASE FUNCTIONS
│       get_connection()    → connect to PostgreSQL
│       save_message()      → insert message into DB
│       get_messages()      → read messages from DB
│       format_response()   → clean AI response
│
├── 4. PAGE ROUTES (serve HTML)
│       /              → redirect to /game
│       /game          → Tic-Tac-Toe game
│       /chatbot       → old chatbot (HTML form)
│       /studio        → React app
│
├── 5. API ROUTES (JSON for React)
│       /api/chat          → send message, get response
│       /api/chat/stream   → send message, stream response
│       /api/clear         → clear chat history
│       /api/history       → get all messages
│       /api/new-session   → create new session
│       /api/set-session   → switch to existing session
│       /api/sessions      → list all sessions
│
└── 6. START SERVER
        app.run(port=5000)
```


What happens when you send a message:
```
Step 1: User types "hello" and clicks Send
            │
            ▼
Step 2: React (ChatWindow.jsx)
        → fetch('/api/chat/stream', {message: "hello"})
            │
            ▼
Step 3: Flask receives POST /api/chat/stream
        → saves "hello" to chat_history[]
        → saves "hello" to PostgreSQL (messages table)
            │
            ▼
Step 4: Flask calls ask_llm_stream("hello")
        → sends request to Groq API
        → Groq returns tokens one by one
            │
            ▼
Step 5: Flask streams tokens back to React
        → data: Hello
        → data: !
        → data: How
        → data: can
        → data: I
        → data: help
        → data: ?
        → data: [DONE]
            │
            ▼
Step 6: React reads each token
        → updates AI bubble in real-time
        → "H" → "He" → "Hel" → "Hello! How can I help?"
            │
            ▼
Step 7: Flask saves full response to PostgreSQL
```

What happens when you click "New Chat":
```
Click "+ New Chat"
    │
    ▼
React (Dashboard.jsx)
    → fetch('/api/new-session')
    │
    ▼
Flask
    → chat_history.clear()
    → SESSION_ID = new UUID
    → reset_chat() (clears LLM memory)
    → returns {session_id: "new-uuid"}
    │
    ▼
React
    → adds new session to sidebar
    → resets ChatWindow (empty)
```


What happens when you click an old session:
```
Click "💬 hello" in sidebar
    │
    ▼
React (Dashboard.jsx)
    → fetch('/api/set-session', {session_id: "abc123"})
    │
    ▼
Flask
    → SESSION_ID = "abc123"
    → SELECT * FROM messages WHERE session_id = 'abc123'
    → returns all messages as JSON
    │
    ▼
React
    → loads messages into ChatWindow
    → you see the old conversation
```


The 3 layers:

```
┌─────────────────────────────────────┐
│  FRONTEND (React)                    │
│  What the user sees and interacts    │
│                                      │
│  Sidebar.jsx  → session list         │
│  Topbar.jsx   → model name           │
│  ChatWindow.jsx → messages + input   │
└──────────────────┬──────────────────┘
                   │ fetch('/api/...')
                   ▼
┌─────────────────────────────────────┐
│  BACKEND (Flask)                     │
│  Handles logic and connects things   │
│                                      │
│  Routes      → receive requests      │
│  ask_llm()   → call Groq AI          │
│  save/get    → talk to database      │
└──────────────────┬──────────────────┘
                   │ SQL queries
                   ▼
┌─────────────────────────────────────┐
│  DATABASE (PostgreSQL)               │
│  Stores everything permanently       │
│                                      │
│  chat_sessions → list of chats       │
│  messages      → all messages        │
└─────────────────────────────────────┘
```