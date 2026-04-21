from machine import Pin
import time
import utime

# Front
trigger1 = Pin(1, Pin.OUT)
echo1 = Pin(0, Pin.IN)

# Left
trigger2 = Pin(16, Pin.OUT)
echo2 = Pin(17, Pin.IN)

# Right

trigger3 = Pin(15, Pin.OUT)
echo3 = Pin(14, Pin.IN)

# Back

trigger4 = Pin(27, Pin.OUT)
echo4 = Pin(26, Pin.IN)


# Front
def distanceSensor_Friday():
    trigger1.low()
    time.sleep(0.2)
    trigger1.high()
    time.sleep(0.5)
    trigger1.low()
 
    while echo1.value() == 0:
        off1 = utime.ticks_us()
        # print("off2 is:", off2)
        
    while echo1.value() == 1:
        on1 = utime.ticks_us()
        # print("on2 is:", on2)
 
    timepassed1 = on1 - off1
    distance1 = (timepassed1 * 0.0343) / 2
    print("The distance2 is:",distance1,"cm")
    return distance1


# Left
def distanceSensor_Left():
    trigger2.low()
    time.sleep(0.2)
    trigger2.high()
    time.sleep(0.5)
    trigger2.low()
 
    while echo2.value() == 0:
        off2 = utime.ticks_us()
        # print("off2 is:", off2)
        
    while echo2.value() == 1:
        on2 = utime.ticks_us()
        # print("on2 is:", on2)
 
    timepassed2 = on2 - off2
    distance2 = (timepassed2 * 0.0343) / 2
    print("The distance2 is:",distance2,"cm")
    return distance2


# Right
def distanceSensor_Right():
    trigger3.low()
    time.sleep(0.2)
    trigger3.high()
    time.sleep(0.5)
    trigger3.low()
 
    while echo3.value() == 0:
        off3 = utime.ticks_us()
        # print("off3 is:", off3)
        
    while echo3.value() == 1:
        on3 = utime.ticks_us()
        # print("on3 is:", on3)
 
    timepassed3 = on3 - off3
    distance3 = (timepassed3 * 0.0343) / 2
    print("The distance3 is:",distance3,"cm")
    return distance3


# Back
def distanceSensor_Back():
    trigger4.low()
    time.sleep(0.2)
    trigger4.high()
    time.sleep(0.5)
    trigger4.low()
 
    while echo4.value() == 0:
        off4 = utime.ticks_us()
        # print("off4 is:", off4)
        
    while echo4.value() == 1:
        on4 = utime.ticks_us()
        # print("on4 is:", on4)
 
    timepassed4 = on4 - off4
    distance4 = (timepassed4 * 0.0343) / 2
    print("The distance4 is:",distance4,"cm")
    return distance4


distanceSensor_Front()
distanceSensor_Left()
distanceSensor_Right()
distanceSensor_Back()