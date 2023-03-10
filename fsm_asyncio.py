from machine import Pin 
from time import sleep
import uasyncio

pins = [23, 22, 21, 19, 18, 5]

for i in pins:
    globals()[f"led_{i}"] = Pin(i, Pin.OUT)

async def input_state():
    while True:


async def hi():
    # h
    led_22.on()
    led_19.on()
    led_21.on()
    await uasyncio.sleep(1)
    led_22.off()
    led_21.off()
    # i
    led_23.on()
    await uasyncio.sleep(1)
    led_19.off()
    led_23.off()


async def bye():
    # b
    # y
