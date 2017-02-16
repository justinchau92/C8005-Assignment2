# -----------------------------------------------------------------------------
# FUNCTION:       EDGE EPO server
#
# DATE:           January 06, 2017
#
# DESIGNERS:      Paul Cabanez, Justin Chau
#
# PROGRAMMERS:    Paul Cabanez, Justin Chau
#
# NOTES: receives an echo from the client and rplies back, utilizes multi-threading
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

def getTime():
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    return timeStamp

def edgeFunction(hostIP, port):

    bufferSize = 1024
    SentTotal = 0
    ReceivedTotal = 0
    sSize = 0
    rSize = 0
    counter = 0
    connections = {}
    
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	
	
    #non-blocking mode
    serverSocket.setblocking(0)
    #create epoll
    epoll = select.epoll()
    
    connections.update({serverSocket.fileno(): serverSocket})
    serverSocket = setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR,1)
    serverSocket.bind(hostIP,port)
    serverSocket.listen(socket.SOMAXCONN)
    #read when socket accepts connection
    epoll.register(serverSocket.fileno(), select.EPOLLIN | select.EPOLLET)
    
    try:
    	
    	while True:
    	
			#checking epoll for any events
			events = epoll.poll(-1)
			
			for fileno, event in events:
				if fileno == serverSocket.fileno():
					while true:
						try:
							clientConnection, cilentAddress = serverSocket.accept()
							counter += 1
							
							connections.update({cilentConnection.fileno(): clientConnection})
							#set new socket to non blocking
							clientConnection.setblocking(0)
							epoll.register(clientConnection.fileno(), select.EPOLLIN)
							
							text_file.write(str(clientAddres) + " connected")
							text_file.write("Number of connected clients: " + str(counter))
							print (str(clientAddress) + " connected.")
							print ("Number of connected clients: " + str(counter))
						except:
							break
				elif event & select.EPOLLIN:
					rSock = connections.get(fileno)
					try:
						data = rSock.recv(bufferSize)
						clientAddress, clientSocket = rSock.getpeername()
						rSize = len(data)
						ReceivedTotal += rSize
						sSize = len(data)
						SentTotal += sSize
						rSock.send(data)
						
						text_file.write("Received Size is " +str(rSize) + " from " +clientAddress+ ":" +str(clientSocket))
						text_file.write("Sent Data Size " +str(sSize) + " back to " + clientAddress+ ":" + str(clientSocket))
					except:
						pass
        			
    except KeyboardInterrupt:
    	close(epoll,severSocket,counter, ReceivedTotal, SentTotal)
        				
        				
def Close(epoll,serverSocket,counter, ReceivedData, SentData):
    print ("Shutting down Server...")
    serverSocket.close()
    text_file.write("\n\nTotal # of connections: " + str(counter))
    text_file.write("\nTotal data received: " + str(ReceivedData))
    text_file.write("\nTotal data sent: " + str(SentData))
    text_file.close()
    sys.exit()


if __name__ == '__main__':

    serverIP = raw_input('Enter your server IP \n')
    port = int(raw_input('What port would you like to use?\n'))


    # Create and initialize the text file with the date in the filename in the logfiles directory
    filename = str(getTime()) + "_edgeserverlog.txt"
    text_file = open(filename, "w")
    
    edgeFunction(serverIP,port)
    
   