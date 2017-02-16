# -----------------------------------------------------------------------------
# FUNCTION:       Client
#
# DATE:           January 06, 2017
#
# DESIGNERS:      Paul Cabanez, Justin Chau
#
# PROGRAMMERS:    Paul Cabanez, Justin Chau
#
# NOTES: program sends strings to the server and will receive the string back in a reply
#
#
#
#
#
# ----------------------------------------------------------------------------*/

from socket import *
import threading
import time
import random
import sys
import datetime


serverIP = ""
port = 8005
message = ""
msgMultiple = 1


def getTime():
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    return timeStamp



def run(clientNumber):
    buffer = 1024

    global totalTime

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((serverIP, port))
    threadRTT = 0

    while 1:
        for _ in range(msgMultiple):
            cData = message + "  From: Client " + str(clientNumber)

            # Start timer and send data
            start = time.time()
            s.send(cData.encode('utf-8'))
            print "Sent: " + cData

            # Stop timer when data is received
            sData = s.recv(buffer)
            end = time.time()

            # Keep track of RTT and update total time
            response_time = end - start
            threadRTT += end - start
            totalTime += response_time
            print "Received: " + cData + '\n'
            t = random.randint(0, 9)
            time.sleep(t)

        # Log information of Client
        text_file.write(
            "\nClient " + str(clientNumber) + " RTT time taken for " + str(msgMultiple) + " messages was: " + str(
                threadRTT) + " seconds.")
        threadRTT = 0
        break


if __name__ == '__main__':
    serverIP = raw_input('Enter the server IP: ')
    port = int(input('Enter the port: '))
    clients = int(input('Enter number of clients: '))
    message = raw_input('Enter a message to send: ')
    msgMultiple = int(input('Enter the number of times you would like to send the message: '))

    # Initialize Log file
    text_file = open("ClientLog.txt", "w")

    # Used to maintain list of all running threads
    threads = []
    totalTime = 0

    # Create a seperate thread for each client
    for x in range(clients):
        thread = threading.Thread(target=run, args=[x])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    # Calculations for log data
    bytes = sys.getsizeof(message)
    totalRequests = clients * msgMultiple
    totalBytes = totalRequests * bytes
    averageRTT = totalTime / totalRequests
    # Output data
    print("Bytes sent in message was : " + str(bytes))
    print("Total Data sent was : " + str(totalBytes) + " Bytes.")
    print("Average RTT was : " + str(averageRTT) + " seconds.")
    print("Requests was : " + str(totalRequests))

    # Write data to log file
    text_file.write("\n\n Bytes sent in message was : " + str(bytes))
    text_file.write("\nTotal Data sent was : " + str(totalBytes) + " Bytes.")
    text_file.write("\nAverage RTT was : " + str(averageRTT) + " seconds.")
    text_file.write("\nRequests was : " + str(totalRequests))
