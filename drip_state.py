from machine import Pin, PWM, Timer
import time



### Pulse Generate
timer = Timer(0)
pwm_out = Pin(23, Pin.OUT)

def pwm_off(timer):
    timer.init(period=39, mode=Timer.ONE_SHOT, callback=pwm_on)
    pwm_out.off()

def pwm_on(timer):
    timer.init(period=61, mode=Timer.ONE_SHOT, callback=pwm_off)
    pwm_out.on()

timer.init(period=1, mode=Timer.ONE_SHOT, callback=pwm_on)
###


### Frequency count
samples = 10
on_count = samples 
off_count = samples 
on_time = 0
off_time = 0
on_sum = 0
off_sum = 0


def timer_on(data):
    global on_time
    global on_sum
    global on_count
    on_time = time.ticks_us()
    if on_count < samples:
        on_sum = on_sum + on_time - off_time
    if on_count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_off, trigger = Pin.IRQ_RISING)
    on_count = on_count - 1
    #print(on_time/1000, 'on    ', on_sum)

def timer_off(data):
    global off_time
    global off_sum
    global off_count
    off_time = time.ticks_us()
    if off_count < samples:
        off_sum = off_sum + off_time - on_time
    if off_count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)
    off_count = off_count - 1
    #print(off_time/1000, 'off   ', off_sum)


data = Pin(34, Pin.IN)
data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)


while True:
    if on_count == 0 or off_count == 0:
        on = on_sum / ((samples - 1 - on_count)*2)
        off = off_sum / ((samples - 1 - off_count)*2)
        t_period = on_time + off_time
        print("on ", on/1000, "off ", off/1000, "frequency ", (1000000/t_period))
        on_sum = 0
        off_sum = 0
        on_count = off_count = samples
        data.irq(handler = timer_on, trigger = Pin.IRQ_RISING)
