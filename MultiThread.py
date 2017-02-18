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

import socket
import threading
import time
import datetime
import sys


def ThreadFunction(clientsocket, clientaddr):
    global ReceivedData
    global SentData
    global requests

    while True:

        #Receive data from client
        data = clientsocket.recv(bufferSize)
        #Get client IP and port
        clientIP, clientSocket = clientsocket.getpeername()

        #Add to total amount of data transfered
        ReceiveDataSize = len(data)
        ReceivedData += ReceiveDataSize

        #LOg the received data
        text_file.write("\nReceived Data is " + str(ReceiveDataSize) + " from " + clientIP + ":" + str(clientSocket) + '\n')
        requests += 1

        #Send data
        clientsocket.send(data)
        SentDataSize = len(data)
        SentData += SentDataSize

        #Log the sent data
        text_file.write("\nSent Data is " + str(SentDataSize) + " from " + clientIP + ":" + str(clientSocket) + '\n')
        
        if data == 'quit':
			clientsocket.close()


def Close(counter, ReceivedData, SentData, requests):
    serversocket.close()
    text_file.write("\n\nTotal # of connections: " + str(counter))
    text_file.write("\nTotal data received: " + str(ReceivedData))
    text_file.write("\nTotal data sent: " + str(SentData))
    text_file.write("\nTotal # of requests: " + str(requests))
    text_file.close()
    print ("Shutting down Server...")
    sys.exit()


if __name__ == '__main__':

    serverIP = '192.168.0.5' #raw_input('Enter your server IP \n')
    port = 2017 #int(raw_input('Enter the port you want to use \n'))

    # Maintain how many connections
    connections = []
    counter = 0
    requests = 0

    # Maintain amount of data sent to and from server
    ReceivedData = 0
    SentData = 0
    bufferSize = 1024

    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M')

    # Create and initialize the text file with the date in the filename in the logfiles directory
    text_file = open("MultiThreadedServerLog.txt", "w")
    address = (serverIP, port)
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
    	Close(counter, ReceivedData, SentData, requests)
