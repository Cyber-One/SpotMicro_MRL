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
print "Starting the various Gestures Services"


#################################################################
# this command returns all the servos to the starting rest      #
# position.  Handy when calibrating.                            #
#################################################################
def rest(Speed):
    print "Moving to Rest postition"
    setAllServoSpeeds(Speed)
    # Now send the legs to the rest position
    FLShoulder.rest()
    FRShoulder.rest()
    BLShoulder.rest()
    BRShoulder.rest()
    FLArm.rest()
    FRArm.rest()
    BLArm.rest()
    BRArm.rest()
    FLWrist.rest()
    FRWrist.rest()
    BLWrist.rest()
    BRWrist.rest()

#################################################################
# layDown(Speed)                                                #
# When laying down, we want the dog to be as low to the ground  #
# as we can make it.                                            #
# This means the Wrist will be set to the minimum, that is bent #
# as far as we can get it and the Arm will be bent back at a    #
# matching angle within a triangle so that the Wrist part of    #
# the leg is parrallel to the body. An equalateral triangle.    #
# Since the Arm is straight down at 90 degrees, we can add the  #
# Wrist Min angle to 90 to get the target Arm servo position.   #
# Note: WristMin = 50.0                                         #
#################################################################
def Laydown(Speed):
    print "Laying Down"
    setAllServoSpeeds(Speed)
    FLShoulder.rest()
    FRShoulder.rest()
    BLShoulder.rest()
    BRShoulder.rest()
    FLArm.moveTo(WristMin + 90)
    FRArm.moveTo(WristMin + 90)
    BLArm.moveTo(WristMin + 90)
    BRArm.moveTo(WristMin + 90)
    FLWrist.moveTo(WristMin)
    FRWrist.moveTo(WristMin)
    BLWrist.moveTo(WristMin)
    BRWrist.moveTo(WristMin)


def Down(Speed):
    sMoveFeetTo(-93.0, 127.85, -92.24, 93.0, 127.85, 92.24, -93.0, -52.15, -92.24, 93.0, -52.15, -92.24, Speed)

def Up(Speed):
    # Set all the base speeds
    setAllServoSpeeds(Speed*0.5)
    # I found if I move straight to the rest position
    # the robot tends to fall over backwards.
    # To help prevent that, I rotate all the arms back 
    # as far they will go, moving the center of mass
    # forward of the center of contact.
    FLArm.moveTo(ArmMax-1)
    FRArm.moveTo(ArmMax-1)
    BLArm.moveTo(ArmMax-1)
    BRArm.moveToBlocking(ArmMax-1)
    setAllServoSpeeds(Speed)
    # Now send the legs to the rest position
    #sMoveFeetTo(-93.0, 87.405, -207.645, 93.0, 87.405, -207.645, -93.0, -92.595, -207.645, 93.0, -92.595, -207.645, Speed)
    lMoveFeetTo(0.0, -93.0, 87.405, -207.645, 0.0, 93.0, 87.405, -207.645, 0.0, -93.0, -92.595, -207.645, 0.0, 93.0, -92.595, -207.645, Speed, 5)

def Crouch(Speed):
    sMoveFeetTo(-93.0, 87.405, -150.0, 93.0, 87.405, -150.0, -93.0, -92.595, -150.0, 93.0, -92.595, -150.0, 0.3)

def Sit(Speed):
    #sMoveFeetTo(-93.0, 29.5, -226.0, 93.0, 29.5, -226.0, -93.0, -94.0, -105.0, 93.0, -94.0, -101.0, 0.3)
    setAllServoSpeeds(Speed)
    FLShoulder.rest()
    FRShoulder.rest()
    BLShoulder.rest()
    BRShoulder.rest()
    FLArm.moveTo(105)
    FRArm.moveTo(105)
    BLArm.moveTo(ArmMax-1)
    BRArm.moveTo(ArmMax-1)
    FLWrist.moveTo(WristMax)
    FRWrist.moveTo(WristMax)
    BLWrist.moveTo(51)
    BRWrist.moveTo(51)
    
def LeanForward(Speed):
    setAllServoSpeeds(Speed)
    lMoveFeetTo(0.0, -93.0, 37.405, -207.645, 0.0, 93.0, 37.405, -207.645, 0.0, -93.0, -142.595, -207.645, 0.0, 93.0, -142.595, -207.645, Speed, 5)
    sleep(3.0)
    lMoveFeetTo(0.0, -93.0, 87.405, -207.645, 0.0, 93.0, 87.405, -207.645, 0.0, -93.0, -92.595, -207.645, 0.0, 93.0, -92.595, -207.645, 1.0, 5)


def WalkForward(StepSize, StepHeight, Type, Steps):
    #Before starting, lets update the systems memory of where it is.
    # At rest, the X and Y positions are easy to work out.
    # BaseX is +/- the sum of LXS and LST
    # then subtrack an amount off to help with the balance.
    # this doesn't change for forward walking
    BaseX = LXS + LST - 30
    # BaseY is +/- LYS plus any offsets
    BaseY = LYS + 3.0
    Yoffset0 = +(StepSize*0.5)
    Yoffset1 = -(StepSize*0.0)
    Yoffset2 = -(StepSize*0.5)
    Yoffset3 = -(StepSize*1.0)
    # BaseZ is the average height we want the robot to walk at
    BaseZ = 180.0
    # Speed control is another issue to look at.
    Speed = -1
    # For each stride there are 4 step actions, 
    # each action moves one foot forward while the rest 
    # move back 1/3 of a step
    if Type == 0: # Starting to walk
        lMoveFeetTo(StepHeight, -BaseX, BaseY+Yoffset0,   -BaseZ, 0.0,        BaseX, BaseY+Yoffset1,    -BaseZ, 0.0,        -BaseX, -BaseY+Yoffset1, -BaseZ, 0.0,         BaseX, -BaseY+Yoffset1, -BaseZ, Speed, Steps)
        lMoveFeetTo(0.0,        -BaseX, BaseY+Yoffset1,   -BaseZ, 0.0,        BaseX, BaseY+Yoffset2,    -BaseZ, 0.0,        -BaseX, -BaseY+Yoffset2, -BaseZ, StepHeight,  BaseX, -BaseY+Yoffset0, -BaseZ, Speed, Steps)
        lMoveFeetTo(0.0,        -BaseX, BaseY+Yoffset2,   -BaseZ, 0.0,        BaseX, BaseY+Yoffset3,    -BaseZ, StepHeight, -BaseX, -BaseY+Yoffset0, -BaseZ, 0.0,         BaseX, -BaseY+Yoffset1, -BaseZ, Speed, Steps)
        lMoveFeetTo(0.0,        -BaseX, BaseY+Yoffset3,   -BaseZ, StepHeight, BaseX, BaseY+Yoffset0,    -BaseZ, 0.0,        -BaseX, -BaseY+Yoffset1, -BaseZ, 0.0,         BaseX, -BaseY+Yoffset2, -BaseZ, Speed, Steps)
    elif Type == 1: # Walking
        lMoveFeetTo(StepHeight, -BaseX, BaseY+Yoffset0,   -BaseZ, 0.0,        BaseX, BaseY+Yoffset1,    -BaseZ, 0.0,        -BaseX, -BaseY+Yoffset2, -BaseZ, 0.0,         BaseX, -BaseY+Yoffset3, -BaseZ, Speed, Steps)
        lMoveFeetTo(0.0,        -BaseX, BaseY+Yoffset1,   -BaseZ, 0.0,        BaseX, BaseY+Yoffset2,    -BaseZ, 0.0,        -BaseX, -BaseY+Yoffset3, -BaseZ, StepHeight,  BaseX, -BaseY+Yoffset0, -BaseZ, Speed, Steps)
        lMoveFeetTo(0.0,        -BaseX, BaseY+Yoffset2,   -BaseZ, 0.0,        BaseX, BaseY+Yoffset3,    -BaseZ, StepHeight, -BaseX, -BaseY+Yoffset0, -BaseZ, 0.0,         BaseX, -BaseY+Yoffset1, -BaseZ, Speed, Steps)
        lMoveFeetTo(0.0,        -BaseX, BaseY+Yoffset3,   -BaseZ, StepHeight, BaseX, BaseY+Yoffset0,    -BaseZ, 0.0,        -BaseX, -BaseY+Yoffset1, -BaseZ, 0.0,         BaseX, -BaseY+Yoffset2, -BaseZ, Speed, Steps)
    elif Type == 2: # Stopping
        lMoveFeetTo(StepHeight, -BaseX, BaseY+Yoffset1,   -BaseZ, 0.0,        BaseX, BaseY+Yoffset0,    -BaseZ, 0.0,        -BaseX, -BaseY+Yoffset1, -BaseZ, 0.0,         BaseX, -BaseY+Yoffset2, -BaseZ, Speed, Steps)
        lMoveFeetTo(0.0,        -BaseX, BaseY+Yoffset1,   -BaseZ, 0.0,        BaseX, BaseY+Yoffset0,    -BaseZ, 0.0,        -BaseX, -BaseY+Yoffset1, -BaseZ, StepHeight,  BaseX, -BaseY+Yoffset1, -BaseZ, Speed, Steps)
        lMoveFeetTo(0.0,        -BaseX, BaseY+Yoffset1,   -BaseZ, 0.0,        BaseX, BaseY+Yoffset0,    -BaseZ, StepHeight, -BaseX, -BaseY+Yoffset1, -BaseZ, 0.0,         BaseX, -BaseY+Yoffset1, -BaseZ, Speed, Steps)
        lMoveFeetTo(0.0,        -BaseX, BaseY+Yoffset1,   -BaseZ, StepHeight, BaseX, BaseY+Yoffset1,    -BaseZ, 0.0,        -BaseX, -BaseY+Yoffset1, -BaseZ, 0.0,         BaseX, -BaseY+Yoffset1, -BaseZ, Speed, Steps)

def WalkExample():
    updateServoPositions()
    StepLength = 50
    StepHeight = 40.0
    Steps = 10
    WalkForward(StepLength, StepHeight, 0, Steps)
    WalkForward(StepLength, StepHeight, 1, Steps)
    WalkForward(StepLength, StepHeight, 1, Steps)
    WalkForward(StepLength, StepHeight, 1, Steps)
    WalkForward(StepLength, StepHeight, 1, Steps)
    WalkForward(StepLength, StepHeight, 1, Steps)
    WalkForward(StepLength, StepHeight, 1, Steps)
    WalkForward(StepLength, StepHeight, 2, Steps)
