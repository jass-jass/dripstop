from machine import Pin, Timer
import time



timer = Timer(0)
pwm_out = Pin(23, Pin.OUT)

def pwm_off(timer):
    timer.init(period=2, mode=Timer.ONE_SHOT, callback=pwm_on)
    pwm_out.off()

def pwm_on(timer):
    timer.init(period=5, mode=Timer.ONE_SHOT, callback=pwm_off)
    pwm_out.on()

timer.init(period=5, mode=Timer.ONE_SHOT, callback=pwm_off)


samples = 10
count = samples + 1
on_time = 0
off_time = 0
on_sum = 0
off_sum = 0


def timer_on(data):
    global on_time
    global on_sum
    global count
    count = count - 1
    on_time = time.ticks_us()
    print(on_time, 'on')
    if count < samples:
        on_sum = on_sum + on_time - off_time
    if count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_off, trigger = Pin.IRQ_RISING)

def timer_off(data):
    global off_time
    global off_sum
    global count
    count = count - 1
    off_time = time.ticks_us()
    print(off_time, 'off')
    if count < samples:
        off_sum = off_sum + off_time - on_time
    if count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)


data = Pin(34, Pin.IN)
data.irq(handler = timer_on, trigger = Pin.IRQ_RISING)


while True:
    if count == 0:
        count = samples + 1
        on = on_sum / samples
        off = off_sum / samples
        t_period = on_time + off_time
        print("on ", on/1000, "off ", off/1000, "frequency ", (1000000/t_period))
        on_sum = 0
        off_sum = 0
        data.irq(handler = timer_on, trigger = Pin.IRQ_RISING)
