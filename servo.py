from machine import Pin, PWM
from time import sleep

def turn(pin_number ,control):
    servo = PWM(Pin(pin_number), freq=15)
    servo.duty(control)
        
turn(4, 40)
sleep(2)
turn(4, 10)

# at freq = 15, the motor covers 180 degrees
# from control 10 to control 40 

# from machine import Pin, PWM
# from time import sleep
# 
# def turn(pin_number ,control):
#     servo = PWM(Pin(pin_number), freq=50)
#     servo.duty(control)
#         
# turn(4, 31)
# sleep(2)
# turn(4, 133)
