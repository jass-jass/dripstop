import machine, pcf8574
from machine import Pin, I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep


class hmi(I2cLcd):
    
    totalRows = 4
    totalColumns = 20
    next_screen = None
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
            self.next_screen = "rate"
        elif self.pcf.pin(self.button_up)==0:
            self.lcd.move_to(0, 2)
            self.next_screen = "volume"
        elif self.pcf.pin(self.button_sel)==0:
            self.screen_blank()
            self.flag_irq = 1
            
    def isr_rate(self, pin):
        count = 0
        while(self.pcf.pin(self.button_sel)):
            self.lcd.move_to(13, 3)
            if self.pcf.pin(self.button_dwn) == 0:
                count = count - 0.1
            elif self.pcf.pin(self.button_up) == 0:
                count = count + 0.1
            self.lcd.putstr(str(self.drip_rate + count))
        self.drip_rate = self.drip_rate + count
        self.screen_blank()
        self.flag_irq = 1
        
    def isr_volume(self, pin):
        count = 0
        while(self.pcf.pin(self.button_sel)):
            self.lcd.move_to(13, 3)
            if self.pcf.pin(self.button_dwn) == 0:
                count = count - 0.1
            elif self.pcf.pin(self.button_up) == 0:
                count = count + 0.1
            self.lcd.putstr(str(self.volume + count))
        self.volume = self.volume + count
        self.screen_blank()
        self.flag_irq = 1
    
    def screen_setup(self):
        self.lcd.move_to(15, 0)
        self.lcd.putstr(("id"+str(self.id)))
        self.lcd.move_to(0, 0)
        self.lcd.putstr("Specs:")
        self.lcd.move_to(0, 2)
        self.lcd.putstr("Volume")
        self.lcd.move_to(0, 3)
        self.lcd.putstr("Infusion Rate")
        self.lcd.move_to(0, 2)
        self.lcd.show_cursor()
    
    def screen_rate(self):
        self.lcd.move_to(0, 0)
        self.lcd.putstr("Infusion")
        self.lcd.move_to(0, 2)
        self.lcd.putstr(("Current rate: "+str(self.drip_rate)))
        self.lcd.move_to(0, 3)
        self.lcd.putstr(("Desired rate: "+str(self.drip_rate)))
        
    def screen_volume(self):
        self.lcd.move_to(0, 0)
        self.lcd.putstr("Volume")
        self.lcd.move_to(0, 2)
        self.lcd.putstr(("Current vol: "+str(self.volume)))
        self.lcd.move_to(0, 3)
        self.lcd.putstr(("Desired vol: "+str(self.volume)))
        
    
        
        

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)
addr = i2c.scan()
int_pcf = Pin(23, Pin.IN)
test = hmi(addr[1], addr[0], int_pcf, 100)
test.screen_setup()
test.int.irq(trigger = Pin.IRQ_FALLING, handler = test.isr_setup)
while True:
    if test.flag_irq:
        if test.next_screen == "volume":
            test.screen_volume()
            test.int.irq(trigger = Pin.IRQ_FALLING, handler = test.isr_volume)
        else:
            test.screen_rate()
            test.int.irq(trigger = Pin.IRQ_FALLING, handler = test.isr_rate)
        test.flag_irq = 0
        break
while True:
    if test.flag_irq:
        test.screen_setup()
        break
