# LIGHT SENSOR CODE

# Reading Sensor:
from machine import I2C, Pin 
import time 

# I2C communication 
i2c = I2C(0, scl=Pin(1), sda=Pin(0))

# sensor address 
light_sensor_add = 0x23

# function to read sensor 
def read_light():
    #send data to sensor 
    i2c.writeto(light_sensor_add, b'\x10')
    time.sleep(0.2)
    #reads 2 bytes from sensor 
    data = i2c.readfrom(light_sensor_add, 2)

    #convert bytes to number  
    # light = first byte (high) << shift left (multiplies by 256) | second byte (low)
    light = (data[0] << 8) | data[1]
    return light 

# main loop
while True:
    value = read_light()
    print("Light: ", value)
    time.sleep(1)


# Change Detection 
previous = read_light()
while True:
    current = read_light()

    change = current - previous 

    print("Light:", current, "Change:", change)

    previous = current 
    time.sleep(1)


# ON / OFF Behaviour 
previous = read_light()

while True:
    current = read_light()
    change = current - previous 

    if change > 5: 
        print("ON -> move forward")

    elif change < -5:
        print("OFF -> turn / explore")

    else:
        print("No sugnificant change")

    previous = current 
    time.sleep(1)


# EMA (Exponential Moving Average)
alpha = 0.3
ema = read_light()

while True: 
    value = read_light()

    ema = alpha * value + (1 - alpha) * ema
    
    print("Smoothed light: ", ema)

    time.sleep(1)