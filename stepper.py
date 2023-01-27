from machine import Pin
import time

pin1 = Pin(4, Pin.OUT)
pin2 = Pin(16, Pin.OUT)
pin3 = Pin(17, Pin.OUT)
pin4 = Pin(18, Pin.OUT)

seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1]]

steps = 50

delay = 1

for i in range(steps):
    for halfstep in range(8):
        for pin in range(4):
            pin_obj = eval("pin" + str(pin+1))
            pin_obj.value(seq[halfstep][pin])
        time.sleep(delay)
