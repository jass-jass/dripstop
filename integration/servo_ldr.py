from time import sleep
from machine import Pin, PWM, Timer, freq, I2C
import servo, sh1106, time, math, machine
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

machine.freq(240000000)


#####################  Instantiation  #########################
# servo
servo = servo.Servo(4)
# i2c lcd
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
addr = i2c.scan()
totalRows = 4
totalColumns = 20
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
# ldr
data = Pin(34, Pin.IN)
###############################################################



#########################  Servo  ##############################
def control_servo(mark, frequency):
    # greater the frequency, lesser the angle
    if mark > frequency:
        angle = servo.read() + 2
    else:
        angle = servo.read() - 2
    servo.write(angle)
################################################################


########################### LCD  ###############################
def display_lcd(text):
    lcd.clear()
    lcd.move_to(0,0)
    if frequency < 0:
        lcd.putstr("ERR")
    else:
        lcd.putstr(text)
################################################################
   
   
   
###################### Frequency count #########################
def get_freq() -> float:
    samples = 10
    count = samples + 1
    prev_time = 0
    curr_time = 0
    sum_time = 0
    read = 0
    while True:
        freq_size = 10
        freq = []
        while freq_size:
            flag = 2
            temp = 0
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
                if data_size >  3000:
                    if read:
                        freq.append(0)
                    else:
                        freq.append(-1)
                    freq_size = freq_size - 1
                    break
                if flag:
                    data_size = data_size + 1 
                else:
                    freq.append(1000/ (data_size * 0.25)) 
                    freq_size = freq_size - 1
                    break
    l = sorted(freq)
    return (l[int(len(l)/ 2)])
################################################################



#########################  start  ##############################
servo.write(0)
display_lcd('Place tube')
sleep(15)
lcd.clear()
lcd.move_to(0,0)
display_lcd('Closing Tube')
servo.write(90)
################################################################
    
    
while True:
    # 0.6 to 25 Hz
    mark = 25.0
    while mark >= 1:
        flag = 0
        while True:
            freq = get_freq()
            display_lcd(mark, freq)
            if mark ^ freq:
                control_servo(freq)
            else:
                if flag:
                    break
                flag = flag + 1
