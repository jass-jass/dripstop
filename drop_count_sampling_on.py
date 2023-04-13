from machine import Pin, PWM, Timer, freq, I2C
from i2c_lcd import I2cLcd
import time, math
import machine as mac

mac.freq(240000000)


#################### PWM generation ############################
timer = Timer(1)
pwm_out = Pin(23, Pin.OUT)

def pwm_off(timer):
    timer.init(period=200, mode=Timer.ONE_SHOT, callback=pwm_on)
    pwm_out.off()
def pwm_on(timer):
    timer.init(period=500, mode=Timer.ONE_SHOT, callback=pwm_off)
    pwm_out.on()

timer.init(period=200, mode=Timer.ONE_SHOT, callback=pwm_on)
################################################################


##################### OLED display #############################
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
addr = i2c.scan()
print(addr)


i2c = I2C(0)
display = I2cLcd(i2c, addr[0], 4, 20)
display.putstr('hi')


def oled_disp(text, numeral):
    display.clear()
    display.putstr(text)
    display.move_to(0, 1)
    display.putstr(str(numeral))
#################################################################'''


####################### Frequency count #########################
samples = 10
count = samples + 1
prev_time = 0
curr_time = 0
sum_time = 0

data = Pin(34, Pin.IN)

prev_time = 0
curr_time = 0
read = 0

while True:
    freq_size = 10
    freq = []
    while freq_size:
        flag = 1
        temp = 1
        data_size = 0
        while temp != data.value():
            pass
        while True:
            while True:
                curr_time = time.ticks_us()
                if curr_time - prev_time > 250:
                    read = data.value()
                    break
            prev_time = curr_time
            if read ^ temp:
                flag = flag - 1
                temp = read
            if data_size >  12000:
                if read:
                    t = -2
                else:
                    t = -1
                oled_disp('period', t)
                freq.append(t) 
                freq_size = freq_size - 1
                break
            if flag:
                data_size = data_size + 1 
            else:
                t = (data_size * 0.25) / 0.989
                oled_disp('period', t)
                freq.append(t) 
                freq_size = freq_size - 1
                break
    l = sorted(freq)
    period = l[int(len(l)/ 2)]
    oled_disp('freq', (1000/period))
