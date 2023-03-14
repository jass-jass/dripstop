from machine import Pin, Timer
import time 


## PWM Generate
timer = Timer(0)
pwm_out = Pin(23, Pin.OUT)

def pwm_off(timer):
    timer.init(period=200, mode=Timer.ONE_SHOT, callback=pwm_on)
    pwm_out.off()

def pwm_on(timer):
    timer.init(period=500, mode=Timer.ONE_SHOT, callback=pwm_off)
    pwm_out.on()

timer.init(period=700, mode=Timer.ONE_SHOT, callback=pwm_off)
###



## PWM Read
read_timer = Timer(1)
read_timer.init(period= 10000)

count = 10
on_time = 0
off_time = 0
on_sum = 0
off_sum = 0

def timer_on(data):
    global on_time
    global on_sum
    global count
    count = count - 1
    on_time = read_timer.value()
    print(on_time, 'on')
    on_sum = on_sum + on_time
    if count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_off, trigger = Pin.IRQ_RISING)
        read_timer.init(period= 10000)

def timer_off(data):
    global off_time
    global off_sum
    global count
    count = count - 1
    off_time = read_timer.value()
    print(off_time, 'off')
    off_sum = off_sum + off_time
    if count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)
        read_timer.init(period= 10000)

data = Pin(34, Pin.IN)
data.irq(handler = timer_on, trigger = Pin.IRQ_RISING)
###

while True:
    if count == 0:
        count = 10
        on_time = on_sum * 2 / count
        off_time = off_sum *2 / count
        t_period = on_time + off_time
        print("on ", on_time, "off ", off_time, "frequency ", (1/t_period))
        on_sum = 0
        off_sum = 0
        data.irq(handler = timer_on, trigger = Pin.IRQ_RISING)
