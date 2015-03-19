from ultrasound import *
import time
import threading
import socket

ultrasound = Ultrasound()

UDP_IP = "192.168.1.145" # ip of stat processor
UDP_PORT = 5005


def collect_range():
    while True:
        message = ultrasound.get_distance()
        str_message = str(message)
        print str_message
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.sendto(str_message, (UDP_IP, UDP_PORT))

range_thread = threading.Thread(target=collect_range)
range_thread.daemon = True
range_thread.start()

while True:
    time.sleep(1)