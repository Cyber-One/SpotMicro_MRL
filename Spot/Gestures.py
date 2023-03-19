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
# Gestures.py                                                   #
# This file is a group of commands that perform actions         #
#                                                               #
#################################################################
print ("Starting the various Gestures Services")

#################################################################
# The following variable will help with the movement controls.  #
# 0 = Rest Position.
# 1 = Standing Position.
# 2 = Sitting Position.
# 3 = Stand Tall.
# 4 = Crouch.
#################################################################
gestureStatus = 0

#################################################################
# This command returns all the servos to the starting rest      #
# position and makes sure all the servos are updated.           #
# Handy when calibrating.                                       #
#################################################################
def rest(Steps = 10, Time = 0.03):
    global gestureStatus
    print ("Moving to Rest postition")
    legs.autoBalance = False
    legs.autoLevel = False
    legs.syncServos()
    legs.updateServos()
    # If we move to the rest position without going to the 
    # crouch position first, the robot tends to fall over.
    if gestureStatus != 4:
        crouch(Steps, Time)
    Shoulder = (legs.FL.shoulder.pos + legs.FR.shoulder.pos + legs.BL.shoulder.pos + legs.BR.shoulder.pos)/4
    Arm = (legs.FL.arm.pos + legs.FR.arm.pos + legs.BL.arm.pos + legs.BR.arm.pos)/4
    Wrist = (legs.FL.wrist.pos + legs.FR.wrist.pos + legs.BL.wrist.pos + legs.BR.wrist.pos)/4
    ShoulderRest = (legs.FL.shoulder.rest + legs.FR.shoulder.rest + legs.BL.shoulder.rest + legs.BR.shoulder.rest)/4
    ArmRest = (legs.FL.arm.rest + legs.FR.arm.rest + legs.BL.arm.rest + legs.BR.arm.rest)/4
    WristRest = (legs.FL.wrist.rest + legs.FR.wrist.rest + legs.BL.wrist.rest + legs.BR.wrist.rest)/4
    legs.moveServos(ShoulderRest - Shoulder, ArmRest - Arm, WristRest - Wrist, Steps, Time)
    legs.rest()
    legs.syncServos()
    gestureStatus = 0
    print(legs)

#################################################################
# Thye crouch() command send the robot into a position that is  #
# safe to move into other positions first.  Examples is from    #
# rest to standing will result in the robot falling over        #
# backwards unless the robot moves via the crouch position      #
# first.  The same applies to moving from Sit or to Rest.
#################################################################
def crouch(Steps = 20, Time = 0.03):
    global gestureStatus
    print ("Moving to Crouch postition")
    legs.autoBalance = False
    legs.autoLevel = False
    # we work out the average rest position for both the 
    # shoulder and the wrist, we don't really want to change 
    # these.
    ShoulderRest = (legs.FL.shoulder.rest + legs.FR.shoulder.rest + legs.BL.shoulder.rest + legs.BR.shoulder.rest)/4
    WristRest = (legs.FL.wrist.rest + legs.FR.wrist.rest + legs.BL.wrist.rest + legs.BR.wrist.rest)/4
    legs.moveServosTo(ShoulderRest, 170, WristRest, Steps, Time)
    gestureStatus = 4

#################################################################
# This function uses a series of small steps to move the legs   #
# in a straight line.  The more steps used, the slower it will  #
# travel from rest to stand.                                    #
# This function uses the RPoR Kinematics.                       #
#################################################################
def restToStand(Steps = 20, Time = 0.03):
    global gestureStatus
    print ("Moving from Rest to Stand position")
    data = legs.getRobotXYZ()
    print(legs)
    #Move the robot up 100mm to around 195 above the ground
    #correcting for and Y error inposition.
    legs.moveRobotRPoRs(-data.get("X"), -data.get("Y"), 100, Steps, Time)
    gestureStatus = 1
    #print(legs)

def stand(Steps = 20, Time = 0.03):
    global gestureStatus
    if gestureStatus == 0:
        crouch(Steps, Time)
        restToStand(Steps, Time)
    elif gestureStatus == 2:
        crouch(Steps, Time)
        legs.moveServosTo(90, 124.45, 115.44, Steps, Time)
    else:
        legs.moveServosTo(90, 124.45, 115.44, Steps, Time)
        #legs.FL.setServoPos(90, 124.45, 115.44)
        #legs.FR.setServoPos(90, 124.45, 115.44)
        #legs.BL.setServoPos(90, 124.45, 115.44)
        #legs.BR.setServoPos(90, 124.45, 115.44)
    gestureStatus = 1
    print(legs)

def standTall():
    global gestureStatus
    legs.autoBalance = False
    legs.autoLevel = False
    legs.moveServosTo(90, 90, 180, Steps, Time)
    #legs.FL.setServoPos(90, 90, 180)
    #legs.FR.setServoPos(90, 90, 180)
    #legs.BL.setServoPos(90, 90, 180)
    #legs.BR.setServoPos(90, 90, 180)
    gestureStatus = 3
    print(legs)

def sit(Steps = 10, Time = 0.05):
    global gestureStatus
    legs.autoBalance = False
    legs.autoLevel = False
    legs.moveServos4D(90-legs.FL.shoulder.pos, 127-legs.FL.arm.pos, 180-legs.FL.wrist.pos, 90-legs.FR.shoulder.pos, 127-legs.FR.arm.pos, 180-legs.FR.wrist.pos, 90-legs.BL.shoulder.pos, 180-legs.BL.arm.pos, 52-legs.BL.wrist.pos, 90-legs.BR.shoulder.pos, 180-legs.BR.arm.pos, 52-legs.BR.wrist.pos, Steps, Time)
    legs.syncServos()
    gestureStatus = 2
    print(legs)

