from machine import Pin, PWM

def turn(pin_number ,control):
    servo = PWM(Pin(pin_number), freq=50)
    while True:
        servo.duty(control)
