#!/usr/bin/python
import RPi.GPIO as GPIO


class FlowMeter():

    def __init__(self, pin, udp_sender):
        #17, 27
        GPIO.setmode(GPIO.BCM) # use real GPIO numbering
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.RISING, callback=self.doAClick, bouncetime=20)
        self.udp_sender = udp_sender

    def doAClick(channel):
        print "Left Tap Pouring"
        self.udp_sender.UdpMessage(int(time.time() * 1000.0))
