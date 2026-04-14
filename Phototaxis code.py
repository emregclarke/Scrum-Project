import time
import board
import adafruit_bh1750
import RPi.GPIO as GPIO


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
    "R3_knee": 13,
}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(list(motor_pins.values()), GPIO.OUT)


def motor_on(name):
    GPIO.output(motor_pins[name], GPIO.HIGH)

def motor_off(name):
    GPIO.output(motor_pins[name], GPIO.LOW)
    
group_A = ["L1_hip", "R2_hip", "L3_hip"]
group_B = ["R1_hip", "L2_hip", "R3_hip"]

def step():
    for m in group_A:
        motor_on(m)
    for m in group_B:
        motor_off(m)
    time.sleep(0.2)
    
    for m in group_A:
        motor_off(m) 
    for m in group_B:
        motor_on(m)
    time.sleep(0.2)
    
    
def search_step():
    for m in ["L1_hip", "L2_hip", "L3_hip"]:
        motor_on(m)
    for m in ["R1_hip", "R2_hip", "R3_hip"]:
        motor_off(m) 
    time.sleep(0.2)
    
    for m in ["L1_hip", "L2_hip", "L3_hip"]:
        motor_off(m)
    for m in ["R1_hip", "R2_hip", "R3_hip"]:
        motor_on(m)
    time.sleep(0.2)
    
    
def stop_all():
    for pin in motor_pins.values():
        GPIO.output(pin, GPIO.LOW)
    
# Sensor setup
i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)

LIGHT_THRESHOLD = 500  
last_lux = 0


try:
    print("Starting Phototaxis Search...")
    
    while True:
        lux = sensor.lux
        print(f"Lux: {lux:.2f}")
        
        if lux > LIGHT_THRESHOLD:
            step()
            print("Walking towards light")
        
        else:
            if lux >= last_lux:
                search_step()
                print("Searching -- Getting brighter")
            else:
                print("Searching -- Getting darker")
                search_step()
            
        last_lux = lux 
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("Stopping")
    
finally:
    stop_all()
    GPIO.cleanup()
