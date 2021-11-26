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
# Controllers.py                                                #
# This file is to start any major controllers                   #
# we might need.                                                #
#                                                               #
#################################################################
print "Starting the various Controllers"

#################################################################
# Load the configuration for the Controllers.                   #
#################################################################
execfile(RuningFolder+'/1_Configuration/2_Controller_Config.py')

#################################################################
# Start the Raspberry Pi service.                               #
# The core of the Spot Micro build,                             #
# is the Raspberry Pi 4 (Raspi4) Single Board Computer (SBC)    #
# This small low cost computer, but it is not very powerful.    #
# The Raspi4 has two I2C ports built in,                        #
# Port 0 is used for the microSD card,                          #
# while Port 1 is available for us to use.                      #
#################################################################
if EnableRaspberryPi == True:
    print "-Starting the Raspberry Pi Service"
    raspi = Runtime.createAndStart("raspi","RasPi")

#################################################################
# Start the Arduino Nano connected using /dev/ttyUSB0           #
# In the Spot build, I'm using an Arduino Nano for the two      #
# Ultrasonic Sensors.                                           #
# The Arduino also has an I2C Port 0 if we need to use it.      #
#################################################################
if EnableArduinoNano == True:
    print "-Starting the Arduino Nano Service"
    arduinoNano = Runtime.start("arduinoNano","Arduino")
    arduinoNano.setBoardNano()
    arduinoNano.connect(ArduinoNanoComPort)

#################################################################
# To assist in performing a sanity test, the following function #
# will return either the CurrentState or False based on the     #
# name of the configured service for I2C supporting services.   #
#################################################################
def TestI2CControllerExists(ControllerName, CurrentState):
    if ((ControllerName == "raspi" and EnableRaspberryPi)
        or (ControllerName == "arduinoNano" and EnableArduinoNano)):
        return(CurrentState)
    else:
        return(False)

#################################################################
# To assist in performing a sanity test, the following function #
# will return either the CurrentState or False based on the     #
# name of the configured service for Arduino supporting         #
# services.                                                     #
#################################################################
def TestArduinoControllerExists(ControllerName, CurrentState):
    if ((ControllerName == "arduinoNano" and EnableArduinoNano)):
        return(CurrentState)
    else:
        return(False)

#################################################################
#                                                               #
# The next level of controllers that can be used are attached   #
# to the I2C bus of either the Raspi4 or the Aurduinos.         #
#                                                               #
#################################################################
# Our servo controller's in Spot are the Adafruit 16 channel    #
# PWM Servo drivers also known as the PCA9685 PWM driver.       #
# With one or two of these installed we will need to create     #
# Two separate service, one for each.                           #
# Next we need to attach the servo drivers to the Raspi4 or the #
# ArduinoNano.                                                  #
# There are three parameters we need to set,                    #
#                                                               #
# The first parameter is the service we want to attach it to,   #
# normally either the RasPi or one of the Arduinos              #
# in our case it will be the Raspi4.                            #
#                                                               #
# The second parameter is the bus, This is normally 1 for the   #
# RasPi or 0 for an Arduino.                                    #
#                                                               #
# Each servo driver has a unique address that is hard coded by  #
# means of a set of jumpers on the controller boards, This is   #
# our Third parameter, There are seven jumpers that form a      #
# binary number that is added to 0x40. Note the 0x indicates    #
# the number is in hexadecimal format that is base 16 and has   #
# values in the range 0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F           #
# 0x40 is equal to 64 in decimal, the seven jumpers will give   #
# up to 128 possible address.                                   #
# Just be aware of any other I2C devices you have on the bus    #
# and what their address are, some device can not be changed    #
# or have a very limited number of selectable addresses.        #
#################################################################

#################################################################
# PCA9685 controler for the Back.                               #
#################################################################
EnableAdafruit16CServoDriverBack = TestI2CControllerExists(BackServoDriverAttached, EnableAdafruit16CServoDriverBack)
if EnableAdafruit16CServoDriverBack == True:
    print "--Starting the Adafruit16CServoDriver for the Back"
    Back = Runtime.createAndStart("Back", "Adafruit16CServoDriver")
    Back.attach(runtime.getService(BackServoDriverAttached), BackServoDriverPort, BackServoDriverAddr)

#################################################################
# PCA9685 controler for the Front.                              #
#################################################################
EnableAdafruit16CServoDriverFront = TestI2CControllerExists(FrontArmServoDriverAttached, EnableAdafruit16CServoDriverFront)
if EnableAdafruit16CServoDriverFront == True:
    print "--Starting the Adafruit16CServoDriver for the Right Arm"
    Front = Runtime.createAndStart("Front", "Adafruit16CServoDriver")
    Front.attach(runtime.getService(FrontArmServoDriverAttached), FrontArmServoDriverPort, FrontArmServoDriverAddr)

#################################################################
# To assist in performing a sanity test, the following function #
# will return either the CurrentState or False based on the     #
# name of the configured service for Servo supporting services. #
#################################################################
def TestServoControllerExists(ControllerName, CurrentState):
    if ((ControllerName == "Back" and EnableAdafruit16CServoDriverBack) 
        or (ControllerName == "Front" and EnableAdafruit16CServoDriverFront)
        or (ControllerName == "arduinoNano" and EnableArduinoNano)):
        return(CurrentState)
    else:
        return(False)


