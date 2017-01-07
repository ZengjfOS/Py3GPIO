# py3gpio

```
    stopPinNumber = GPIO.getIMXPinNumber(0, 12)
    GPIO.initGPIOOut(stopPinNumber, 0)
    GPIO.setValue(stopPinNumber, 1)
    GPIO.freeGPIO(stopPinNumber)
```
