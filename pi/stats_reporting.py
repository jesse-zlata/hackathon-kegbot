import threading
import time
import ultrasound
import flow
import udp


distance_meter = ultrasound.Ultrasound()

UDP_IP = "192.168.1.145" # ip of stat processor
UDP_PORT = 5005

lfm_sender = udp.UdpMessage(UDP_IP, UDP_PORT, "Kegbot 1", "left_flow_meter")
rfm_sender = udp.UdpMessage(UDP_IP, UDP_PORT, "Kegbot 1", "right_flow_meter")
range_sender = udp.UdpMessage(UDP_IP, UDP_PORT, "Kegbot 1", "range_meter")

left_fm = flow.FlowMeter(17, lfm_sender)
right_fm = flow.FlowMeter(27, rfm_sender)


def collect_range():
    while True:
        data = distance_meter.get_distance()
        range_sender.send_message(data)


range_thread = threading.Thread(target=collect_range)
range_thread.daemon = True
range_thread.start()

while True:
    time.sleep(1)