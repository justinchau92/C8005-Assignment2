# -----------------------------------------------------------------------------
# FUNCTION:       Select EPO server
#
# DATE:           January 06, 2017
#
# DESIGNERS:      Paul Cabanez, Justin Chau
#
# PROGRAMMERS:    Paul Cabanez, Justin Chau
#
# NOTES: receives an echo from the client and rplies back, utilizes select epoll level triggered
#
#
#
#
#
# ----------------------------------------------------------------------------*/

from Tkinter import *
import socket
import select
import thread
import time
import datetime
import sys

fields = 'Server IP' , 'Port'

#---------------------------------------------------
# getTime()
# Time function that gives the current time
# return timeStamp
#---------------------------------------------------
def getTime():
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    return timeStamp

#---------------------------------------------------
# SelectFunction(hostIP, port)
# General function to run the select (level triggered) server
# hostIP = IP of the server
# port = port number you want to use for the server
#---------------------------------------------------
def SelectFunction(entries):
	
    bufferSize = 1024
    running = True
    SentTotal = 0
    ReceivedTotal = 0
    sSize = 0
    rSize = 0
    counter = 0
    requestCounter = 0
    
    address = (entries[0][1].get(), int(entries[1][1].get()))
    
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(address)
    
    serverSocket.listen(socket.SOMAXCONN)
    print ("Server is listening...\n")
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
					
					#total size of bytes counting
					rSize = len(data)
					ReceivedTotal += rSize
					sSize = len(data)
					SentTotal += sSize
					rSock.send(data)
					
					
					requestCounter += 1
					text_file.write("\n\nReceived Size is " + str(rSize) + " from " +clientAddress+ ":" +str(clientSocket))
					text_file.write("\n\nSent Data Size " +str(sSize) + " back to " + clientAddress+ ":" + str(clientSocket))
				
					print("\n\nReceived Size is " + str(rSize) + " from " +clientAddress+ ":" +str(clientSocket))
					print("\n\nSent Data Size " +str(sSize) + " back to " + clientAddress+ ":" + str(clientSocket))
					
					#if client sends quit data close the socket
					if data == 'quit':
						rSock.close()
					
				elif event & select.EPOLLERR:
					counter -= 1
				elif event & select.EPOLLHIP:
					counter -= 1
        			
    except KeyboardInterrupt:
    	Close(epoll,serverSocket,counter, ReceivedTotal, SentTotal,requestCounter)


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
    
    epoll.unregister(serverSocket.fileno())
    epoll.close()
    serverSocket.close()
    text_file.write("\n\nTotal # of connections: " + str(counter))
    text_file.write("\nTotal # of requests: " + str(requestCounter))
    text_file.write("\nTotal data received: " + str(ReceivedData))
    text_file.write("\nTotal data sent: " + str(SentData))
    text_file.close()
    print ("Shutting down Server...")
    sys.exit()

#---------------------------------------------------
# makeform - method to create input box and labels
#
# root - the GUI form
# fields - list of inputs you want i.e (serverip, port)
#-------------------------------------------------
def makeform(root, fields):
	entries = []
	
	#for each field create an input
	for field in fields:
		row = Frame(root)
		lab = Label(row, width=15, text = field , anchor ='w')
		ent = Entry(row)
		ent.config(highlightbackground = "gray")
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		lab.pack(side=LEFT)
		ent.pack(side=RIGHT,expand=YES, fill=X)
		entries.append((field,ent))
	return entries
	

if __name__ == '__main__':

    serverIP = '192.168.0.16'#raw_input('Enter your server IP \n')
    port = 2018#int(raw_input('What port would you like to use?\n'))


    # Create and initialize the text file with the date in the filename in the logfiles directory
    filename = str(getTime()) + "_selectserverlog.txt"
    text_file = open(filename, "w")
    
    root = Tk()
    ents = makeform(root,fields)
    
    buttonFrame = Frame(root)
    buttonFrame.pack(side=TOP,padx=5,pady=5)
    
    b1 = Button(root, text='Start Server', command=(lambda e=ents: SelectFunction(e)))
    b1.pack(in_=buttonFrame , side=LEFT, padx=5,pady=5)
    
    root.title("Select Level Triggered Server")
    root.mainloop()
    
    
   
