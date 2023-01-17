from machine import Pin
import _thread
import time

def rd(pin_number, val):
    in_pin = Pin(pin_number, Pin.IN)
    prev_time = time.time()
    while True:
       if(time.time()-prev_time > 1):
           prev_time = time.time()
           val = in_pin.value()

def read(pin_number, val):
    _thread.start_new_thread(rd(pin_number))

def wr(pin_number, val):
    out_pin = Pin(pin_number, Pin.OUT)
    prev_time = time.time()
    while True:
       if(not out_pin.value()-val):
           prev_time = time.time()
           in_pin.value(val)
        
def write(pin_number, val):
    _thread.start_new_thread(wr(pin_number, val))
