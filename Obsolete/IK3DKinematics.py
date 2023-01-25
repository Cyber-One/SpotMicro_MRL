#################################################################
#                                                               #
# Program Code for Spot Micro MRL                               #
# Of the Cyber_One YouTube Channel                              #
# https://www.youtube.com/cyber_one                             #
#                                                               #
# This is version 0.1                                           #
# Divided up into sub programs                                  #
# Coded for the Nixie Version of MyRobotLab.                    #
#                                                               #
# Running on MyRobotLab (MRL) http://myrobotlab.org/            #
# Spot Micro MRL is a set of Python scripts that run inside     #
# the MRL system                                                #
#                                                               #
# LegPosition.py                                                #
# This file calculates the requires servo angles to move a foot #
# to a given position.                                          #
#                                                               #
#################################################################
import math
from org.myrobotlab.kinematics import DHRobotArm
from org.myrobotlab.kinematics import DHLink
from org.myrobotlab.kinematics import DHLinkType

print ("Starting the leg IK3D service")

#################################################################
#                                                               #
# There are a number of ways of calculating the current foot    #
# position, one of the more popular ways is to use the          #
# Kinematic model.  Converseley, planning how to set the joints #
# to place the foot in a set position is known as Inverse       #
# Kinematics or IK.                                             #
#                                                               #
# When calculating out the position of the foot, we know the    #
# following bits of the equation:                               #
# LWF: length of the leg between the Wrist joint and the foot.  #
# LTW: length between the Arm joint and the Wrist joint.        #
# LST: length between the shoulder joint and the Arm joint.     #
# LYS: Length between the center Y plane and the shoulder joint #
# LXS: Length between the center X plane and the shoulder joint #
# We also know the position of each of the servos, but each     #
# servo also has an allowable range. Based off this information #
# we can calculate the current position of the foot relative to #
# the center of the robot.  But just for clarity, lets list the #
# servo ranges.                                                 #
# Wrist: 0 - 135 degrees. 0 degrees is straight.                #
# Arm: 0 - 180 degrees. 90 is straight down.                    #
# Shoulder: 45 - 125 degrees. 90 is with the leg straigt down.  #
# Just for clarity, I will define the Axis we will use here:    #
# X: is from side to side of the robot. Left is negative.       #
# Y: is from the back to Front of the robot. Back is negative.  #
# Z: is from top to bottom of the robot. Down is negative.      #
#                                                               #
#################################################################
# Create a robot arm
myRobotArm = DHRobotArm()

# Lets create a 3 link robot arm
# Create the first link in the arm specified by 100,100,0,90
# additionally specify a name for the link which can be used elsewhere. 
d0 = 10
r0 = 39
theta0 = 66.8
alpha0 = 90
link0 = DHLink("base", d0, r0, theta0, alpha0)

# Create the second link (same as the first link.)
d1 = 91
r1 = -6
theta1 = 90
alpha1 = 90
link1 = DHLink("link1", d1, r1, theta1, alpha1)

# Create the third link (same as the first link.)
d2 = 0
r2 = 105
theta2 = 9
alpha2 = 0
link2 = DHLink("link2", d2, r2, theta2, alpha2)

# Create the third link (same as the first link.)
d3 = 0
r3 = 125
theta3 = 0
alpha3 = 0
link3 = DHLink("link3", d3, r3, theta3, alpha3)

# Add the links to the robot arm
myRobotArm.addLink(link1)
myRobotArm.addLink(link2)
myRobotArm.addLink(link3)


# create the  IK3D service.
ik3d= Runtime.start("ik3d", "InverseKinematics3D")

# assign our custom DH robot arm to the IK service.
ik3d.setCurrentArm("FrontLeftLeg", myRobotArm)

# create the method that will take the calculated joint angles
# and apply them to the required servos.
def ik3dProcessor(angleData):
    print (angleData.name, " - ", angleData.angle)

python.subscribe('ik3d', 'publishJointAngle', 'python', 'ik3dProcessor')
