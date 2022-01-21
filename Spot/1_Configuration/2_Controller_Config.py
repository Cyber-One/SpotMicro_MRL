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
# 2_Controller_Config.py                                        #
# This is where the configuration settings live for the         #
# varoius controllers.                                          #
#                                                               #
#################################################################
print "Creating the Controller Config"
#################################################################
#                                                               #
# Level 1 Controllers                                           #
#                                                               #
#################################################################
#                                                               #
# The Raspberry Pi 4 is a small Single Board Computer (SBC)     #
# with enough power to experiment and run a lot of MRL          #
# services, just not all at once. :-)                           #
# Built on to the Raspberry Pi are the                          #
# General Purpose Input Output (GPIO) pins.  Amonst these are   #
# and I2C bus, a TTL Serial, I2S Audio bus and other general    #
# purpose configurable Inputs and Outputs.                      #
# Note: The I2C bus is on Port 1. Pins 2 (SDA) and Pin 3 (SCL)  #
#       I2C Port 0 is used for the uSD card.                    #
#################################################################
## NOTE: the GPIO are 3.3V only, applying 5V to these pins     ##
## will destroy your Raspberry Pi SBC, You have been warned    ##
#################################################################
EnableRaspberryPi = True            # True for on, False for off

# In the Spot build, I'm using an Arduino Nano for the two      #
# Ultrasonic Sensors and the PIR sensor.                        #
# The Arduino also has an I2C Port 0 if we need to use it.      #
EnableArduinoNano = False           # True for on, False for off
ArduinoNanoComPort = "/dev/ttyAMA0" # Refer to notes above

#################################################################
#                                                               #
# Level 2 Controllers. I2C based devices                        #
#                                                               #
#################################################################
#                                                               #
# Our servo controllers in Spot are the Adafruit 16 channel     #
# PWM Servo drivers.  With two of these installed we will       #
# need to create two separate service, one for each.            #
# Next we need to attach the servo drivers to the Raspi4 or     #
# the Arduino                                                   #
# There are three parameters we need to set,                    #
#                                                               #
# The first parameter is the service we want to attach it to,   #
# normally either the RasPi or the "arduinoNano"                #
# in our case it will be the Raspi4. "raspi"                    #
#                                                               #
# The second parameter is the bus, This is normally 1 for the   #
# RasPi or 0 for an Arduino.                                    #
#                                                               #
# Each servo driver has a unique address that is hard coded     #
# by means of a set of jumpers on the controller boards, This   #
# is our Third parameter, There are seven jumpers that form     #
# a binary number that is added to 0x40. Note the 0x            #
# indicates the number is in hexadecimal format that is base    #
# 16 and has values in the range:                               #
# 0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F                               #
# 0x40 is equal to 64 in decimal, the seven jumpers will give   #
# up to 128 possible address.                                   #
# Just be aware of any other I2C devices you have on the bus    #
# and what their address are, some device can not be changed    #
# or have a very limited number of selectable addresses.        #
#                                                               #
#################################################################

EnableAdafruit16CServoDriverBack = True     # True or False
BackServoDriverAddr = "0x40"                # Refer to notes above
BackServoDriverBus = "1"                    # Refer to notes above
BackServoDriverAttached = "raspi"           # Refer to notes above

EnableAdafruit16CServoDriverFront = False   # True or False
FrontArmServoDriverAddr = "0x41"            # Refer to notes above
FrontArmServoDriverBus = "1"                # Refer to notes above
FrontArmServoDriverAttached = "raspi"       # Refer to notes above

