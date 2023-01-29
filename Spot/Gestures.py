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
import FootClass

#################################################################
# this command returns all the servos to the starting rest      #
# position and makes sure all the servos are updated.           #
# Handy when calibrating.                                       #
#################################################################
def rest():
    print ("Moving to Rest postition")
    legs.FL.updateServo()
    legs.FR.updateServo()
    legs.BL.updateServo()
    legs.BR.updateServo()
    legs.rest()
    legs.syncServos()
    print(legs)



def Stand():
    legs.FL.setServoPos(90, 139, 90)
    legs.FR.setServoPos(90, 139, 90)
    legs.BL.setServoPos(90, 139, 90)
    legs.BR.setServoPos(90, 139, 90)
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

