import socket
from flask import jsonify


class UdpMessage():

    def __init__(self, ip, port, platform, sensor):
        self.ip = ip
        self.port = port
        self.platform = platform
        self.sensor = sensor

    def send_message(self, data):
        message = {"platform": self.platform,
                   "sensor": self.sensor,
                   "data": data}
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)
        sock.sendto(jsonify(message), (self.ip, self.port))