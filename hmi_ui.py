import machine, pcf8574
from machine import Pin, I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep


class hmi(I2cLcd):
    
    totalRows = 4
    totalColumns = 20
    parameter = "volume"
    flag_irq = 0
    
    def __init__(self, addr_lcd, addr_pcf, int_pcf, id_dev):
        self.lcd = I2cLcd(i2c, addr_lcd, self.totalRows, self.totalColumns)
        self.volume = 0.0
        self.drip_rate = 0.0
        self.id = id_dev
        self.consumed = 0
        self.time_left = -1
        self.lcd.clear()
        ###                            ###
        self.pcf = pcf8574.PCF8574(i2c, addr_pcf)
        self.int = int_pcf
        self.button_dec = 0
        self.button_inc = 1
        self.button_dwn = 2
        self.button_sel = 3
        self.button_up = 4
        self.button_bck = 5
        self.button_strt = 6
        self.button_rst = 7
        
    def screen_blank(self):
        self.lcd.hide_cursor()
        self.lcd.clear()
        self.lcd.move_to(15, 0)
        self.lcd.putstr(("id"+str(self.id)))
        
    def isr_setup(self, pin):
        if self.pcf.pin(self.button_dwn)==0:
            self.lcd.move_to(0, 3)
            self.parameter = "rate"
        elif self.pcf.pin(self.button_up)==0:
            self.lcd.move_to(0, 2)
            self.parameter = "volume"
        elif self.pcf.pin(self.button_inc)==0:
            if self.parameter == "volume":
                self.lcd.move_to(7, 2)
                self.volume = self.volume + 0.1
                self.lcd.putstr(str(round(self.volume, 2)))
            else:
                self.lcd.move_to(10, 3)
                self.drip_rate = self.drip_rate + 0.1
                self.lcd.putstr(str(round(self.drip_rate, 2)))
        elif self.pcf.pin(self.button_dec)==0:
            if self.parameter == "volume":
                self.lcd.move_to(7, 2)
                self.volume = self.volume - 0.1
                self.lcd.putstr(str(round(self.volume, 2)))
            else:
                self.lcd.move_to(10, 3)
                self.drip_rate = self.drip_rate - 0.1
                self.lcd.putstr(str(round(self.drip_rate, 2)))
        elif self.pcf.pin(self.button_sel)==0:
            self.screen_blank()
            self.flag_irq = 1
            
    def screen_setup(self):
        self.lcd.move_to(15, 0)
        self.lcd.putstr(("id"+str(self.id)))
        self.lcd.move_to(0, 0)
        self.lcd.putstr("Specs:")
        self.lcd.move_to(0, 2)
        self.lcd.putstr(("Volume "+str(self.volume)))
        self.lcd.move_to(19, 2)
        self.lcd.putstr("L")
        self.lcd.move_to(0, 3)
        self.lcd.putstr(("Drop rate "+str(self.drip_rate)))
        self.lcd.move_to(16, 3)
        self.lcd.putstr("dp/m")
        self.lcd.move_to(0, 2)
        self.lcd.show_cursor()
        
    def screen_confirm(self):
        self.lcd.hide_cursor()
        self.lcd.move_to(0, 0)
        self.lcd.putstr(("Consumed "+str(self.consumed)+" %"))
        self.lcd.move_to(0, 1)
        self.lcd.putstr(("Time left "+str(self.time_left)))
        self.lcd.move_to(0, 2)
        self.lcd.putstr(("Volume "+str(self.volume)))
        self.lcd.move_to(19, 2)
        self.lcd.putstr("L")
        self.lcd.move_to(0, 3)
        self.lcd.putstr(("Drop rate "+str(self.drip_rate)))
        self.lcd.move_to(16, 3)
        self.lcd.putstr("dp/m")
        
    
        
        

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)
addr = i2c.scan()
int_pcf = Pin(23, Pin.IN)
test = hmi(addr[1], addr[0], int_pcf, 100)
test.screen_setup()
test.int.irq(trigger = Pin.IRQ_FALLING, handler = test.isr_setup)
while True:
    if test.flag_irq:
        test.flag_irq = 0
        test.screen_confirm()
        break
