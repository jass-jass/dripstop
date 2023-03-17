from machine import Pin, PWM, Timer, freq
import time, math
import machine as mac

mac.freq(240000000)


timer = Timer(1)
pwm_out = Pin(23, Pin.OUT)

def pwm_off(timer):
    timer.init(period=7, mode=Timer.ONE_SHOT, callback=pwm_on)
    pwm_out.off()

def pwm_on(timer):
    timer.init(period=3, mode=Timer.ONE_SHOT, callback=pwm_off)
    pwm_out.on()

timer.init(period=1, mode=Timer.ONE_SHOT, callback=pwm_on)


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
    on_time = time.ticks_cpu()
    if on_count < samples:
        on_sum = on_sum + on_time - off_time
    if on_count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_off, trigger = Pin.IRQ_RISING)
    on_count = on_count - 1

def timer_off(data):
    global off_time
    global off_sum
    global off_count
    off_time = time.ticks_cpu()
    if off_count < samples:
        off_sum = off_sum + off_time - on_time
    if off_count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)
    off_count = off_count - 1


data = Pin(34, Pin.IN)
data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)


while True:
    if on_count == 0 or off_count == 0:
        on = (on_sum / (samples - 1 - on_count)) / 240000000 - 0.00025
        off = off_sum / (samples - 1 - off_count) / 240000000 - 0.00025
        t_period = (on + off)
        print("on ", on, "off ", off, "frequency ", (t_period))
        on_sum = 0
        off_sum = 0
        on_count = off_count = samples
        data.irq(handler = timer_on, trigger = Pin.IRQ_RISING)
