import machine, pcf8574
from machine import Pin, I2C
from i2c_lcd import I2cLcd
import time


class HMI(I2cLcd):
    
    totalRows = 4
    totalColumns = 20
    params = "calibrate", "volume", "rate"
    parameter = params[0]
    state = "setup"
    sr = "start"
    flag_irq = 0
    cursor = [0,0]    # cursor[0] - x
                      # cursor[1] - y

    
    def __init__(self, i2c, addr_lcd, addr_pcf, int_pcf, id_dev):
        self.lcd = I2cLcd(i2c, addr_lcd, self.totalRows, self.totalColumns)
        self.volume = 0.0
        self.drip_rate = 5
        self.id = id_dev
        self.consumed = 0
        self.time_left = -1
        self.lcd.custom_char(1, [ 0x04,0x0E,0x0E,0x1F,0x1F,0x1F,0x0E,0x00])
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
    
    '''
    def poll():
        for i in range(8):
            temp = pcf.pin(i)
            print(temp)
            arr.append(temp)
            if temp:
                ones = ones + 1
        if ones != 7:
            return
        data = arr
    '''
    
    def isr_setup(self, pin):
        if self.pcf.pin(self.button_dwn)==0:
            self.cursor[1] = self.cursor[1] + 1
            if self.cursor[1] > 3:
                self.cursor[1] = 3
            self.lcd.move_to(self.cursor[0], self.cursor[1])
            self.parameter = self.params[(self.cursor[1]-1)]
        if self.pcf.pin(self.button_up)==0:
            self.cursor[1] = self.cursor[1] - 1
            if self.cursor[1] < 1:
                self.cursor[1] = 1
            self.lcd.move_to(self.cursor[0], self.cursor[1])
            self.parameter = self.params[(self.cursor[1]-1)]
        elif self.pcf.pin(self.button_inc)==0:
            if self.parameter == "volume":
                self.lcd.move_to(7, 2)
                self.volume = self.volume + 0.1
                self.lcd.putstr(str(round(self.volume, 2)))
            elif self.parameter == "rate":
                self.lcd.move_to(10, 3)
                self.drip_rate = self.drip_rate + 5
                self.lcd.putstr(str(self.drip_rate))
        elif self.pcf.pin(self.button_dec)==0:
            if self.parameter == "volume":
                self.lcd.move_to(7, 2)
                self.volume = self.volume - 0.1
                if self.volume < 0.0:
                    self.volume = 0.0
                self.lcd.putstr(str(round(self.volume, 2)))
            elif self.parameter == "rate":
                self.lcd.move_to(10, 3)
                self.drip_rate = self.drip_rate - 5
                if self.drip_rate < 5:
                    self.drip_rate = 5
                self.lcd.putstr(str(self.drip_rate))
        elif self.pcf.pin(self.button_sel)==0:
            if self.parameter == "calibrate":
                self.state = self.parameter
            else:
                self.state = "confirm"
            self.flag_irq = 1
    
    def isr_confirm(self, pin):
        if self.pcf.pin(self.button_dec) == 0: # or self.pcf.pin(self.button_up) ==0:
            self.lcd.move_to(1,3)
            #print("yes")
            self.state = "done"
        elif self.pcf.pin(self.button_inc) == 0: #or self.pcf.pin(self.button_dwn) ==0:
            self.lcd.move_to(17,3)
            #print("no")
            self.state = "setup"
        elif self.pcf.pin(self.button_sel)==0:
            self.flag_irq = 1
    
    def isr_continue(self, Pin):
        self.state = "confirm"
        self.flag_irq = 1
    
    def animate_drops(self, x, x_limit, line):
        while x < x_limit:
            self.lcd.move_to(x, line)
            self.lcd.putstr("\x01")
            self.lcd.move_to(x, line)
            t = time.ticks_us()
            while time.ticks_us() - t < 600000:
                pass
            self.lcd.putstr(" ")
            x = x + 1
        self.state = "confirm"
    
    def screen_setup(self):
        self.screen_blank()
        self.lcd.move_to(0, 0)
        self.lcd.putstr("Specs:")
        self.lcd.move_to(0, 1)
        self.lcd.putstr("Calibrate")
        self.lcd.move_to(0, 2)
        self.lcd.putstr(("Volume "+str(self.volume)))
        self.lcd.move_to(19, 2)
        self.lcd.putstr("L")
        self.lcd.move_to(0, 3)
        self.lcd.putstr(("Drop rate "+str(self.drip_rate)))
        self.lcd.move_to(16, 3)
        self.lcd.putstr("dp/m")
        self.lcd.move_to(0, 1)
        self.parameter = self.params[0]
        self.lcd.show_cursor()
   
    def screen_calibrate(self):
        self.screen_blank()
        self.lcd.move_to(4,2)
        self.lcd.putstr("In Progress")
        
    def screen_blank(self):
        self.lcd.hide_cursor()
        self.lcd.clear()
        self.lcd.move_to(15, 0)
        self.lcd.putstr(("ID"+str(self.id)))
        
    def screen_confirm(self):
        self.screen_blank()
        self.lcd.move_to(2,1)
        self.lcd.putstr(("Are you sure you     want to " + self.sr + "?"))
        self.lcd.move_to(1,3)
        self.lcd.putstr("Yes")
        self.lcd.move_to(17,3)
        self.lcd.putstr("No")
        self.lcd.move_to(1,3)
        self.state = "done"
        self.lcd.show_cursor()
        
    def screen_display(self):
        self.screen_blank()
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
