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
print ("Starting the various Servos Services")

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
        FLShoulder.map(ShoulderMin, ShoulderMax, FLShoulderMinPos, FLShoulderMaxPos)
    else:
        FLShoulder.map(ShoulderMin, ShoulderMax, FLShoulderMaxPos, FLShoulderMinPos)
    # The Rest position is a pre-programmed position for the    #
    # servo to move to when you call the rest method.           #
    # Note it works on the input side of the map function.      #
    FLShoulder.setRest(ShoulderRest)
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
    FLShoulder.setAutoDisable(False)
    # Lets just make sure the servo is enabled, it should be but#
    FLShoulder.enable()
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
    # The rest method will send to servo to the pre-programmed  #
    # position as set by the setRest method or if not set, to   #
    # the default position as set using the setRest() function. #
    FLShoulder.rest()

#################################################################
# The Front Left Arm Servo                                      #
#################################################################
EnableFLArm = TestServoControllerExists(FLArmAttachment, EnableFLArm)
if EnableFLArm == True:
    FLArm = Runtime.start("FLArm", "Servo")
    # This next if statement is looking for an inverted servo
    if FLArmMinPos < FLArmMaxPos:
        FLArm.map(ArmMin, ArmMax, FLArmMinPos, FLArmMaxPos)
        FLArm.setInverted(False)
    else:
        FLArm.map(ArmMin, ArmMax, FLArmMaxPos, FLArmMinPos)
        FLArm.setInverted(True)
    FLArm.setRest(ArmRest)
    FLArm.setSpeed(FLArmVelocity)
    FLArm.setAutoDisable(False)
    FLArm.enable()
    FLArm.attach(runtime.getService(FLArmAttachment), FLArmPin)
    FLArm.rest()

#################################################################
# The Front Left Wrist Servo                                    #
#################################################################
EnableFLWrist = TestServoControllerExists(FLWristAttachment, EnableFLWrist)
if EnableFLWrist == True:
    FLWrist = Runtime.start("FLWrist", "Servo")
    # This next if statement is looking for an inverted servo
    if FLWristMinPos < FLWristMaxPos:
        FLWrist.map(WristMin, WristMax, FLWristMinPos, FLWristMaxPos)
        FLWrist.setInverted(False)
    else:
        FLWrist.map(WristMin, WristMax, FLWristMaxPos, FLWristMinPos)
        FLWrist.setInverted(True)
    FLWrist.setRest(WristRest)
    FLWrist.setSpeed(FLWristVelocity)
    FLWrist.setAutoDisable(False)
    FLWrist.enable()
    FLWrist.attach(runtime.getService(FLWristAttachment), FLWristPin)
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
    FRShoulder = Runtime.start("FRShoulder", "Servo")
    # This next if statement is looking for an inverted servo
    if FRShoulderMinPos < FRShoulderMaxPos:
        FRShoulder.map(ShoulderMin, ShoulderMax, FRShoulderMinPos, FRShoulderMaxPos)
        FRShoulder.setInverted(False)
    else:
        FRShoulder.map(ShoulderMin, ShoulderMax, FRShoulderMaxPos, FRShoulderMinPos)
        FRShoulder.setInverted(True)
    FRShoulder.setRest(ShoulderRest)
    FRShoulder.setSpeed(FRShoulderVelocity)
    FRShoulder.setAutoDisable(False)
    FRShoulder.enable()
    FRShoulder.attach(runtime.getService(FRShoulderAttachment), FRShoulderPin)
    FRShoulder.rest()

#################################################################
# The Front Right Arm Servo                                     #
#################################################################
EnableFRArm = TestServoControllerExists(FRArmAttachment, EnableFRArm)
if EnableFRArm == True:
    FRArm = Runtime.start("FRArm", "Servo")
    # This next if statement is looking for an inverted servo
    if FRArmMinPos < FRArmMaxPos:
        FRArm.map(ArmMin, ArmMax, FRArmMinPos, FRArmMaxPos)
        FRArm.setInverted(False)
    else:
        FRArm.map(ArmMin, ArmMax, FRArmMaxPos, FRArmMinPos)
        FRArm.setInverted(True)
    FRArm.setRest(ArmRest)
    FRArm.setSpeed(FRArmVelocity)
    FRArm.setAutoDisable(False)
    FRArm.enable()
    FRArm.attach(runtime.getService(FRArmAttachment), FRArmPin)
    FRArm.rest()

#################################################################
# The Front Right Wrist Servo                                   #
#################################################################
EnableFRWrist = TestServoControllerExists(FRWristAttachment, EnableFRWrist)
if EnableFRWrist == True:
    FRWrist = Runtime.start("FRWrist", "Servo")
    # This next if statement is looking for an inverted servo
    if FRWristMinPos < FRWristMaxPos:
        FRWrist.map(WristMin, WristMax, FRWristMinPos, FRWristMaxPos)
        FRWrist.setInverted(False)
    else:
        FRWrist.map(WristMin, WristMax, FRWristMaxPos, FRWristMinPos)
        FRWrist.setInverted(True)
    FRWrist.setRest(WristRest)
    FRWrist.setSpeed(FRWristVelocity)
    FRWrist.setAutoDisable(False)
    FRWrist.enable()
    FRWrist.attach(runtime.getService(FRWristAttachment), FRWristPin)
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
    BLShoulder = Runtime.start("BLShoulder", "Servo")
    # This next if statement is looking for an inverted servo
    if BLShoulderMinPos < BLShoulderMaxPos:
        BLShoulder.map(ShoulderMin, ShoulderMax, BLShoulderMinPos, BLShoulderMaxPos)
        BLShoulder.setInverted(False)
    else:
        BLShoulder.map(ShoulderMin, ShoulderMax, BLShoulderMaxPos, BLShoulderMinPos)
        BLShoulder.setInverted(True)
    BLShoulder.setRest(ShoulderRest)
    BLShoulder.setSpeed(BLShoulderVelocity)
    BLShoulder.setAutoDisable(False)
    BLShoulder.enable()
    BLShoulder.attach(runtime.getService(BLShoulderAttachment), BLShoulderPin)
    BLShoulder.rest()

#################################################################
# The Back Left Arm Servo                                       #
#################################################################
EnableBLArm = TestServoControllerExists(BLArmAttachment, EnableBLArm)
if EnableBLArm == True:
    BLArm = Runtime.start("BLArm", "Servo")
    # This next if statement is looking for an inverted servo
    if BLArmMinPos < BLArmMaxPos:
        BLArm.map(ArmMin, ArmMax, BLArmMinPos, BLArmMaxPos)
        BLArm.setInverted(False)
    else:
        BLArm.map(ArmMin, ArmMax, BLArmMaxPos, BLArmMinPos)
        BLArm.setInverted(True)
    BLArm.setRest(ArmRest)
    BLArm.setSpeed(BLArmVelocity)
    BLArm.setAutoDisable(False)
    BLArm.enable()
    BLArm.attach(runtime.getService(BLArmAttachment), BLArmPin)
    BLArm.rest()

#################################################################
# The Back Left Wrist Servo                                     #
#################################################################
EnableBLWrist = TestServoControllerExists(BLWristAttachment, EnableBLWrist)
if EnableBLWrist == True:
    BLWrist = Runtime.start("BLWrist", "Servo")
    # This next if statement is looking for an inverted servo
    if BLWristMinPos < BLWristMaxPos:
        BLWrist.map(WristMin, WristMax, BLWristMinPos, BLWristMaxPos)
        BLWrist.setInverted(False)
    else:
        BLWrist.map(WristMin, WristMax, BLWristMaxPos, BLWristMinPos)
        BLWrist.setInverted(True)
    BLWrist.setRest(WristRest)
    BLWrist.setSpeed(BLWristVelocity)
    BLWrist.setAutoDisable(False)
    BLWrist.enable()
    BLWrist.attach(runtime.getService(BLWristAttachment), BLWristPin)
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
    BRShoulder = Runtime.start("BRShoulder", "Servo")
    # This next if statement is looking for an inverted servo
    if BRShoulderMinPos < BRShoulderMaxPos:
        BRShoulder.map(ShoulderMin, ShoulderMax, BRShoulderMinPos, BRShoulderMaxPos)
        BRShoulder.setInverted(False)
    else:
        BRShoulder.map(ShoulderMin, ShoulderMax, BRShoulderMaxPos, BRShoulderMinPos)
        BRShoulder.setInverted(True)
    BRShoulder.setRest(ShoulderRest)
    BRShoulder.setSpeed(BRShoulderVelocity)
    BRShoulder.setAutoDisable(False)
    BRShoulder.enable()
    BRShoulder.attach(runtime.getService(BRShoulderAttachment), BRShoulderPin)
    BRShoulder.rest()

#################################################################
# The Back Right Arm Servo                                      #
#################################################################
EnableBRArm = TestServoControllerExists(BRArmAttachment, EnableBRArm)
if EnableBRArm == True:
    BRArm = Runtime.start("BRArm", "Servo")
    # This next if statement is looking for an inverted servo
    if BRArmMinPos < BRArmMaxPos:
        BRArm.map(ArmMin, ArmMax, BRArmMinPos, BRArmMaxPos)
        BRArm.setInverted(False)
    else:
        BRArm.map(ArmMin, ArmMax, BRArmMaxPos, BRArmMinPos)
        BRArm.setInverted(True)
    BRArm.setRest(ArmRest)
    BRArm.setSpeed(BRArmVelocity)
    BRArm.setAutoDisable(False)
    BRArm.enable()
    BRArm.attach(runtime.getService(BRArmAttachment), BRArmPin)
    BRArm.rest()

#################################################################
# The Back Right Wrist Servo                                    #
#################################################################
EnableBRWrist = TestServoControllerExists(BRWristAttachment, EnableBRWrist)
if EnableBRWrist == True:
    BRWrist = Runtime.start("BRWrist", "Servo")
    # This next if statement is looking for an inverted servo
    if BRWristMinPos < BRWristMaxPos:
        BRWrist.map(WristMin, WristMax, BRWristMinPos, BRWristMaxPos)
        BRWrist.setInverted(False)
    else:
        BRWrist.map(WristMin, WristMax, BRWristMaxPos, BRWristMinPos)
        BRWrist.setInverted(True)
    BRWrist.setRest(WristRest)
    BRWrist.setSpeed(BRWristVelocity)
    BRWrist.setAutoDisable(False)
    BRWrist.enable()
    BRWrist.attach(runtime.getService(BRWristAttachment), BRWristPin)
    BRWrist.rest()

