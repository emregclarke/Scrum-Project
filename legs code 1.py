import Wire.h
import Adafruit_PWMServoDricer.h
import busio
import csv
from board import SCL, SDA
from machine import I2C, Pin
import time
from adafruit_pca9685 import PCA9685
from servo import Servos

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c)
pca.freq(50)

### to record pca9685 values ###

csv_filename = "pca9685_log.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp","Channel", "PWM_Value"])
    
def set_pwm_log(channel, value):
    try:
        pca.channels[channel1].duty_cycle = value
        with open(csv_filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().isoformat(), channel, value])
        except Exception as e:
            printf(f"Error setting PWM on channel {channel}: {e}")
            

def Timer(duration):
    start_time = time.time()
    run = False
    while run == False:
        time.sleep(.1)
        time_past = time.time() - start_time
        if time_past >= duration:
            run = True

i2c = I2C(0, sda=Pin(0), scl=Pin(1))

servoPins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
servos = Servos(i2c)#

MIN_US = 500
MAX_US = 2500
FREQ = 50

motor_pins = {
    "L1_hip": 2,
    "L1_knee": 3,
    "L2_hip": 4,
    "L2_knee": 5,
    "L3_hip": 6,
    "L3_knee": 7,
    "R1_hip": 8,
    "R1_knee": 9,
    "R2_hip": 10,
    "R2_knee": 11,
    "R3_hip": 12,
    "R3_knee": 13}

GPIO.setup(list(motor_pins.values()), GPIO.OUT)
def hexapod_start():
    for i in range(12):
        servos.position(i, degrees=90)
    print("All legs centered.")
    
hexapod_start()

while True:
    servos.position(0, degrees=45)
    time.sleep(0.5)
    servos.position(0, degrees=90)
    time.sleep(0.5)