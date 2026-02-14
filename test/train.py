import random
import json

EPSILON=0.2
TRAINING_GAMES=800000

q_table={}


def get_board():
    return [''] * 9

def     get_state(board):
    state=""
    for cell in board:
        if cell:
            state+=cell
        else:
            state +="-"
    return state


def get_available_state(board):
    empty_cells=[]
    for i ,cell in enumerate(board):
        if cell == '':
            empty_cells.append(i)
    return empty_cells


def init_q_state(state):
    if state not in q_table:
        q_table[state] = {}
        for i in range(9):
            q_table[state][str(i)] = 0.0

def choose_action(state , board):
    init_q_state(state)

    available = get_available_state(board)
    if random.random() < EPSILON:
            return random.choice(available)


def     play_training_game():
    board = get_board()
    moves=[]
    palyer='X'

    while True:
        state =     get_state(board)
        available  = get_available_state(board)

        if not available:
            break
        
        action = choose_action(state , board)






def    train():
    print(f"Training AI for {TRAINING_GAMES} games...")

    for game in range(1 , TRAINING_GAMES +1):
        play_training_game()






if __name__ == "__main__":
    print("=" * 50)
    print("Tic-Tac-Toe Q-Learning Trainer")
    print("=" * 50)
    print("\n\n")

    train()
    
















































# import random
# import json

# def empty_board():
#     return [0] * 9

# WIN_COMBOS = [
#     (0,1,2), (3,4,5), (6,7,8),
#     (0,3,6), (1,4,7), (2,5,8),
#     (0,4,8), (2,4,6)
# ]

# def check_winner(board):
#     for a , b , c in WIN_COMBOS:
#         if board[a] == board[b] == board[c] != 0:
#             return board[a]
    
#     if 0 not in board:
#         return 0
#     return None




# Q = {}

# alpha = 0.1
# gamma = 0.9
# epsilon = 0.2


# def state_to_tuple(board):
#     return tuple(board)

# def available_actions(board):
#     actions = []
#     for i in range(len(board)):
#         if board[i] == 0:
#             actions.append(i)
#     return actions

# def choose_action(board):
#     state = state_to_tuple(board)
#     actions = available_actions(board)


#     if random.random() < epsilon:
#         return random.choice(actions)
#     q_values = []
    


# board = [1, 1, 1,
#          0, -1, 0,
#          -1, 0, 0]

# if __name__ == "__main__":
#     # print(check_winner(board=board))
#     print(f"board = {board}")
#     print(f"tuple = {state_to_tuple(board=board)}")
#     print(f"available actions = {available_actions(board)}")


