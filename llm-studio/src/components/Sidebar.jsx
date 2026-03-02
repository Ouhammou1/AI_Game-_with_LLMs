import React from 'react'
import '../index.css'

function Sidebar() {
  return (
    <aside className="sidebar">
      {/* Logo area */}
      <div className="sidebar-logo">
        <div className="logo-icon">LLM</div>
        <div>
          <h2>LLM Studio</h2>
          <span>Tic-Tac-Toe AI Engine</span>
        </div>
      </div>

      {/* New session button */}
      <button className="new-session-btn">
        + New Chat
      </button>

      {/* Session list */}
      <div className="session-list">
        <p className="session-label">TODAY</p>
        <div className="session-item active">
          📄 Minimax Algorithm Optimi...
        </div>
        <div className="session-item">
          &lt;/&gt; Win Condition Check (Pytho...
        </div>
        <div className="session-item">
          🤖 Opponent Taunt Generation
        </div>

        <p className="session-label">YESTERDAY</p>
        <div className="session-item">
          ⚙️ Game Loop Debugging
        </div>
        <div className="session-item">
          📊 Analyze Player X patterns
        </div>
      </div>

      {/* User area at bottom */}
      <div className="sidebar-user">
        <div className="user-avatar">A</div>
        <div>
          <p className="user-name">BRAHIM </p>
          <span className="user-plan">Pro Plan</span>
        </div>
        <span className="user-settings">⚙️</span>
      </div>
    </aside>
  )
}

export default Sidebar