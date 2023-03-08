from machine import Pin
from time import sleep
#import _thread

count = 0

ledr = Pin(4, Pin.OUT)
button = Pin(23, Pin.IN)
ledg = Pin(5, Pin.OUT)

def state_on(ledg):
    ledg.on()
    sleep(5)

def state_off(ledg):
    ledg.off()
    sleep(5)

def state_status(button, ledr):
    for i in range(50000):
        ledr.value(button.value())

def print_msg(no):
    print('Loop ', no)

while True:
    state_on(ledg)
    state_off(ledg)
    state_status(button, ledr)
    count = count + 1
    print_msg(count)
