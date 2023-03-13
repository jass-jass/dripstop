from machine import Pin, Timer
import time 


## PWM Generate
timer = Timer(0)
pwm_out = Pin(23, Pin.OUT)

def pwm_off(timer):
    timer.init(period=5000, mode=Timer.ONE_SHOT, callback=pwm_on)
    pwm_out.off()

def pwm_on(timer):
    timer.init(period=1000, mode=Timer.ONE_SHOT, callback=pwm_off)
    pwm_out.on()

###

## PWM Read
read_timer = Timer(1)



while True:
    start = time.time()
    timer.init(period=1000, mode=Timer.ONE_SHOT, callback=pwm_off)
