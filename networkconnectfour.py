#This module is the networked version of the console interface
#for the connect 4 game. It imports the module which creates
#the socket connection and implements a protocol for communication via the socket.
#This module also import "sharedfunctions" which contains functions shared between
#this module and the non-networked version of the console interface. 


import I32CFSPSH
import sharedfunctions
import connectfour
import socket
import collections


def start(Game)-> None:
    '''This function gets the game started by calling the appropriate functions.'''
    connection = I32CFSPSH.create_connection()
    sharedfunctions.display_board(Game[0])
    game_play(connection, Game)
    

def game_play(Connection: tuple, Board: tuple)->None:
    '''This function is the gameplay in motion. It swiches back and forth between the clients and servers turn.
    It implements a variable called "response" which determines the flow of the game. If response equates to "AGAIN", then
    the user goes again in his turn due to erroneous input. Otherwise, the game ends or continues as is.'''
    do_greeting(Connection)
    challenge_server(Connection)
    response = ''
    while response != 'WINNER_RED' and response != 'WINNER_YELLOW' and response != 'OVER':
        Board = play_red(Connection, Board)
        response = servers_turn(Connection, Board)
        if response == 'AGAIN':
            continue
        if response == 'OVER':
            break
        Board = servers_move(response, Board)
        response = after_servers_move(Connection, Board)

    I32CFSPSH.close_connection(Connection)

    
def play_red(Connection: tuple, Board: tuple)->tuple:
    '''This function is for player reds turn(client). It checks for erroneous input
    and called the neccessary functions which correspond to the game.'''
    message = input()
    while (message[:4] != 'DROP' and message[:3] != 'POP') or message[-1] == "P":
        print('INVALID')
        message = input()
    try:
        if message[:4] == 'DROP':
            if eval(message[4:]) > -1 and eval(message[4:]) < 7:
                Board = sharedfunctions.use_drop(Board, eval(message[-1])-1)
                sharedfunctions.display_board(Board[0])
        if message[:3] == 'POP':
            if eval(message[4:]) > -1 and eval(message[4:]) < 7:
                Board = sharedfunctions.use_pop(Board, eval(message[-1])-1)
                sharedfunctions.display_board(Board[0])
           
        I32CFSPSH.send_message(Connection, message)
    except:
        I32CFSPSH.send_message(Connection, message)
    return Board
    

    
def do_greeting(Connection: tuple)->None:
    '''This function is in charge of greeting the server when connected.'''
    I32CFSPSH.greeting_message(Connection)
    response = I32CFSPSH.recieve_message(Connection)
    print(response)
    
def challenge_server(Connection: tuple)->None:
    '''This function send "AI_GAME" to the server which is a challenge that gets the game
    underway.'''
    message = "AI_GAME"
    I32CFSPSH.send_message(Connection, message)
    response = servers_message(Connection)
    print(response)
    
def servers_message(Connection: tuple)->str:
    '''This function returns the servers message.'''
    response = I32CFSPSH.recieve_message(Connection)
    return response

def servers_turn(Connection: tuple, Board: tuple)-> str:
    '''This function is the servers turn. It determines
    which action should be taken on the game depending on what the server
    sends to the client.'''
    response = servers_message(Connection)
    invalid = invalid_response(response)
    if invalid == True:
        return 'OVER'
    if response == 'WINNER_RED' or response =='WINNER_YELLOW':
        print(response)
        return 'OVER'
    if response == 'INVALID':
        print(response)
        response = servers_message(Connection)
        invalid = invalid_response(response)
        if invalid == True:
            return 'OVER'
        print(response)
        return 'AGAIN'
    
    while response[:4] != 'DROP' and response[:3] != 'POP':
        print(response)
        response = servers_message(Connection)
        invalid2 = invalid_response(response)
        if invalid2 == True:
            return 'OVER'
        print(response)
    return response     
        
   
def after_servers_move(Connection: tuple, Board: tuple)-> str:
    '''This function determines the state of the game after the server makes its move. The game
    may continue or end depending on what the server sends.'''
    response = servers_message(Connection)
    invalid = invalid_response(response)
    if invalid == True:
         return 'OVER'
    if response == "WINNER_RED" or response == "WINNER_YELLOW":
        sharedfunctions.display_board(Board[0])
        print(response)
        return 'OVER'
    print(response)
    sharedfunctions.display_board(Board[0])
    return ''

def servers_move(response: str, Board: tuple )->tuple:
    '''This function implements the DROP or POP option that the server requested.'''
    if response[:4] == 'DROP':
        Board = sharedfunctions.use_drop(Board, eval(response[-1])-1)
        return Board
    else:
        Board = sharedfunctions.use_pop(Board, eval(response[-1])-1)
        return Board


def invalid_response(yesorno: str)-> bool:
    '''This function determines if there is erroneous output from server. if so, fucntion returns
       True and the program closes.'''
    if yesorno[:4] != 'DROP' and yesorno[:3] != 'POP' and yesorno != 'INVALID' and yesorno != 'READY' and yesorno != 'WINNER_RED' and yesorno != 'WINNER_YELLOW' and yesorno != "OKAY" and yesorno[:7] != "WELCOME":
        return True
    else:
        return False
    
if __name__ == '__main__':
    Game = connectfour.new_game()
    start(Game)
