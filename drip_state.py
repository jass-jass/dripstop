from machine import Pin, PWM
from time import sleep
import _thread



def pulse_generate():
    pulse_pin = Pin(22, Pin.OUT)
    pulse = PWM(pulse_pin)
    pulse.freq(700)
    while True:
        for i in range(1024):
            pulse.duty(i)
            sleep(2)

_thread.start_new_thread(pulse_generate, ())



read = Pin(34, Pin.IN)

def pulse_read():
