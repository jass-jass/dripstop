from machine import Pin
import multiprocessing
import time

def read(pin, previous_time):
    current_time = time.time()
    if(current_time - previous_time > 1):
        return pin.value(), current_time

def write(pin, val, previous_time):
    current_time = time.time()
    if(current_time - previous_time > 1):
        pin.value(val)
        return current_time
