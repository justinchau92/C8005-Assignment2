# -----------------------------------------------------------------------------
# FUNCTION:       Select EPO server
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

def SelectFunction(hostIP, port):
	
    bufferSize = 1024
    running = True
    SentTotal = 0
    ReceivedTotal = 0
    sSize = 0
    rSize = 0
    counter = 0
    address = (hostIP, port)
    
    
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(address)
    
    serverSocket.listen(socket.SOMAXCONN)
    text_file.write("Server is now listening")
    
    #non-blocking mode
    serverSocket.setblocking(0)
    #create epoll
    epoll = select.epoll()
    
    #read when socket accepts connection
    epoll.register(serverSocket.fileno(), select.EPOLLIN)
    try:
    	connections = {}
    	while running:
    	
			#checking epoll for any events
			events = epoll.poll(-1)
			
			for fileno, event in events:
				if fileno == serverSocket.fileno():
					clientConnection, clientAddress = serverSocket.accept()
					counter += 1
					
					connections.update({clientConnection.fileno(): clientConnection})
					#set new socket to non blocking
					clientConnection.setblocking(0)
					epoll.register(clientConnection.fileno(), select.EPOLLIN)
					
					text_file.write("\n\n" +str(clientAddress) + " connected")
					text_file.write("\nNumber of connected clients: " + str(counter))
					
					print (str(clientAddress) + " connected.")
					print ("\nNumber of connected clients: " + str(counter))
					
				elif event & select.EPOLLIN:
					rSock = connections.get(fileno)
					data = rSock.recv(bufferSize)
					clientAddress, clientSocket = rSock.getpeername()
					rSize = len(data)
					
					ReceivedTotal += rSize
					sSize = len(data)
					SentTotal += sSize
					rSock.send(data)
					
					if rSize > 0:
						text_file.write("\n\nReceived Size is " + data + " from " +clientAddress+ ":" +str(clientSocket))
						text_file.write("\nSent Data Size " +str(sSize) + " back to " + clientAddress+ ":" + str(clientSocket))
					
						print("\n\nReceived Size is " + data + " from " +clientAddress+ ":" +str(clientSocket))
						print("\nSent Data Size " +str(sSize) + " back to " + clientAddress+ ":" + str(clientSocket))

					

				elif event & select.EPOLLERR:
					counter -= 1
				elif event & select.EPOLLHIP:
					counter -= 1
        			
    except KeyboardInterrupt:
    	Close(epoll,serverSocket,counter, ReceivedTotal, SentTotal)

        				
def Close(epoll,serverSocket,counter, ReceivedData, SentData):
    
    serverSocket.close()
    text_file.write("\n\nTotal # of connections: " + str(counter))
    text_file.write("\nTotal data received: " + str(ReceivedData))
    text_file.write("\nTotal data sent: " + str(SentData))
    text_file.close()
    print ("Shutting down Server...")
    sys.exit()


if __name__ == '__main__':

    serverIP = '192.168.0.5'#raw_input('Enter your server IP \n')
    port = 2017#int(raw_input('What port would you like to use?\n'))


    # Create and initialize the text file with the date in the filename in the logfiles directory
    filename = str(getTime()) + "_selectserverlog.txt"
    text_file = open(filename, "w")
    
    SelectFunction(serverIP,port)
    
   
