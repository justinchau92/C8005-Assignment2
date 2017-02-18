# -----------------------------------------------------------------------------
# FUNCTION:       EDGE EPO server
#
# DATE:           January 06, 2017
#
# DESIGNERS:      Paul Cabanez, Justin Chau
#
# PROGRAMMERS:    Paul Cabanez, Justin Chau
#
# NOTES: receives an echo from the client and rplies back, utilizes edge level trigging
#
#
#
#
#
# ----------------------------------------------------------------------------*/

import socket
import select
import thread
import time
import datetime
import sys


#---------------------------------------------------
# getTime()
# Time function that gives the current time
# returns timeStamp
#---------------------------------------------------
def getTime():
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    return timeStamp

#---------------------------------------------------
# edgeFunction(hostIP, port)
# General function to run the epoll (edge triggered) server
# hostIP = IP of the server
# port = port number you want to use for the server
#---------------------------------------------------
def edgeFunction(hostIP, port):

	#variables
    bufferSize = 1024
    running = True
    SentTotal = 0
    ReceivedTotal = 0
    sSize = 0
    rSize = 0
    counter = 0
    requestCounter = 0
    connections = {}
    
    #create the server socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
    #non-blocking mode
    serverSocket.setblocking(0)
    #create epoll
    epoll = select.epoll()
    
    address = (hostIP, port)
    
    #add socket to connections
    connections.update({serverSocket.fileno(): serverSocket})
    #allows a bind to occur for reusedaddr
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    #socket binds
    serverSocket.bind(address)
    
    print ("Server is listening for connections\n")
    serverSocket.listen(10000)
    
    
    #read when socket accepts connection
    epoll.register(serverSocket.fileno(), select.EPOLLIN | select.EPOLLET)
    
    try:
    	
    	while running:
			
			#checking epoll for any events
			events = epoll.poll(-1)
			
			for fileno, event in events:
				if fileno == serverSocket.fileno():
					while running:
						try:
							clientConnection, clientAddress = serverSocket.accept()
							counter += 1
							
							connections.update({clientConnection.fileno(): clientConnection})
							#set new socket to non blocking
							clientConnection.setblocking(0)
							#register the epoll 
							epoll.register(clientConnection.fileno(), select.EPOLLIN | select.EPOLLET)
							
							text_file.write("\n\n" +str(clientAddress) + " connected")
							text_file.write("\nNumber of connected clients: " + str(counter))
					
							print (str(clientAddress) + " connected.")
							print ("\nNumber of connected clients: " + str(counter))
						except socket.error:
							break
							
				elif event & select.EPOLLIN:
					rSock = connections.get(fileno)
					#receieve the data and send it back
					try:
						data = rSock.recv(bufferSize)
						clientAddress, clientSocket = rSock.getpeername()
						rSize = len(data)
						ReceivedTotal += rSize
						sSize = len(data)
						SentTotal += sSize
						rSock.send(data)
						
						requestCounter += 1
						
						#if client sends a quit message close the socket
						if data == 'quit':
							rSock.close()
						
					except socket.error:
						pass
        			
    except KeyboardInterrupt:
    	Close(epoll,serverSocket,counter, ReceivedTotal, SentTotal, requestCounter)
        				
#----------------------------------------------------------------------------
# Close Function
# Function to turn off the server
#
# epoll = epoll object
# serverSocket = the server socket opened
# counter = number of connections
# ReceivedData = Amount of data received from the clients
# SentData = Amount of data sent back to the clients
# Request Counter = number of request the server got from the client
#-----------------------------------------------------------------------------   
    				
def Close(epoll,serverSocket,counter, ReceivedData, SentData, requestCounter):
    print ("Shutting down Server...")
    epoll.unregister(serverSocket.fileno())
    epoll.close()
    serverSocket.close()
    
    text_file.write("\n\nTotal # of client connections: " + str(counter))
    text_file.write("\nTotal # of request: " + str(requestCounter))
    text_file.write("\nTotal data received: " + str(ReceivedData))
    text_file.write("\nTotal data sent: " + str(SentData))
    text_file.close()
    sys.exit()


if __name__ == '__main__':

    serverIP = '192.168.0.5'#raw_input('Enter your server IP \n')
    port = 2017#int(raw_input('What port would you like to use?\n'))


    # Create and initialize the text file with the date in the filename in the logfiles directory
    filename = str(getTime()) + "_edgeserverlog.txt"
    text_file = open(filename, "w")
    
    edgeFunction(serverIP,port)
    
   
