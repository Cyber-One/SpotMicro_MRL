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
# 3_Servo_Head_Config.py                                        #
# This is where the configuration settings live for the         #
# varoius controllers.                                          #
#                                                               #
################################################################
print "Creating the Servo Config"
#################################################################
#                                                               #
# Servo Front Left Leg Group                                    #
#                                                               #
#################################################################
# Each servo has a number of parameters that need to be setup   #
# before it can be used, these include where it's attached      #
# and how far it can be moved.                                  #
# The default values will be one of our controllers.            #
# "arduinoNano", "Back", "Front".                               #
# If a new controller is released or more servos are added,     #
# then add it to this list and to each of the servos in the     #
# related Servo.py file.                                        #
# In some cases, the direction of travel is sometime in the     #
# oposite direction to what we need.  In this case, swap the    #
# Min and Max pos, this will swap the direction to what we need.#

# The Front Left Shoulder Servo                                 #
# TThis servo swings the leg in and out relative to the line    #
# of the body.                                                  #
EnableFLShoulder = True # True or False
# This is the controller the Front Left Shoulder Servo is       #
# attached to                                                   #
FLShoulderAttachment = "Back"
# The controller will have a number of pis, this is the pin     #
# this servo is connected to.                                   #
FLShoulderPin = 9
# The is the value from testing where the Front Left Shoulder   #
# is all the way towards the center line of the both            #
FLShoulderMinPos = 70
# This is the value from testing where the Front Left Shoulder  #
# is all the way as far from the centerline as is possible      #
FLShoulderMaxPos = 140
# This is the speed that the Front Left Shoulder moves at.      #
# -1 is no speed limit, the Front Left Shoulder will move as    #
# fast as possible.                                             #
FLShoulderVelocity = -1

# The Front Left Arm
EnableFLArm = True
FLArmAttachment = "Back"
FLArmPin = 15
FLArmMinPos = 0
FLArmMaxPos = 180
FLArmVelocity = -1

# The Front Left Wrist
EnableFLWrist = True
FLWristAttachment = "Back"
FLWristPin = 14
FLWristMinPos = 0
FLWristMaxPos = 180
FLWristVelocity = -1


#################################################################
#                                                               #
# Servo Front Right Leg Group                                    #
#                                                               #
#################################################################

# The Front Right Shoulder
EnableFRShoulder = True
FRShoulderAttachment = "Back"
FRShoulderPin = 13
FRShoulderMinPos = 0
FRShoulderMaxPos = 180
FRShoulderVelocity = -1

# The Front Right Arm
EnableFRArm = True
FRArmAttachment = "Back"
FRArmPin = 15
FRArmMinPos = 0
FRArmMaxPos = 180
FRArmVelocity = -1

# The Front Right Wrist
EnableFRWrist = True
FRWristAttachment = "Back"
FRWristPin = 14
FRWristMinPos = 0
FRWristMaxPos = 180
FRWristVelocity = -1

#################################################################
#                                                               #
# Servo Back Left Leg Group                                    #
#                                                               #
#################################################################

# The Back Left Shoulder
EnableBLShoulder = True
BLShoulderAttachment = "Back"
BLShoulderPin = 13
BLShoulderMinPos = 0
BLShoulderMaxPos = 180
BLShoulderVelocity = -1

# The Back Left Arm
EnableBLArm = True
BLArmAttachment = "Back"
BLArmPin = 15
BLArmMinPos = 0
BLArmMaxPos = 180
BLArmVelocity = -1

# The Back Left Wrist
EnableBLWrist = True
BLWristAttachment = "Back"
BLWristPin = 14
BLWristMinPos = 0
BLWristMaxPos = 180
BLWristVelocity = -1

#################################################################
#                                                               #
# Servo Back Right Leg Group                                    #
#                                                               #
#################################################################

# The Back Right Shoulder
EnableBRShoulder = True
BRShoulderAttachment = "Back"
BRShoulderPin = 13
BRShoulderMinPos = 0
BRShoulderMaxPos = 180
BRShoulderVelocity = -1

# The Back Right Arm
EnableBRArm = True
BRArmAttachment = "Back"
BRArmPin = 15
BRArmMinPos = 0
BRArmMaxPos = 180
BRArmVelocity = -1

# The Back Right Wrist
EnableBRWrist = True
BRWristAttachment = "Back"
BRWristPin = 14
BRWristMinPos = 0
BRWristMaxPos = 180
BRWristVelocity = -1
