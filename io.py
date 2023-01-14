from machine import Pin
import _thread
import pyb

def rd(pin_number):
    in_pin = Pin(pin_number, Pin.IN)
    prev_time = pyb.millis()
    while True:
       if(pyb.millis()-prev_time > 1):
           prev_time = pyb.millis()
           pin_value = in_pin.value()

def read(pin_number):
    _thread.start_new_thread(rd(pin_number))

def wr(pin_number, val):
    out_pin = Pin(pin_number, Pin.OUT)
    prev_time = pyb.millis()
    while True:
       if(not out_pin.value()-val):
           prev_time = pyb.millis()
           pin_value = in_pin.value(val)
        
def write(pin_number, val):
    _thread.start_new_thread(wr(pin_number, val))