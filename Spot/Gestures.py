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
    # Now send the legs to the rest position
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
    lMoveFeetTo("L", -93.0, 87.405, -207.645, "L", 93.0, 87.405, -207.645, "L", -93.0, -92.595, -207.645, "L", 93.0, -92.595, -207.645, Speed, 5)

def Crouch(Speed):
    sMoveFeetTo(-93.0, 87.405, -150.0, 93.0, 87.405, -150.0, -93.0, -92.595, -150.0, 93.0, -92.595, -150.0, 0.3)

def Sit(Speed):
    sMoveFeetTo(-93.0, 10.0, -219.0, 93.0, 10.0, -219.0, -93.0, -105.677, -113.0, 93.0, -105.677, -113.0, 0.3)
    
def LeanForward(Speed):
    setAllServoSpeeds(Speed)
    lMoveFeetTo("L", -93.0, 37.405, -207.645, "L", 93.0, 37.405, -207.645, "L", -93.0, -142.595, -207.645, "L", 93.0, -142.595, -207.645, Speed, 5)
    sleep(3.0)
    lMoveFeetTo("L", -93.0, 87.405, -207.645, "L", 93.0, 87.405, -207.645, "L", -93.0, -92.595, -207.645, "L", 93.0, -92.595, -207.645, Speed, 5)
