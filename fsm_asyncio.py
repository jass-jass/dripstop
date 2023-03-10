from machine import Pin 
from time import sleep
import uasyncio


led_23 = Pin(23, Pin.OUT)
led_22 = Pin(22, Pin.OUT)
led_21 = Pin(21, Pin.OUT)
led_19 = Pin(19, Pin.OUT)
led_18 = Pin(18, Pin.OUT)
led_5 = Pin(5, Pin.OUT)


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
    led_22.on()
    led_19.on()
    await uasyncio.sleep(1)
    led_19.off()
    # y
    led_23.on()
    led_21.on()
    led_18.on()
    led_5.on()
    await uasyncio.sleep(1)
    led_23.off()
    led_19.off()
    led_18.off()
    led_5.off()
    # e
    await uasyncio.sleep(1)
    led_21.off()
    led_22.off()
