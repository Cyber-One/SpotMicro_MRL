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
# A_IO_Config.py                                                #
# This is where the configuration settings live for the         #
# varoius devices that don't fit in the other catagories.       #
#                                                               #
#################################################################
print "Creating the Input/Output Config"

#################################################################
#                                                               #
# The Ultra-Sonic Range Sensors                                 #
#                                                               #
#################################################################
# Ultrasonic sensors emit a pulse of high frequency sound       #
# normally 8 cycles at a frequency the we can not hear.         #
# They then wait for the reflected sound to be detected.        #
# The time taken for the sound pulse to travel to an object and #
# be reflected back can be timed and give a reasonable          #
# indication of the distance the object is away from the sensor.#
# The speed of sound in air is about 343 metres per second      #
# or 1,235 km/h; 1,125 ft/s; 767 mph.                           #
# The speed of sound however will vary with temperature.        #
# Speed = 331.3 + (0.606 * airTemp) m/s                         #
# Our robot use a Ultrasonic module to do the above, but we     #
# need to handle the time measurement.                          #
# MRL offloads this to the Arduino, It starts the pulse         #
# transmission using the transmit pin, the times how long it    #
# takes for the receive pin to be pulsed high.                  #
# From there it can do the math to get a distance.              #
# Pin 1 is used for the Transmit of the pulse.        Trigger   #
# Pin 2 is used for the receive of the return pulse.  Echo      #
EnableLeftUltrasonic = True
LeftUltrasonicAttachment = "arduinoNano"
LeftUltrasonicPin1 = 3
LeftUltrasonicPin2 = 4

EnableRightUltraSonic = True
RightUltrasonicAttachment = "arduinoNano"
RightUltrasonicPin1 = 5
RightUltrasonicPin2 = 6

# Time between Pings in milli-seconds.
PingTime = 1000

#################################################################
#                                                               #
# The Battery Voltage Monitor                                   #
#                                                               #
#################################################################
# Battery Voltage can be a very important thing to monitor      #
# when your robot is running on batteries.  For the most        #
# part this is done with a simple resistor divider network.     #
# For this to work, an analog pin needs to be allocated         #
# from one of the installed Arduino's.  A resistor divider      #
# network, two resistors connected in series is connected       #
# between the ground and the battery power.  The junction       #
# of the two resistors is then connected to teh Arduino's       #
# analoginput.                                                  #
# The resistors are selected so that at no time would the       #
# voltage at the Arduino exceed 5 volts.                        #
# For Spots build, he's using 7.4Vdc batteries, so if we        #
# use a 10K resistor between gnd and the input and a 56K        #
# resistor between the input and the battery, we should be      #
# safe up to 33Vdc                                              #
# To enable, the Enable Battery monitor must be set to a        #
# value between 1 and 2, with each of the inputs defined`       #
# below.                                                        #
#################################################################
EnableBatteryMonitor = 2
BatteryMonitorAttachment = "arduinoNano"
BatteryMonitorPin1 = "A0" # On the Arduino Nano, this = A0
BatteryMonitorPin2 = "A1" # On the Arduino Nano, this = A1
BatteryMonitorPollInterval = 10000 # milli-seconds

#################################################################
#                                                               #
# MPU6050 Inertial Measurment Unit (IMU)                        #
#                                                               #
#################################################################
# It would be good to know when the body was level.             #
# This can achived by installing an Inertial Measurment         #
# Unit (IMU).  The IMU we can use here is the MPU6050,          #
# a reasonably cheap I2C device that provides acelleration      #
# in 3 axis of the linear direction as well as 3 axis of        #
# rotational motion.                                            #
#################################################################
EnableMPU6050A = True                   # True or False
MPU6050AAttached = "raspi"
MPU6050ABus = "1"
MPU6050AAddr = "0x68"
MPU6050AgyroXOffset = 2
MPU6050AgyroYOffset = 0
MPU6050AgyroZOffset = 0

EnableMPU6050B = False                   # True or False
MPU6050BAttached = "raspi"
MPU6050BBus = "1"
MPU6050BAddr = "0x69"
MPU6050BgyroXOffset = 0
MPU6050BgyroYOffset = 0
MPU6050BgyroZOffset = 0


#################################################################
#                                                               #
# HD44780 2 line 16 Character I2C LCD Display                   #
#                                                               #
#################################################################
# The HD44780 LCD driver is able to drive up to 40 characters   #
# over 2 lines, There are some displays, that will split at the #
# 20th character to create a 4 line 20 character display        #
# The LCD dispaly is not inherintly an I2C device, so we use a  #
# PCF8574 8 channel I/O Expander to provide the signals we need #
# to driver the LCD display.                                    #
#################################################################
EnableLCD = True
LCDAttached = "raspi"
LCDBus = "1"
LCDAddr = "0x27"
LCDStartMessage1 = "Cyber_One  Spot "
LCDStartMessage2 = "MyRobotLab Micro"

#################################################################
#                                                               #
# Ibus Remote Control Service                                   #
#                                                               #
#################################################################
# Not yet available
EnableIBus = False
IbusAttach = "arduinoLeft"
IbuSerial = "Serial1"

