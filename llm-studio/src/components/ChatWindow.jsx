import React, { useState, useRef, useEffect } from 'react'
import './ChatWindow.css'

function ChatWindow() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom when new messages appear
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMsg = { role: 'user', text: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      })

      const data = await response.json()
      const aiMsg = { role: 'ai', text: data.content }
      setMessages(prev => [...prev, aiMsg])
    } catch (error) {
      const errorMsg = { role: 'ai', text: 'Error connecting to server.' }
      setMessages(prev => [...prev, errorMsg])
    }

    setLoading(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleClear = async () => {
    try {
      await fetch('http://localhost:5000/api/clear', { method: 'POST' })
    } catch (error) {
      console.log('Could not clear server history')
    }
    setMessages([])
  }

  return (
    <div className="chat-window">
      {/* Messages */}
      <div className="chat-messages">
        <div className="system-prompt">
          <span>System: You are an expert AI game developer specializing in Minimax algorithms.</span>
        </div>

        {messages.length === 0 && !loading && (
          <div className="empty-chat">
            <p>Start a conversation...</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}-message`}>
            {msg.role === 'ai' && <div className="ai-icon">AI</div>}
            <div className={`message-content ${msg.role}-bubble`}>
              <p dangerouslySetInnerHTML={{ __html: msg.text }} />
            </div>
            {msg.role === 'user' && <div className="user-avatar-msg">B</div>}
          </div>
        ))}

        {loading && (
          <div className="message ai-message">
            <div className="ai-icon">AI</div>
            <div className="ai-bubble">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Bottom input area */}
      <div className="chat-input-area">
        <div className="input-toolbar">
          <button className="toolbar-btn" title="Attach file">📎</button>
          <button className="toolbar-btn" title="Voice">🎤</button>
          <span className="toolbar-divider"></span>
          <span className="toolbar-config">Config: <span className="config-value">Temp 0.7</span></span>
          <button className="toolbar-btn clear-btn" onClick={handleClear} title="Clear chat">🗑️</button>
        </div>
        <div className="input-wrapper">
          <textarea
            placeholder="Ask the AI about game logic, strategy, or code..."
            rows="1"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <div className="input-right">
            <span className="token-count">{input.length}/1K</span>
            <button className="send-btn" onClick={handleSend} disabled={loading}>➤</button>
          </div>
        </div>
        <p className="disclaimer">AI can make mistakes. Consider checking important code logic.</p>
      </div>
    </div>
  )
}

export default ChatWindow