from gopigo import *
from time import *
import math
import numpy as np
import matplotlib.pyplot as plt

threesixty = 39.0
WHEEL_RAD = 3.25

BUG_POS = [0, 0, 90] # x, y, theta
MAP = [BUG_POS]
Q_GOAL = [0, 100]

def left_deg(deg):
    if deg < 0:
	right_deg(-deg)
        return
    BUG_POS[2] += deg
    MAP.append(list(BUG_POS))
    enc_tgt(1, 1, int(deg * threesixty / 360.0))
    while read_enc_status():
        left_rot()
    stop()
    
def right_deg(deg):
    if deg < 0:
	left_deg(-deg)
        return
    BUG_POS[2] -= deg
    MAP.append(list(BUG_POS))
    enc_tgt(1, 1, int(deg * threesixty / 360.0))
    while read_enc_status():
        right_rot()
    stop()
    
def fwd_cm(dist):
    BUG_POS[0] += dist * math.cos(math.radians(BUG_POS[2]))
    BUG_POS[1] += dist * math.sin(math.radians(BUG_POS[2]))
    MAP.append(list(BUG_POS))
    enc_tgt(1, 1, cm2pulse(dist))
    while read_enc_status():
        fwd()
    stop()

def cm2pulse(dist):
    return int(dist / (2 * math.pi * WHEEL_RAD) * 18)   


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
def isatpoint(p1, p2):
    if dist(p1, p2) < 2.9:
        return True
    return False

def draw_map():
    print(len(MAP))
    x, y, u, v = [], [], [], []
    for i in MAP:
        x.append(i[0])
        y.append(i[1])
        u.append(math.cos(math.radians(i[2])))
        v.append(math.sin(math.radians(i[2])))
    plt.figure()
    ax = plt.gca()
    ax.quiver(x, y, u, v)
    plt.draw()
    plt.show()
# test accuracy  of fwd_cm

def bug2():
    while True:
        while (us_dist(15) > 10):
            fwd_cm(5)
            sleep(0.2)
            if isatpoint(BUG_POS, Q_GOAL):
                return True
        left_deg(90)
        hit_point = list(BUG_POS)
        
        while True:
            servo(0)
            sleep(0.2)
            right = us_dist(15)
            servo(90)
            sleep(0.2)
            forward = us_dist(15)
            # right sensor and fwd sensor tests
            if right < 10:
                left_deg(30)
                sleep(0.25)
                fwd_cm(3)
                sleep(0.25)
            if not right < 25:
                servo(45)
                sleep(0.2)
                if us_dist(15) < 25:
                    left_deg(30)
                    sleep(0.25)
                    fwd_cm(3)
                    sleep(0.25)
                else:
                    fwd_cm(3)
                    sleep(0.25)
                    right_deg(30)
                    sleep(0.25)
            elif forward < 25:
                left_deg(30)
                sleep(0.25)
                fwd_cm(3)
                sleep(0.25)
            else:
                fwd_cm(5)
                sleep(0.25)
            # do move following bound
	    print BUG_POS            
        
            if isatpoint(BUG_POS, Q_GOAL):
                return True
            if isatpoint(BUG_POS, hit_point):
                return False
            if abs(BUG_POS[0]) < 2 and dist(BUG_POS, Q_GOAL) < dist(hit_point, Q_GOAL):
                print("reached mline")
		left_deg(90 - BUG_POS[2])
		sleep(0.3)
		servo(90)
		sleep(0.25)
		if us_dist(15) < 15:
		    continue

		break

                
if __name__ == "__main__":
    enable_servo()
    servo(90)
    if bug2():
        print("Goal found!")
    else:
        print("Impossible :(")
    draw_map()
