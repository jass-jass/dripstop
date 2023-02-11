from machine import Pin, Timer
from time import sleep
import io
import servo



######## Initialization of pins ########
# Inputs
load_cell_pin = Pin(dot, Pin.IN)
# Outputs
buzzer_pin    = Pin(dot, Pin.OUT)
servo_pin     = Pin(dot, Pin.OUT)



### Variables for pin status of pins ###
# shared for both core functions
#load_value    = False



######## Timer Interrupt handler #######
def ISR_Timer(arg):
    timer_10_sec.deinit()      # turn off timer
    servo_pin.turn()           # 85 degrees
    buzzer_pin.value(0)        # turn off buzzer



### Interrupt handler for 10% weight ###
def ISR_10_percent():
    timer_10_sec = Timer(1)
    timer_10_sec.init(period = 10000, mode = Timer.ONE_SHOT, callback = ISR_Timer)
    
    

### Interrupt definition 10% weight ###
Interrupt.irq(trigger = Pin.IRQ_FALLING, handler = ISR_10_percent)



def critical_core():
    #global load_value
    time_stamp = 0
    while True:
        load_value, time_stamp = io.read(load_cell_pin, time_stamp)
