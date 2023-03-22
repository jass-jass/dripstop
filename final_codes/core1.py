from machine import Pin 
from time import sleep
import uasyncio



### power on state ###
def power_on():

async def run_state_machine():
    state = power_on
    while True:
        state = await state()


loop = uasyncio.get_event_loop()
loop.create_task(run_state_machine())
loop.run_forever()
