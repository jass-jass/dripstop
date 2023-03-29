### import ###
from machine import Pin, PWM, I2C
from micropython import const
from time import sleep
import uasyncio
from hx711 import HX711



#######################################################################
                         ''' Initializations '''
#######################################################################
### Outputs ###
status_led = Pin(23, Pin.OUT)
servo = PWM(Pin(26), freq(50))

### Inputs ###
drip_sensor = Pin(14, Pin.IN)   # interrupt for rising and falling edges
pcf_int = Pin(25, Pin.IN)   # interrupt
load_cell = HX711(d_out = 4, pd_sck = 18, channel = 1)  # channel A gain 128

### Protocols ###
i2c_device = I2C(0, scl = Pin(22), sda = Pin(21))

### Variables ###
tube_change = 0
drip_rate = 0
hmi_status = 0x00

### Flags ###
load_cell_flag = 0
count_flag = 0

### Constants ###
# Status LED
status_power_on = const()
status_adjust = const()
status_calibrate = const()

# Servo motor
servo_home = const()
servo_close = const()
servo_step = 0


#######################################################################



#######################################################################
                             '''ISRs'''
#######################################################################
def HMI_ISR():
  global load_cell_flag
  global input_array
  if load_cell_flag:
    # disable interrupt
    # return to idle
  elif input_array xor :   # data from pcf


#######################################################################



#######################################################################
                            '''STATES'''
#######################################################################
### power on state ###
async def power_on():
    led_status.value(status_power_on)
    # lcd display configure
    if tube_change:
        servo.duty(servo_home)
    # HMI with LCD updation
    await # wait for start button to be pressed
    
    
### start state ###
async def start():
    servo.duty(servo_close)
    led_status.value(status_calibrate)
    drip_rate = # calculate drip rate
    # check for current rate and calculated 
    # switch to idle or adjust acc
    
    
### compare and adjust state ###
async def comp_n_adjust():
    servo_step = 0
    while True:
        # ticks with interrupt
        if drip_rate = freq_ticks:
            count_flag = count_flag + 1
        else:
            servo_step = servo_step + 2     # angle increased by 2 degrees
            servo.duty(servo_close + servo_step)
        if count_flag == 2:
            count_flag = 0
            return idle
    

### Idle state ###
async def idle():
    
    
#######################################################################



async def run_state_machine():
    state = power_on
    while True:
        state = await state()

       
### thread safe flag allows interrupts and threads to run along with 
### tasks of the fsm
tsf = uasyncio.ThreadSafeFlag()

def set_tsf(_):
    tsf.set()

async def schedule_interrupt():
    while True:
        await tsf.wait()
        HMI_ISR()

pdf_int.irq(trigger = Pin.IRQ_RISING, handler = set_tsf)

loop = uasyncio.get_event_loop()
loop.create_task(run_state_machine())    # FSM for main tasks
loop.create_task(schedule_interrupt())   # FSM for interrupts
loop.run_forever()
