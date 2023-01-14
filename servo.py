from machine import Pin, PWM
import pyb
import "io.py"

def turn(pin_number, control):
    servo = PWM(Pin(Pin(pin_number), freq(50)))
    while True:
        duty = map(control, 40, 80, 0, 120)
        servo.duty(duty)