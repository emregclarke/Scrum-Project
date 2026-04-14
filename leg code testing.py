from machine import Pin, PWM
from time import sleep

# Servo connected to GP15
servo_pin = PWM(Pin(15))
servo_pin.freq(50)  # Standard servo frequency: 50Hz

def set_angle(angle):
    """
    Set servo angle between 0 and 180 degrees.
    Adjust duty cycle range if your servo behaves differently.
    """
    if angle < 0 or angle > 180:
        raise ValueError("Angle must be between 0 and 180")

    # Convert angle to duty cycle (for 50Hz, duty_u16 range ~1638 to ~8192)
    min_duty = 1638   # ~0.5ms pulse
    max_duty = 8192   # ~2.5ms pulse
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo_pin.duty_u16(duty)

# Example: Sweep servo back and forth
try:
    while True:
        for angle in range(0, 181, 5):
            set_angle(angle)
            sleep(0.05)
        for angle in range(180, -1, -5):
            set_angle(angle)
            sleep(0.05)
except KeyboardInterrupt:
    servo_pin.deinit()  # Turn off PWM safely
