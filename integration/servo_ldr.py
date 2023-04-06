from time import sleep
from machine import Pin, PWM, Timer, freq, I2C
import servo, sh1106, time, math
import machine as mac

mac.freq(240000000)



servo = servo.Servo(4)

while True:
    angle = int(input('angle '))
    servo.write(angle)


##################### OLED display #############################
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
addr = i2c.scan()
print(addr)


i2c = I2C(0)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(2), addr[0], rotate=0, delay=0)


def oled_disp(text, numeral):
    display.sleep(False)
    display.fill(0)
    display.text(text, 0, 0, 1)
    display.text(str(numeral), 0, 8, 1)
    display.show()
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
        flag = 2
        temp = 0
        data_size = 0
        try:
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
                if data_size >  3000:
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
                    t = data_size * 0.25 #/ 1.85
                    oled_disp('period', t)
                    freq.append(t) 
                    freq_size = freq_size - 1
                    break
        except:
            oled_disp('meow', 1)
            time.sleep(2)
    l = sorted(freq)
    period = l[int(len(l)/ 2)]
    oled_disp('freq', (1000/period))
    control_servo(freq)
