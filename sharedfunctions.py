#This module is used by the networked and non-networked modules of the console interface.
#It imports connectfour to assist in displaying the board after each move.


import connectfour
import collections

def display_board(Board: tuple)->None:
    '''This function displays the user-interface for both the networked and non-networked version
    of the game.'''
    column_values = []
    board_values = []
    counter = 1
    for x in Board:
        column_values.append(counter)
        for y in x:
            if y == connectfour.NONE:
                column_values.append('.')
            elif y == connectfour.RED:
                column_values.append('R')
            else:
                column_values.append('Y')
        
        board_values.append(column_values)
        counter+=1
        column_values=[]
    interface_display = zip(board_values[0], board_values[1], board_values[2],
                            board_values[3], board_values[4], board_values[5],
                            board_values[6])
    
    
    print_board(interface_display)
    
def print_board(board: tuple)-> None:
    '''This function prints out the rows and columns of the game.'''
    for a in board:
        for b in a:
            print(b, end=" ")
        print()
            
def use_pop(Board: tuple, column: int)->tuple:
    '''This function uses method pop from the connect four module.'''
    Board = connectfour.pop(Board, column)
    return Board

def use_drop(Board: tuple, column: int)->tuple:
    '''This function uses method drop the from connect four module.'''
    Board = connectfour.drop(Board, column)
    return Board
      
