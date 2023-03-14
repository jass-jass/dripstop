from machine import Pin, Timer
import time 


## PWM Generate
timer = Timer(0)
pwm_out = Pin(23, Pin.OUT)

def pwm_off(timer):
    timer.init(period=500, mode=Timer.ONE_SHOT, callback=pwm_on)
    pwm_out.off()

def pwm_on(timer):
    timer.init(period=1000, mode=Timer.ONE_SHOT, callback=pwm_off)
    pwm_out.on()

timer.init(period=1000, mode=Timer.ONE_SHOT, callback=pwm_off)
###



## PWM Read
read_timer = Timer(1)

on_time = 0
off_time = 0

def timer_on(data):
    global on_time
    on_time  = time.time_ns() / 1000000
    data.irq(handler = timer_off, trigger = Pin.IRQ_RISING)
    print(on_time-off_time)

def timer_off(data):
    global off_time
    off_time = time.time_ns() / 1000000
    data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)
    print(off_time - on_time)

data = Pin(34, Pin.IN)
data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)
###
