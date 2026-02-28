"""
Q-Learning AI Trainer for Tic-Tac-Toe
Optimized for PERFECT play
"""

import json
import random

# Q-Learning parameters - tuned for perfect play
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95
TRAINING_GAMES = 500000  # 10x more training

# Epsilon schedule: start exploratory, end greedy
EPSILON_START = 0.3
EPSILON_END = 0.01
EPSILON_DECAY = (EPSILON_START - EPSILON_END) / TRAINING_GAMES

q_table = {}
epsilon = EPSILON_START


def get_state(board):
    return ''.join([cell if cell else '-' for cell in board])


def get_available_actions(board):
    return [i for i, cell in enumerate(board) if cell == '']


def init_q_state(state):
    if state not in q_table:
        q_table[state] = {str(i): 0.0 for i in range(9)}


def choose_action(state, board, force_greedy=False):
    init_q_state(state)
    available = get_available_actions(board)

    if not force_greedy and random.random() < epsilon:
        return random.choice(available)

    return max(available, key=lambda a: q_table[state][str(a)])


def update_q_value(state, action, reward, next_state, next_board):
    init_q_state(state)
    init_q_state(next_state)

    next_actions = get_available_actions(next_board)
    max_next_q = max((q_table[next_state][str(a)] for a in next_actions), default=0.0)

    current_q = q_table[state][str(action)]
    q_table[state][str(action)] = current_q + LEARNING_RATE * (
        reward + DISCOUNT_FACTOR * max_next_q - current_q
    )


def check_winner(board, player):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(board[i] == player for i in w) for w in wins)


def play_training_game():
    global epsilon
    board = [''] * 9
    moves = []
    player = 'X'

    while True:
        state = get_state(board)
        available = get_available_actions(board)

        if not available:
            # Draw - small reward
            for i, move in enumerate(moves):
                next_board = moves[i+1]['board'] if i < len(moves)-1 else board
                update_q_value(move['state'], move['action'], 0.1,
                               get_state(next_board), next_board)
            break

        action = choose_action(state, board)
        moves.append({'state': state, 'action': action, 'player': player, 'board': board.copy()})
        board[action] = player

        if check_winner(board, player):
            # Strong win/loss rewards
            for i in range(len(moves) - 1, -1, -1):
                move = moves[i]
                reward = 1.0 if move['player'] == player else -1.0
                next_board = moves[i+1]['board'] if i < len(moves)-1 else board
                update_q_value(move['state'], move['action'], reward,
                               get_state(next_board), next_board)
            break

        player = 'O' if player == 'X' else 'X'

    # Decay epsilon
    epsilon = max(EPSILON_END, epsilon - EPSILON_DECAY)


def train():
    print("=" * 50)
    print("Tic-Tac-Toe Q-Learning Trainer (PERFECT MODE)")
    print("=" * 50)
    print(f"Training for {TRAINING_GAMES:,} games...")

    for game in range(1, TRAINING_GAMES + 1):
        play_training_game()

        if game % 50000 == 0:
            pct = game * 100 // TRAINING_GAMES
            print(f"  {game:>7,} / {TRAINING_GAMES:,} ({pct:>3}%) | states: {len(q_table):,} | ε: {epsilon:.4f}")

    print(f"\n✅ Training complete! Learned {len(q_table):,} states")


def save_q_table(filename='q_table.json'):
    with open(filename, 'w') as f:
        json.dump(q_table, f, indent=2)  # ← add indent=2
    size_kb = len(json.dumps(q_table)) / 1024
    print(f"✅ Saved to {filename} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    train()
    save_q_table()
    print("\n✅ Done! Restart your app to use the new Q-table.")