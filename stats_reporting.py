from ultrasound import *
import threading
import socket

ultrasound = Ultrasound()

UDP_IP = "127.0.0.1"
UDP_PORT = 5005


def ultrasound_stuff():
    while True:
        message = ultrasound.checkForHuman()
        print message
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.sendto(message, (UDP_IP, UDP_PORT))

threads = []
range_thread = threading.Thread(target=ultrasound_stuff)

range_thread.daemon = True

threads.append(range_thread)

range_thread.start()

