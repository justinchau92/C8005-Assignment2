# -----------------------------------------------------------------------------
# FUNCTION:       Multi-thread server
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

from Tkinter import *
import socket
import threading
import time
import datetime
import sys

#list of inputs you need
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

#--------------------------------------------
# ThreadedFunction 
# function that executes the send and receive
#
# clientsocket - socket of the specific client
# clientaddr - address of the specific client
#--------------------------------------------
def ThreadFunction(clientsocket, clientaddr):
    global ReceivedData
    global SentData
    global requests
    
    bufferSize = 1024
	
    while True:

        #Receive data from client
        data = clientsocket.recv(bufferSize)
        #Get client IP and port
        clientIP, clientSocket = clientsocket.getpeername()

        #Add to total amount of data transfered
        ReceiveDataSize = len(data)
        ReceivedData += ReceiveDataSize
        
        if ReceiveDataSize > 0:
			
			#LOg the received data
			text_file.write("\nReceived Data is " + str(ReceiveDataSize) + " from " + clientIP + ":" + str(clientSocket) + '\n')
			requests += 1
	
			#Send data
			clientsocket.send(data)
			SentDataSize = len(data)
			SentData += SentDataSize
	
			#Log the sent data
			text_file.write("\nSent Data is " + str(SentDataSize) + " from " + clientIP + ":" + str(clientSocket) + '\n')
        
#-------------------------------------
# ThreadRunner
# Creates the threads and executes the methods to them
#
# entries - the inputs from the GUI
#
#------------------------------------- 
def ThreadRunner(entries):

    counter = 0
    request = 0
    address = (entries[0][1].get(), int(entries[1][1].get()))
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind server to port
    serversocket.bind(address)

    # The listen backlog queue size
    serversocket.listen(50)
    print ("Server is listening...\n")

    try:
        while 1:
            # Accept client connections, increment number of connections
            clientsocket, clientaddr = serversocket.accept()
            counter += 1

            # Log client information
            text_file.write("\n\n" +str(clientaddr) + " connected")
            text_file.write("\nNumber of connected clients: " + str(counter) + "\n")
            print("\n\n" +str(clientaddr) + " connected")
            print("\nNumber of connected clients: " + str(counter))
            clientThread = threading.Thread(target=ThreadFunction, args=(clientsocket, clientaddr))
            clientThread.daemon = True
            clientThread.start()

    except KeyboardInterrupt:
    	Close(serversocket,counter, ReceivedData, SentData,requests)        

        				
#----------------------------------------------------------------------------
# Close Function
# Function to turn off the server
#
# serverSocket = the server socket opened
# counter = number of connections
# ReceivedData = Amount of data received from the clients
# SentData = Amount of data sent back to the clients
# Request Counter = number of request the server got from the client
#-----------------------------------------------------------------------------  
def Close(serversocket, counter, ReceivedData, SentData,requests):
    serversocket.close()
    text_file.write("\n\nTotal # of connections: " + str(counter))
    text_file.write("\nTotal # of requests: " + str(requests))
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

    #serverIP = '192.168.0.16' #raw_input('Enter your server IP \n')
    #port = 2017 #int(raw_input('Enter the port you want to use \n'))

	# Maintain how many connections
    connections = []


    # Maintain amount of data sent to and from server
    ReceivedData = 0
    SentData = 0
    requests = 0

    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M')

    # Create and initialize the text file with the date in the filename in the logfiles directory
    text_file = open(str(getTime()) + "_MultiThreadedServerLog.txt", "w")
    
    root = Tk()
    ents = makeform(root,fields)
    
    buttonFrame = Frame(root)
    buttonFrame.pack(side=TOP,padx=5,pady=5)
    
    b1 = Button(root, text='Start Server', command=(lambda e=ents: ThreadRunner(e)))
    b1.pack(in_=buttonFrame , side=LEFT, padx=5,pady=5)

    
    root.title("MultiThreaded Server")
    root.mainloop()
    

