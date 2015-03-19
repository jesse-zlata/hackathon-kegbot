from ultrasound import *
import socket

ultrasound = Ultrasound()

UDP_IP = "127.0.0.1"
UDP_PORT = 5005


while True:
    message = ultrasound.checkForHuman()
    str_message = str(message)
    print str_message
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(str_message, (UDP_IP, UDP_PORT))

