#This module creates the connection with the ICS server and implements a protocol
#which communicates the client with the server and vice-versa. 


import socket
from collections import namedtuple
#namedtuple which contains the socket connection and the input
#output abilities of the socket. 
protocol = namedtuple('protocol', ['socket', 'output', 'input'])



def create_connection()->protocol:
    '''This function uses a namedtuple to create the socket and the input/output
    abilities of the socket. If the connection fails, an error message is printed out.'''
    HOST = input('HOST :')
    PORT = eval(input('PORT :'))
    try:
        protocol_socket = socket.socket()
        protocol_socket.connect((HOST,PORT))
        send = protocol_socket.makefile('w')
        read = protocol_socket.makefile('r')
        return protocol(socket = protocol_socket, output = send, input = read)
    except:
        print("UNABLE TO CONNECT")

def recieve_message(Connection: protocol)->str:
    '''This function obtains the messages sent by the server using a namedtuple.'''
    message = Connection.input.readline()[:-1]
    return message
    
def greeting_message(Connection: protocol)-> str:
    '''This function creates the greeting message which is sent to the server using a namedtuple.'''
    user = input("Username : ")
    user1 = user.strip()
    message = 'I32CFSP_HELLO ' + user1 + '\r\n'
    Connection.output.write(message)
    Connection.output.flush()

def send_message(Connection: protocol, Message: str)->None:
    '''This function sends messages to the server using a namedtuple.'''
    Connection.output.write(Message + '\r\n')
    Connection.output.flush()
    
def close_connection(Connection: socket)->None:
    '''This function closes the socket connection.'''
    Connection.socket.close()
