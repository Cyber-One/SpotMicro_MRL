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
# this command returns all the servos to the starting rest      #
# position and makes sure all the servos are updated.           #
# Handy when calibrating.                                       #
#################################################################
def rest(Steps = 10, Time = 0.1):
    print ("Moving to Rest postition")
    legs.FL.updateServo()
    legs.FR.updateServo()
    legs.BL.updateServo()
    legs.BR.updateServo()
    data = legs.getRobotXYZ()
    legs.moveRobotRPoRs(0, 0, data.get("Z")+100, Steps, Time)
    #data = legs.getRobotXYZ()
    #print(legs.getRobotXYZ())
    Shoulder = (legs.FL.shoulder.pos + legs.FR.shoulder.pos + legs.BL.shoulder.pos + legs.BR.shoulder.pos)/4
    Arm = (legs.FL.arm.pos + legs.FR.arm.pos + legs.BL.arm.pos + legs.BR.arm.pos)/4
    Wrist = (legs.FL.wrist.pos + legs.FR.wrist.pos + legs.BL.wrist.pos + legs.BR.wrist.pos)/4
    ShoulderRest = (legs.FL.shoulder.rest + legs.FR.shoulder.rest + legs.BL.shoulder.rest + legs.BR.shoulder.rest)/4
    ArmRest = (legs.FL.arm.rest + legs.FR.arm.rest + legs.BL.arm.rest + legs.BR.arm.rest)/4
    WristRest = (legs.FL.wrist.rest + legs.FR.wrist.rest + legs.BL.wrist.rest + legs.BR.wrist.rest)/4
    legs.moveServos(ShoulderRest - Shoulder, ArmRest - Arm, WristRest - Wrist, Steps, Time)
    legs.rest()
    legs.syncServos()
    print(legs)

#################################################################
# This function uses a series of small steps to move the legs   #
# in a straight line.  The more steps used, the slower it will  #
# travel from rest to stand.                                    #
# This function uses the RPoR Kinematics.                       #
#################################################################
def restToStand(steps, Time = 0.1):
    print ("Moving from Rest to Stand position")
    #Rotate the arm to pivot the feet under the shoulders.
    legs.moveServos(0, 46, 0, steps, Time) 
    #Get the robots current position. 
    data = legs.getRobotXYZ()
    print(legs.getRobotXYZ())
    #Move the robot up 100mm to around 195 above the ground
    #correcting for and Y error inposition.
    legs.moveRobotRPoRs(0, -data.get("Y"), 100, steps, Time)
    print(legs.getRobotXYZ())

def Stand():
    legs.FL.setServoPos(90, 140.64, 86.06)
    legs.FR.setServoPos(90, 140.64, 86.06)
    legs.BL.setServoPos(90, 140.64, 86.06)
    legs.BR.setServoPos(90, 140.64, 86.06)
    legs.syncServos()
    print(legs)

def StandTall():
    legs.FL.setServoPos(90, 90, 180)
    legs.FR.setServoPos(90, 90, 180)
    legs.BL.setServoPos(90, 90, 180)
    legs.BR.setServoPos(90, 90, 180)
    legs.syncServos()
    print(legs)

def Sit():
    Stand()
    legs.FL.setServoPos(90, 90, 180)
    legs.FR.setServoPos(90, 90, 180)
    legs.BL.setServoPos(90, 160, 50)
    legs.BR.setServoPos(90, 160, 50)
    legs.syncServos()
    print(legs)

