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
#################################################################
#                                                               #
# The Front Left Shoulder Servo                                 #
# This servo swings the leg in and out relative to the line     #
# of the body.  The min is closer to the centerline and max is  #
# further out                                                   #
#                                                               #
#################################################################
EnableFLShoulder = True # True or False
# This is the controller the Front Left Shoulder Servo is       #
# attached to                                                   #
FLShoulderAttachment = "Back"
# The controller will have a number of pis, this is the pin     #
# this servo is connected to.                                   #
FLShoulderPin = 12
# The is the value from testing where the Front Left Shoulder   #
# is all the way towards the center line of the both            #
FLShoulderMinPos = 54
# This is the value from testing where the Front Left Shoulder  #
# is all the way as far from the centerline as is possible      #
FLShoulderMaxPos = 154
# This is the speed that the Front Left Shoulder moves at.      #
# -1 is no speed limit, the Front Left Shoulder will move as    #
# fast as possible.                                             #
FLShoulderVelocity = 272

#################################################################
#                                                               #
# The Front Left Arm                                            #
# This servo moves the arm (between the shoulder and the wrist) #
# back and forward.  Min is all the way back and max is all the #
# way forward.                                                  #
#                                                               #
#################################################################
EnableFLArm = True
FLArmAttachment = "Back"
FLArmPin = 13
FLArmMinPos = 26
FLArmMaxPos = 169
FLArmVelocity = 272

#################################################################
#                                                               #
# The Front Left Wrist                                          #
# This servo swings the lower leg back and forward.             #
# Min is all the way forward and max is all the way back.       #
#                                                               #
#################################################################
EnableFLWrist = True
FLWristAttachment = "Back"
FLWristPin = 14
FLWristMinPos = 37
FLWristMaxPos = 147
FLWristVelocity = 272


#################################################################
#                                                               #
# Servo Front Right Leg Group                                   #
#                                                               #
#################################################################
#                                                               #
# The Front Right Shoulder                                      #
# This servo swings the leg in and out relative to the line     #
# of the body.  The min is closer to the centerline and max is  #
# further out                                                   #
#                                                               #
#################################################################
EnableFRShoulder = True
FRShoulderAttachment = "Back"
FRShoulderPin = 0
FRShoulderMinPos = 164
FRShoulderMaxPos = 76
FRShoulderVelocity = 272

#################################################################
#                                                               #
# The Front Right Arm                                           #
# This servo moves the arm (between the shoulder and the wrist) #
# back and forward.  Min is all the way back and max is all the #
# way forward.                                                  #
#                                                               #
#################################################################
EnableFRArm = True
FRArmAttachment = "Back"
FRArmPin = 1
FRArmMinPos = 168
FRArmMaxPos = 29
FRArmVelocity = 272

#################################################################
#                                                               #
# The Front Right Wrist
# This servo swings the lower leg back and forward.             #
# Min is all the way forward and max is all the way back.       #
#                                                               #
#################################################################
EnableFRWrist = True
FRWristAttachment = "Back"
FRWristPin = 2
FRWristMinPos = 171
FRWristMaxPos = 56
FRWristVelocity = 272

#################################################################
#                                                               #
# Servo Back Left Leg Group                                     #
#                                                               #
#################################################################
#                                                               #
# The Back Left Shoulder                                        #
# This servo swings the leg in and out relative to the line     #
# of the body.  The min is closer to the centerline and max is  #
# further out                                                   #
#                                                               #
#################################################################
EnableBLShoulder = True
BLShoulderAttachment = "Back"
BLShoulderPin = 8
BLShoulderMinPos = 141
BLShoulderMaxPos = 37
BLShoulderVelocity = 272

#################################################################
#                                                               #
# The Back Left Arm                                             #
# This servo moves the arm (between the shoulder and the wrist) #
# back and forward.  Min is all the way back and max is all the #
# way forward.                                                  #
#                                                               #
#################################################################
EnableBLArm = True
BLArmAttachment = "Back"
BLArmPin = 9
BLArmMinPos = 28
BLArmMaxPos = 173
BLArmVelocity = 272

#################################################################
#                                                               #
# The Back Left Wrist                                           #
# This servo swings the lower leg back and forward.             #
# Min is all the way forward and max is all the way back.       #
#                                                               #
#################################################################
EnableBLWrist = True
BLWristAttachment = "Back"
BLWristPin = 10
BLWristMinPos = 35
BLWristMaxPos = 147
BLWristVelocity = 272

#################################################################
#                                                               #
# Servo Back Right Leg Group                                    #
#                                                               #
#################################################################
#                                                               #
# The Back Right Shoulder                                       #
# This servo swings the leg in and out relative to the line     #
# of the body.  The min is closer to the centerline and max is  #
# further out                                                   #
#                                                               #
#################################################################
EnableBRShoulder = True
BRShoulderAttachment = "Back"
BRShoulderPin = 4
BRShoulderMinPos = 54
BRShoulderMaxPos = 158
BRShoulderVelocity = 272

#################################################################
#                                                               #
# The Back Right Arm                                            #
# This servo moves the arm (between the shoulder and the wrist) #
# back and forward.  Min is all the way back and max is all the #
# way forward.                                                  #
#                                                               #
#################################################################
EnableBRArm = True
BRArmAttachment = "Back"
BRArmPin = 5
BRArmMinPos = 177
BRArmMaxPos = 40
BRArmVelocity = 272

#################################################################
#                                                               #
# The Back Right Wrist                                          #
# This servo swings the lower leg back and forward.             #
# Min is all the way forward and max is all the way back.       #
#                                                               #
#################################################################
EnableBRWrist = True
BRWristAttachment = "Back"
BRWristPin = 6
BRWristMinPos = 177
BRWristMaxPos = 58
BRWristVelocity = 272
