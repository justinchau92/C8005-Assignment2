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

def getTime():
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    return timeStamp

def ThreadFunction(clientsocket, clientaddr):
    global ReceivedData
    global SentData
    while True:

        #Receive data from client
        data = clientsocket.recv(bufferSize)
        #Get client IP and port
        clientIP, clientSocket = clientsocket.getpeername()

        #Add to total amount of data transfered
        ReceiveDataSize = len(data)
        ReceivedData += ReceiveDataSize

        #LOg the received data
        text_file.write(str(getTime()) + "__ Size of data received (" + clientIP + ":" + str(clientSocket) + ") = " + str(ReceiveDataSize) + '\n')

        #Send data
        clientsocket.send(data)
        SentDataSize = len(data)
        SentData += SentDataSize

        #Log the sent data
        text_file.write(str(getTime()) + "__ Size of data sent (" + clientIP + ":" + str(clientSocket) + ") = " + str(SentDataSize) + '\n')


def Close(counter, ReceivedData, SentData):
    print ("Shutting down Server...")
    serversocket.close()
    text_file.write("\n\nTotal # of connections: " + str(counter))
    text_file.write("\nTotal data received: " + str(ReceivedData))
    text_file.write("\nTotal data sent: " + str(SentData))
    text_file.close()
    sys.exit()


if __name__ == '__main__':

    serverIP = raw_input('Enter your server IP \n')
    port = int(raw_input('What port would you like to use?\n'))

    # Maintain how many connections
    connections = []
    counter = 0

    # Maintain amount of data sent to and from server
    ReceivedData = 0
    SentData = 0
    bufferSize = 1024

    # Create and initialize the text file with the date in the filename in the logfiles directory
    text_file = open("MultiThreadedServerLog.txt", "w")
    address = (serverIP, port)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind server to port
    serversocket.bind(address)

    # The listen backlog queue size
    serversocket.listen(50)
    print ("Server is listening for connections\n")

    try:
        while 1:
            # Accept client connections, increment number of connections
            clientsocket, clientaddr = serversocket.accept()
            counter += 1

            # Log client information
            print (str(clientaddr) + " : " + " Just Connected. \n Currently connected clients: " + str(counter) + "\n")
            text_file.write(str(getTime()) + " - " + str(clientaddr) + " : " + " Just Connected. \n Currently connected clients: " + str(counter) + "\n")
            clientThread = threading.Thread(target=ThreadFunction, args=(clientsocket, clientaddr))
            clientThread.start()

    except KeyboardInterrupt:
        print ("Keyboard interrupt occurred.")
        Close(counter, ReceivedData, SentData)