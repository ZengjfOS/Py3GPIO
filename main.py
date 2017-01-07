#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gpio.GPIO import GPIO

def main():

    stopPinNumber = GPIO.getIMXPinNumber(0, 12)
    GPIO.initGPIOOut(stopPinNumber, 0)
    GPIO.setValue(stopPinNumber, 1)
    GPIO.freeGPIO(stopPinNumber)

if __name__ == '__main__':
    main()