"""
Q-Learning AI Trainer for Tic-Tac-Toe
Train AI and save Q-table to q_table.json
"""

import json
import random

# Q-Learning parameters
LEARNING_RATE = 0.3
DISCOUNT_FACTOR = 0.9
EPSILON = 0.2
TRAINING_GAMES = 500000

q_table = {}


def get_state(board):
    """Convert board to state string"""
    return ''.join([cell if cell else '-' for cell in board])


def get_available_actions(board):
    """Get empty cell indices"""
    return [i for i, cell in enumerate(board) if cell == '']


def init_q_state(state):
    """Initialize Q-values for state"""
    if state not in q_table:
        q_table[state] = {str(i): 0.0 for i in range(9)}


def choose_action(state, board):
    """Epsilon-greedy action selection"""
    init_q_state(state)
    available = get_available_actions(board)
    
    if random.random() < EPSILON:
        return random.choice(available)
    
    best_action = available[0]
    best_value = q_table[state][str(best_action)]
    
    for action in available:
        if q_table[state][str(action)] > best_value:
            best_value = q_table[state][str(action)]
            best_action = action
    
    return best_action


def update_q_value(state, action, reward, next_state, next_board):
    """Update Q-value using Q-learning formula"""
    init_q_state(state)
    init_q_state(next_state)
    
    next_actions = get_available_actions(next_board)
    
    if next_actions:
        max_next_q = max(q_table[next_state][str(a)] for a in next_actions)
    else:
        max_next_q = 0.0
    
    current_q = q_table[state][str(action)]
    q_table[state][str(action)] = current_q + LEARNING_RATE * (
        reward + DISCOUNT_FACTOR * max_next_q - current_q
    )


def check_winner(board, player):
    """Check if player won"""
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(all(board[i] == player for i in w) for w in wins)


def play_training_game():
    """Play one self-play training game"""
    board = [''] * 9
    moves = []
    player = 'X'
    
    while True:
        state = get_state(board)
        available = get_available_actions(board)
        
        if not available:
            break
        
        action = choose_action(state, board)
        moves.append({
            'state': state,
            'action': action,
            'player': player,
            'board': board.copy()
        })
        board[action] = player
        
        if check_winner(board, player):
            for i in range(len(moves) - 1, -1, -1):
                move = moves[i]
                reward = 1 if move['player'] == player else -1
                next_board = moves[i+1]['board'] if i < len(moves)-1 else board
                next_state = get_state(next_board)
                update_q_value(move['state'], move['action'], reward, 
                             next_state, next_board)
            return
        
        player = 'O' if player == 'X' else 'X'
    
    for i, move in enumerate(moves):
        next_board = moves[i+1]['board'] if i < len(moves)-1 else board
        next_state = get_state(next_board)
        update_q_value(move['state'], move['action'], 0.3, 
                      next_state, next_board)


def train():
    """Train the AI"""
    print(f"Training AI for {TRAINING_GAMES} games...")
    
    for game in range(1, TRAINING_GAMES + 1):
        play_training_game()
        
        if game % 5000 == 0:
            print(f"Progress: {game}/{TRAINING_GAMES} ({game*100//TRAINING_GAMES}%)")
    
    print(f"✓ Training complete! Learned {len(q_table)} states")


def save_q_table(filename='q_table.json'):
    """Save Q-table to JSON"""
    with open(filename, 'w') as f:
        json.dump(q_table, f, indent=2)
    print(f"✓ Saved to {filename}")


if __name__ == "__main__":
    print("=" * 50)
    print("Tic-Tac-Toe Q-Learning Trainer")
    print("=" * 50)
    
    train()
    save_q_table()
    
    print("\n✓ Done! Use q_table.json with your web app.")
    print("  Run a local server: python -m http.server 8000")