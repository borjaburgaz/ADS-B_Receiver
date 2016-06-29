'''
Created on 15/2/2015

@author: borjaburgaz
'''
import math

ew_vel = 272.0
ns_vel = 75.0

ew_dir = 0      #East
ns_dir = 1      #South


abs_vel = math.sqrt(ew_vel**2.0+ns_vel**2.0)
print(abs_vel)

def heading(ew_vel,ns_vel,ew_dir,ns_dir):
    if ew_dir == 0 and ns_dir == 0:
        return 90.0 - (math.atan(ns_vel/ew_vel)*(180/math.pi))
    elif ew_dir == 0 and ns_dir == 1:
        return (math.atan(ns_vel/ew_vel)*(180.0/math.pi)) + 90.0
    elif ew_dir == 1 and ns_dir == 1:
        return 270.0 - (math.atan(ns_vel/ew_vel)*(180/math.pi))
    else:
        return (math.atan(ns_vel/ew_vel)*(180/math.pi)) + 270.0

print(heading(ew_vel,ns_vel,ew_dir,ns_dir))



