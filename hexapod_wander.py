
import time
import random
import busio
import csv
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from servo import Servos
from machine import I2C, Pin


i2c_board = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_board)
pca.frequency = 50

i2c = I2C(0, sda=Pin(0), scl=Pin(1))
servos = Servos(i2c)

# Servo pulse limits
MIN_US = 500
MAX_US = 2500
FREQ   = 50

# Servo channel map
motor_pins = {
    "L1_hip":  2,  "L1_knee":  3,
    "L2_hip":  4,  "L2_knee":  5,
    "L3_hip":  6,  "L3_knee":  7,
    "R1_hip":  8,  "R1_knee":  9,
    "R2_hip": 10,  "R2_knee": 11,
    "R3_hip": 12,  "R3_knee": 13,
}

csv_filename = "pca9685_log.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Channel", "PWM_Value"])

def set_pwm_log(channel, value):
    """Set a PWM channel and log it to CSV."""
    try:
        pca.channels[channel].duty_cycle = value
        with open(csv_filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([time.time(), channel, value])
    except Exception as e:
        print(f"Error setting PWM on channel {channel}: {e}")

# ------------------------------------------------------------
#  UTILITY
# ------------------------------------------------------------
def timer(duration):
    """Blocking timer in seconds."""
    start = time.time()
    while (time.time() - start) < duration:
        time.sleep(0.05)

def set_leg(name, degrees):
    """Move a named servo to a given angle."""
    servos.position(motor_pins[name], degrees=degrees)


def hexapod_start():
    for i in range(14):
        servos.position(i, degrees=90)
    print("Hexapod ready - all legs centred.")


STEP_DELAY  = 0.15   # seconds between sub-steps
LIFT_ANGLE  = 60     # knee angle for lifting a leg
STAND_ANGLE = 90     # neutral knee angle
STEP_FWD    = 70     # hip forward sweep
STEP_BWD    = 110    # hip back sweep
TURN_INNER  = 60     # hip angle for inner legs on a turn
TURN_OUTER  = 120    # hip angle for outer legs on a turn

GROUP_A = ["L1", "R2", "L3"]
GROUP_B = ["R1", "L2", "R3"]

def _tripod_step(group_a_hips, group_b_hips, hip_angle):
    """
    One tripod stride cycle.
    Group A lifts and swings to hip_angle while Group B pushes back.
    Then roles reverse.
    """
    # Phase 1: Group A swings forward, Group B pushes
    for ch in group_a_hips:
        set_leg(ch + "_knee", LIFT_ANGLE)
    for ch in group_a_hips:
        set_leg(ch + "_hip", hip_angle)
    for ch in group_b_hips:
        set_leg(ch + "_hip", STEP_BWD)
    time.sleep(STEP_DELAY)
    for ch in group_a_hips:
        set_leg(ch + "_knee", STAND_ANGLE)
    time.sleep(STEP_DELAY)

    # Phase 2: Group B swings forward, Group A pushes
    for ch in group_b_hips:
        set_leg(ch + "_knee", LIFT_ANGLE)
    for ch in group_b_hips:
        set_leg(ch + "_hip", hip_angle)
    for ch in group_a_hips:
        set_leg(ch + "_hip", STEP_BWD)
    time.sleep(STEP_DELAY)
    for ch in group_b_hips:
        set_leg(ch + "_knee", STAND_ANGLE)
    time.sleep(STEP_DELAY)

def Forward(steps=1):
    print(">> Forward")
    for _ in range(steps):
        _tripod_step(GROUP_A, GROUP_B, STEP_FWD)

def Backward(steps=1):
    print(">> Backward")
    for _ in range(steps):
        _tripod_step(GROUP_A, GROUP_B, STEP_BWD)

def Left(steps=1):
    """Turn left: right legs push forward, left legs push back."""
    print(">> Left")
    for _ in range(steps):
        for ch in ["R1", "R2", "R3"]:
            set_leg(ch + "_knee", LIFT_ANGLE)
            set_leg(ch + "_hip",  TURN_OUTER)
        for ch in ["L1", "L2", "L3"]:
            set_leg(ch + "_hip",  TURN_INNER)
        time.sleep(STEP_DELAY)
        for ch in ["R1", "R2", "R3"]:
            set_leg(ch + "_knee", STAND_ANGLE)
        time.sleep(STEP_DELAY)

def Right(steps=1):
    """Turn right: left legs push forward, right legs push back."""
    print(">> Right")
    for _ in range(steps):
        for ch in ["L1", "L2", "L3"]:
            set_leg(ch + "_knee", LIFT_ANGLE)
            set_leg(ch + "_hip",  TURN_OUTER)
        for ch in ["R1", "R2", "R3"]:
            set_leg(ch + "_hip",  TURN_INNER)
        time.sleep(STEP_DELAY)
        for ch in ["L1", "L2", "L3"]:
            set_leg(ch + "_knee", STAND_ANGLE)
        time.sleep(STEP_DELAY)

def Stop():
    """Hold position - all knees down, hips neutral."""
    print(">> Stop")
    for i in range(14):
        servos.position(i, degrees=90)

def open_wing():
    """Predator response - spread all legs wide."""
    print("!! Predator detected - opening wings!")
    for ch in ["L1", "L2", "L3"]:
        set_leg(ch + "_hip", 60)
    for ch in ["R1", "R2", "R3"]:
        set_leg(ch + "_hip", 120)
    for i in range(14):
        servos.position(i, degrees=45)
    timer(1.0)


ultrasonic_data = [0, 0, 0, 0]   # [Front, Left, Right, Back]

def distanceSensor_Front():
    return 100   # TODO: replace with actual sensor read

def distanceSensor_Left():
    return 100   # TODO: replace with actual sensor read

def distanceSensor_Right():
    return 100   # TODO: replace with actual sensor read

def distanceSensor_Back():
    return 100   # TODO: replace with actual sensor read

def ultrasonic():
    """Read all four ultrasonic sensors into ultrasonic_data."""
    ultrasonic_data[0] = distanceSensor_Front()
    ultrasonic_data[1] = distanceSensor_Left()
    ultrasonic_data[2] = distanceSensor_Right()
    ultrasonic_data[3] = distanceSensor_Back()

THRESH_FRONT = 25
THRESH_SIDE  = 30
THRESH_BACK  = 10

def check_avoidance():
    """
    Checks sensors and reacts to nearby obstacles.
    Returns True if an avoidance action was taken (skips wander for this cycle).
    Priority: Front > Left > Right > Back
    """
    front = ultrasonic_data[0]
    left  = ultrasonic_data[1]
    right = ultrasonic_data[2]
    back  = ultrasonic_data[3]

    if front <= THRESH_FRONT:
        print(f"[AVOID] Object front ({front} cm) - turning left")
        Left(steps=2)
        return True

    if left <= THRESH_SIDE:
        print(f"[AVOID] Object left ({left} cm) - turning right")
        Right(steps=2)
        return True

    if right <= THRESH_SIDE:
        print(f"[AVOID] Object right ({right} cm) - turning left")
        Left(steps=2)
        return True

    if back <= THRESH_BACK:
        print(f"[AVOID] Object back ({back} cm) - moving forward")
        Forward(steps=2)
        return True

    return False


PREDATOR_CHANGE_THRESH = 25

# Will be initialised after first sensor read
current_value_Front = 0
current_value_Left  = 0
current_value_Right = 0
current_value_Back  = 0

def init_predator_values():
    """Seed the previous-value tracking after first sensor read."""
    global current_value_Front, current_value_Left
    global current_value_Right, current_value_Back
    ultrasonic()
    current_value_Front = ultrasonic_data[0]
    current_value_Left  = ultrasonic_data[1]
    current_value_Right = ultrasonic_data[2]
    current_value_Back  = ultrasonic_data[3]

def check_predator():
    """
    Detects rapid approach (large negative delta = object closing fast).
    Returns True if predator response was triggered.
    """
    global current_value_Front, current_value_Left
    global current_value_Right, current_value_Back

    previous_value_Front = current_value_Front
    current_value_Front  = ultrasonic_data[0]
    change_Front = previous_value_Front - current_value_Front  # positive = closing

    previous_value_Left = current_value_Left
    current_value_Left  = ultrasonic_data[1]
    change_Left = previous_value_Left - current_value_Left

    previous_value_Right = current_value_Right
    current_value_Right  = ultrasonic_data[2]
    change_Right = previous_value_Right - current_value_Right

    previous_value_Back = current_value_Back
    current_value_Back  = ultrasonic_data[3]
    change_Back = previous_value_Back - current_value_Back

    if (change_Front >= PREDATOR_CHANGE_THRESH or
        change_Left  >= PREDATOR_CHANGE_THRESH or
        change_Right >= PREDATOR_CHANGE_THRESH or
        change_Back  >= PREDATOR_CHANGE_THRESH):
        open_wing()
        return True

    return False


WANDER_ACTIONS   = ["forward", "forward", "forward", "left", "right"]
WANDER_STEPS_MIN = 2
WANDER_STEPS_MAX = 6

def random_wander():
    """Pick a random movement and execute it."""
    action = random.choice(WANDER_ACTIONS)
    steps  = random.randint(WANDER_STEPS_MIN, WANDER_STEPS_MAX)
    print(f"[WANDER] {action} x{steps}")

    if action == "forward":
        Forward(steps=steps)
    elif action == "left":
        Left(steps=steps)
    elif action == "right":
        Right(steps=steps)

hexapod_start()
timer(1.0)
init_predator_values()

print("=" * 40)
print("  Wander loop running - press Stop to exit")
print("=" * 40)

while True:

    # 1. Read all sensors first
    ultrasonic()

    # 2. Predator check - highest priority
    if check_predator():
        timer(0.5)
        continue

    # 3. Object avoidance - overrides wander
    if check_avoidance():
        timer(0.3)
        continue

    # 4. Normal random wander
    random_wander()
    timer(0.2)
