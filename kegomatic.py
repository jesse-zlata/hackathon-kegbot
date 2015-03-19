#!/usr/bin/python
import RPi.GPIO as GPIO
from flowmeter import *

#boardRevision = GPIO.RPI_REVISION


# set up the flow meters
fm = FlowMeter('metric', 'left_tap')
fm2 = FlowMeter('metric', 'right_tap')


class FlowMeters():

    def __init__(self):
        GPIO.setmode(GPIO.BCM) # use real GPIO numbering
        GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Beer, on Pin 17
    def doAClick(channel):
        print "Left Tap Pouring"
        currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
        if fm.enabled:
            fm.update(currentTime)


    # Root Beer, on Pin 27.
    def doAClick2(channel):
        print "Right Tap Pouting"
        currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
        if fm2.enabled:
            fm2.update(currentTime)

GPIO.add_event_detect(17, GPIO.RISING, callback=doAClick, bouncetime=20) # Beer, on Pin 23
GPIO.add_event_detect(27, GPIO.RISING, callback=doAClick2, bouncetime=20) # Root Beer, on Pin 24
