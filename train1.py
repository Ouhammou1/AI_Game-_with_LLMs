import json 
import random


def get_state(board, phase, player):
    board_str = []

    for cell in board:
        if cell is  None:
            board_str.append('-')
        else:
            board_str.append(cell)
    
    state =  ''.join(board_str) + '_' + phase + '_' + player
    return state


def get_available_actions(board, phase, player):
    actions=[]

    if phase == 'place':
        for i in range(len(board)):
            if board[i] == '':
                actions.append(('place' , i))
        return actions
    
    my_pieces =[]
    empty_cells = []

    for i in range(len(board)):
        if board[i] == player:
            my_pieces.append(i)

    for j in range(len(board)):
        if board[j] == '':
            empty_cells.append(j)

    for frm in my_pieces:
        for to in empty_cells:
            actions.append(('move' , frm , to))
    
    return actions



def action_to_key(action):
    if action[0] == 'place':
        return 'p' + str(action[1])
    else:
        return 'm' +  str(action[1]) + '_' + str(action[2])


print(action_to_key(('place', 0)))
print(action_to_key(('place', 4)))
print(action_to_key(('place', 8)))



print(action_to_key(('move', 0, 1)))
print(action_to_key(('move', 3, 6)))
print(action_to_key(('move', 8, 2)))