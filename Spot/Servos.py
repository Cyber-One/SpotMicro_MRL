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
# Servos.py                                                     #
# This file is to start all the servos used in the Robot        #
#                                                               #
#################################################################
print "Starting the various Servos Services"

#################################################################
# Load the configuration for the Servos.                        #
#################################################################
execfile(RuningFolder+'/1_Configuration/3_Servo_Config.py')

#################################################################
#                                                               #
# Servo Front Left Leg Group                                    #
#                                                               #
#################################################################
#################################################################
# The Front Left Shoulder Servo                                 #
#################################################################

# This line is a sanity check.  It makes sure the controller we #
# plan to attach the servo to is actually setup.  If not, it    #
# disables the servo.                                           #
EnableFLShoulder = TestServoControllerExists(FLShoulderAttachment, EnableFLShoulder)
if EnableFLShoulder == True:
    # The Servo service is designed to operate a number of      #
    # different types of servos via different controllers       #
    # while providing a common interface for your robot.        #
    # Before we can use a servo, we must first create the       #
    # servo object by using the Runtime service and the         #
    # start function, passing in the Name we want to            #
    # call our new servo service as well as the type of         #
    # service, in this case "Servo".                            #
    # We then assign this new object to a variable.             #
    # In this example, we are assigning a Servo Service to      #
    # the variable FLShoulder
    FLShoulder = Runtime.start("FLShoulder", "Servo")
    # Once we have a Servo service, we need to attach it to     #
    # a controller on our system.  There can be more than one   #
    # controller or even types of controllers within the        #
    # system, so we need to tell the service where to find      #
    # the controller and what pin to connect ther servo         #
    # service to.  For that we use the attach method.           #
    # This method takes two parameters, the first is the        #
    # service object.                                           #
    # The second parameter is the pin on the controller that    #
    # the servo will be attached to.                            #
    # Because we have a number of options for the controller    #
    # service, we will use a feature in the runtime service     #
    # that will return the service object based on it's name.   #
    FLShoulder.attach(runtime.getService(FLShoulderAttachment), FLShoulderPin)
    # A lot of servos will have a 180 degree range of motion.   #
    # however there are some with more range and others with    #
    # less range, the servo service cannot tell these types     #
    # apart, the solution is to Map them :-)                    #
    # If you have a 270 degree servo, the same PWM signal       #
    # range for the 180 dgree servos will rotate 270 degree.    #
    # What we can do is Map the 0 - 180 to the 0 - 270 degrees  #
    # In this case, we would map the 0 - 270 as the input to    #
    # the 0 - 180 on the output. Then when you adjust the       #
    # output by 90 degrees the servo will turn 90 degrees.      #
    # This  if statement is looking for an inverted servo       #
    if FLShoulderMinPos < FLShoulderMaxPos:
        FLShoulder.map(30, 150, FLShoulderMinPos, FLShoulderMaxPos)
    else:
        FLShoulder.map(30, 150, FLShoulderMaxPos, FLShoulderMinPos)
    # The Rest position is a pre-programmed position for the    #
    # servo to move to when you call the rest method.           #
    # Note it works on the input side of the map function.      #
    FLShoulder.setRest(90)
    # On occasion you may need to reverse the direction of a    #
    # servo. You may have an arm on each side of the robot,     #
    # where 90 degree it pointing forward, but 0 degrees has    #
    # one arm move up while the other moves down.  In this      #
    # case you may want both servo to mover the arms down.      #
    # What you will want to do is Invert the direction of one   #
    # of the servos so that both are down at 0 degrees.         #
    # Setting the setInvert to True will invert the servo.      #
    if FLShoulderMinPos < FLShoulderMaxPos:
        FLShoulder.setInverted(False)
    else:
        FLShoulder.setInverted(True)
    # Without any speed control, when you change a servos       #
    # position, the servo will try and rotate to the new        #
    # position as fast as it can.  This can at times be         #
    # undesirable, resulting in your whole robot shaking or     #
    # worse falling over causing damage.  The speed at which    #
    # the servo rotate can limited or controlled by sending a   #
    # series of position updates between the current position   #
    # and the target position.  The rate of rotation is set     #
    # in degrees per second.                                    #
    # A value of -1 disables speed control.                     #
    FLShoulder.setSpeed(FLShoulderVelocity)
    # The Servo service has a feature where it will disable a   #
    # servos, saving power and potentially preventing the       #
    # servo from burning out.  This feature can be disabled     #
    # when disabling the servo would be bad.                    #
    FLShoulder.setAutoDisable(True)
    # The rest method will send to servo to the pre-programmed  #
    # position as set by the setRest method or if not set, to   #
    # the default position as set using the setRest() function. #
    FLShoulder.rest()

#################################################################
# The Front Left Arm Servo                                      #
#################################################################
EnableFLArm = TestServoControllerExists(FLArmAttachment, EnableFLArm)
if EnableFLArm == True:
    FLArm = Runtime.createAndStart("FLArm", "Servo")
    FLArm.attach(runtime.getService(FLArmAttachment), FLArmPin)
    # This next if statement is looking for an inverted servo
    if FLArmMinPos < FLArmMaxPos:
        FLArm.map(0, 180, FLArmMinPos, FLArmMaxPos)
        FLArm.setInverted(False)
    else:
        FLArm.map(0, 180, FLArmMaxPos, FLArmMinPos)
        FLArm.setInverted(True)
    FLArm.setRest(120)
    FLArm.setSpeed(FLArmVelocity)
    FLArm.setAutoDisable(True)
    FLArm.rest()

#################################################################
# The Front Left Wrist Servo                                    #
#################################################################
EnableFLWrist = TestServoControllerExists(FLWristAttachment, EnableFLWrist)
if EnableFLWrist == True:
    FLWrist = Runtime.createAndStart("FLWrist", "Servo")
    FLWrist.attach(runtime.getService(FLWristAttachment), FLWristPin)
    # This next if statement is looking for an inverted servo
    if FLWristMinPos < FLWristMaxPos:
        FLWrist.map(25, 180, FLWristMinPos, FLWristMaxPos)
        FLWrist.setInverted(False)
    else:
        FLWrist.map(25, 180, FLWristMaxPos, FLWristMinPos)
        FLWrist.setInverted(True)
    FLWrist.setRest(120)
    FLWrist.setSpeed(FLWristVelocity)
    FLWrist.setAutoDisable(True)
    FLWrist.rest()


#################################################################
#                                                               #
# Servo Front Right Leg Group                                   #
#                                                               #
#################################################################

#################################################################
# The Front Right Shoulder Servo                                #
#################################################################
EnableFRShoulder = TestServoControllerExists(FRShoulderAttachment, EnableFRShoulder)
if EnableFRShoulder == True:
    FRShoulder = Runtime.createAndStart("FRShoulder", "Servo")
    FRShoulder.attach(runtime.getService(FRShoulderAttachment), FRShoulderPin)
    # This next if statement is looking for an inverted servo
    if FRShoulderMinPos < FRShoulderMaxPos:
        FRShoulder.map(30, 150, FRShoulderMinPos, FRShoulderMaxPos)
        FRShoulder.setInverted(False)
    else:
        FRShoulder.map(30, 150, FRShoulderMaxPos, FRShoulderMinPos)
        FRShoulder.setInverted(True)
    FRShoulder.setRest(90)
    FRShoulder.setSpeed(FRShoulderVelocity)
    FRShoulder.setAutoDisable(True)
    FRShoulder.rest()

#################################################################
# The Front Right Arm Servo                                     #
#################################################################
EnableFRArm = TestServoControllerExists(FRArmAttachment, EnableFRArm)
if EnableFRArm == True:
    FRArm = Runtime.createAndStart("FRArm", "Servo")
    FRArm.attach(runtime.getService(FRArmAttachment), FRArmPin)
    # This next if statement is looking for an inverted servo
    if FRArmMinPos < FRArmMaxPos:
        FRArm.map(0, 180, FRArmMinPos, FRArmMaxPos)
        FRArm.setInverted(False)
    else:
        FRArm.map(0, 180, FRArmMaxPos, FRArmMinPos)
        FRArm.setInverted(True)
    FRArm.setRest(120)
    FRArm.setSpeed(FRArmVelocity)
    FRArm.setAutoDisable(True)
    FRArm.rest()

#################################################################
# The Front Right Wrist Servo                                   #
#################################################################
EnableFRWrist = TestServoControllerExists(FRWristAttachment, EnableFRWrist)
if EnableFRWrist == True:
    FRWrist = Runtime.createAndStart("FRWrist", "Servo")
    FRWrist.attach(runtime.getService(FRWristAttachment), FRWristPin)
    # This next if statement is looking for an inverted servo
    if FRWristMinPos < FRWristMaxPos:
        FRWrist.map(25, 180, FRWristMinPos, FRWristMaxPos)
        FRWrist.setInverted(False)
    else:
        FRWrist.map(25, 180, FRWristMaxPos, FRWristMinPos)
        FRWrist.setInverted(True)
    FRWrist.setRest(120)
    FRWrist.setSpeed(FRWristVelocity)
    FRWrist.setAutoDisable(True)
    FRWrist.rest()


#################################################################
#                                                               #
# Servo Back Left Leg Group                                     #
#                                                               #
#################################################################

#################################################################
# The Back Left Shoulder Servo                                  #
#################################################################
EnableBLShoulder = TestServoControllerExists(BLShoulderAttachment, EnableBLShoulder)
if EnableBLShoulder == True:
    BLShoulder = Runtime.createAndStart("BLShoulder", "Servo")
    BLShoulder.attach(runtime.getService(BLShoulderAttachment), BLShoulderPin)
    # This next if statement is looking for an inverted servo
    if BLShoulderMinPos < BLShoulderMaxPos:
        BLShoulder.map(30, 150, BLShoulderMinPos, BLShoulderMaxPos)
        BLShoulder.setInverted(False)
    else:
        BLShoulder.map(30, 150, BLShoulderMaxPos, BLShoulderMinPos)
        BLShoulder.setInverted(True)
    BLShoulder.setRest(90)
    BLShoulder.setSpeed(BLShoulderVelocity)
    BLShoulder.setAutoDisable(True)
    BLShoulder.rest()

#################################################################
# The Back Left Arm Servo                                       #
#################################################################
EnableBLArm = TestServoControllerExists(BLArmAttachment, EnableBLArm)
if EnableBLArm == True:
    BLArm = Runtime.createAndStart("BLArm", "Servo")
    BLArm.attach(runtime.getService(BLArmAttachment), BLArmPin)
    # This next if statement is looking for an inverted servo
    if BLArmMinPos < BLArmMaxPos:
        BLArm.map(0, 180, BLArmMinPos, BLArmMaxPos)
        BLArm.setInverted(False)
    else:
        BLArm.map(0, 180, BLArmMaxPos, BLArmMinPos)
        BLArm.setInverted(True)
    BLArm.setRest(120)
    BLArm.setSpeed(BLArmVelocity)
    BLArm.setAutoDisable(True)
    BLArm.rest()

#################################################################
# The Back Left Wrist Servo                                     #
#################################################################
EnableBLWrist = TestServoControllerExists(BLWristAttachment, EnableBLWrist)
if EnableBLWrist == True:
    BLWrist = Runtime.createAndStart("BLWrist", "Servo")
    BLWrist.attach(runtime.getService(BLWristAttachment), BLWristPin)
    # This next if statement is looking for an inverted servo
    if BLWristMinPos < BLWristMaxPos:
        BLWrist.map(25, 180, BLWristMinPos, BLWristMaxPos)
        BLWrist.setInverted(False)
    else:
        BLWrist.map(25, 180, BLWristMaxPos, BLWristMinPos)
        BLWrist.setInverted(True)
    BLWrist.setRest(120)
    BLWrist.setSpeed(BLWristVelocity)
    BLWrist.setAutoDisable(True)
    BLWrist.rest()


#################################################################
#                                                               #
# Servo Back Right Leg Group                                    #
#                                                               #
#################################################################

#################################################################
# The Back Right Shoulder Servo                                 #
#################################################################
EnableBRShoulder = TestServoControllerExists(BRShoulderAttachment, EnableBRShoulder)
if EnableBRShoulder == True:
    BRShoulder = Runtime.createAndStart("BRShoulder", "Servo")
    BRShoulder.attach(runtime.getService(BRShoulderAttachment), BRShoulderPin)
    # This next if statement is looking for an inverted servo
    if BRShoulderMinPos < BRShoulderMaxPos:
        BRShoulder.map(30, 150, BRShoulderMinPos, BRShoulderMaxPos)
        BRShoulder.setInverted(False)
    else:
        BRShoulder.map(30, 150, BRShoulderMaxPos, BRShoulderMinPos)
        BRShoulder.setInverted(True)
    BRShoulder.setRest(90)
    BRShoulder.setSpeed(BRShoulderVelocity)
    BRShoulder.setAutoDisable(True)
    BRShoulder.rest()

#################################################################
# The Back Right Arm Servo                                      #
#################################################################
EnableBRArm = TestServoControllerExists(BRArmAttachment, EnableBRArm)
if EnableBRArm == True:
    BRArm = Runtime.createAndStart("BRArm", "Servo")
    BRArm.attach(runtime.getService(BRArmAttachment), BRArmPin)
    # This next if statement is looking for an inverted servo
    if BRArmMinPos < BRArmMaxPos:
        BRArm.map(0, 180, BRArmMinPos, BRArmMaxPos)
        BRArm.setInverted(False)
    else:
        BRArm.map(0, 180, BRArmMaxPos, BRArmMinPos)
        BRArm.setInverted(True)
    BRArm.setRest(120)
    BRArm.setSpeed(BRArmVelocity)
    BRArm.setAutoDisable(True)
    BRArm.rest()

#################################################################
# The Back Right Wrist Servo                                    #
#################################################################
EnableBRWrist = TestServoControllerExists(BRWristAttachment, EnableBRWrist)
if EnableBRWrist == True:
    BRWrist = Runtime.createAndStart("BRWrist", "Servo")
    BRWrist.attach(runtime.getService(BRWristAttachment), BRWristPin)
    # This next if statement is looking for an inverted servo
    if BRWristMinPos < BRWristMaxPos:
        BRWrist.map(25, 180, BRWristMinPos, BRWristMaxPos)
        BRWrist.setInverted(False)
    else:
        BRWrist.map(25, 180, BRWristMaxPos, BRWristMinPos)
        BRWrist.setInverted(True)
    BRWrist.setRest(120)
    BRWrist.setSpeed(BRWristVelocity)
    BRWrist.setAutoDisable(True)
    BRWrist.rest()

