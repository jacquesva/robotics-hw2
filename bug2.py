from gopigo import *
from time import *
import math

threesixty = 39.0
WHEEL_RAD = 3.25

def left_deg(deg):
    enc_tgt(1, 1, int(deg * threesixty / 360.0))
    while read_enc_status():
        left_rot()
    stop()
    
def right_deg(deg):
    enc_tgt(1, 1, int(deg * threesixty / 360.0))
    while read_enc_status():
        right_rot()
    stop()
    
def fwd_cm(dist):
    enc_tgt(1, 1, cm2pulse(dist))
    while read_enc_status():
        fwd()
    stop()

def cm2pulse(dist):
    return int(dist / (2 * math.pi * WHEEL_RAD) * 18)

enable_servo()
servo(90)

bug_pos = [0, 0]
q_goal = [0, 300]

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
def isatpoint(p1, p2):
    if dist(p1, p2) < 16:
        return True
    return False

# test accuracy  of fwd_cm

def bug2():
    while True:
        initial_dist = us_dist(15)
        dist_traveled = 0
        while (us_dist(15) > 17):
            fwd_cm(5)
            sleep(0.2)
            if isatpoint([bug_pos[0], bug_pos[1] + initial_dist - us_dist(15)], q_goal):
                return True
        bug_pos[1] += initial_dist - us_dist(15)
        left_deg(90)
        hit_point = bug_pos
        
        while True:
            
            # right sensor and fwd sensor tests
            if !right:
                right_deg(some amount)
            elif fwd:
                left_deg(some amount)
            else:
                fwd(5)
            # do move following bound
            
        
            if isatpoint(bug_pos, q_goal):
                return True
            if isatpoint(bug_pos, hit_point):
                return False
            if abs(bug_pos[0]) < 2 and dist(bug_pos, q_goal) < dist(hit_point, q_goal):
                # check if obstacle in way of driving to goal goal
                # if not, break. If so, continue
                # reposition to face goal

    break

if __name__ == "__main__":
    if bug2():
        print("Goal found!")
    else:
        print("Impossible :(")