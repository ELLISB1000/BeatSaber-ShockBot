import websocket
import time
import datetime
import json
import RPi.GPIO as GPIO
from websocket import create_connection

# Setup GPIO as output
PIN = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.LOW)

# Variable
numfail = 0
maxfail = 3
deltafail = 2
start = datetime.datetime.now()

def shock():
    print('Shock')
    GPIO.output(PIN, GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(PIN, GPIO.LOW)
    self.start = datetime.datetime.now()


class OnMessage():
    def __init__(self):
        # Variable
        self.numfail = 0
        self.maxfail = 2
        self.deltafail = 2
        self.start = datetime.datetime.now()

    def __call__(self, ws, message):
        evtjson = json.loads(message)
        evt = evtjson["event"]
        if(evt == "noteMissed" or evt == "bombHit"):
            self.end = datetime.datetime.now()
            delta = self.end - self.start
            if (delta.seconds < self.deltafail and numfail > self.maxfail):
                self.start = datetime.datetime.now()
            elif (delta.seconds < self.deltafail and numfail < self.maxfail):
                self.start = datetime.datetime.now()
                shock()
                self.numfail = numfail + 1
            elif (delta.seconds > deltafail and numfail > maxfail):
                self.start = datetime.datetime.now()
                shock()
                self.numfail = 0
                self.numfail = numfail + 1
            elif (delta.seconds > self.deltafail and numfail < self.maxfail):
                self.start = datetime.datetime.now()
                shock()
                self.numfail = 0
                self.numfail = numfail + 1
            else:
                print('Error processing Event: ' + evt)
        elif(evt == "menu"):
            print ("In Menu, Waiting for Song to Start") 

on_message = OnMessage()

def on_error(ws, error):
    print("Error")

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print ("Opened Session")

websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://192.168.1.39:6557/socket/", on_message = on_message, on_error = on_error, on_close = on_close)
ws.on_open = on_open
ws.run_forever()