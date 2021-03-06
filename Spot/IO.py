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
# IO.py                                                         #
# This file handels the various Sensors and outputs             #
# not already covered in other modules                          #
#                                                               #
#################################################################
print "Creating the various IO Services"
# Load the configuration for the IO devices.
execfile(RuningFolder+'/1_Configuration/A_IO_Config.py')

#################################################################
#                                                               #
# The Ultrasonic services                                       #
#                                                               #
#################################################################
# the Ultrasonic services has a couple of option on how you     #
# can use it. In anycase the max range from a software          #
# perspective is 5 meters.                                      #
# 1) ping()         This returns the time of flight in          #
#                   milli-seconds each time you call it.        #
#                   This is a On-Demand method.                 #
# 2) range()        This gives you the distance in              #
#                   centimeters each time you call it.          #
#                   This is a On-Demand method.                 #
# 3) startRanging() The start and stop ranging methods          #
#    stopRanging()  produce a series of pulses with the         #
#                   results returning on the callback           #
#                   method, the default being onRange.          #
#                   This is normally setup using                #
#                   UltraSonic.addRangeListener(python)         #
#                   But we will use the subscribe method        #
#                   from the python service so we can           #
#                   seperate the two sensors returns.           #
#################################################################

EnableLeftUltrasonic = TestArduinoControllerExists(LeftUltrasonicAttachment, EnableLeftUltrasonic)
if EnableLeftUltrasonic:
    arduinoNano.pinMode(2, Arduino.OUTPUT)
    arduinoNano.digitalWrite(2,1)
    LeftUltraSonic = Runtime.start("LeftUltraSonic", "UltrasonicSensor")
    LeftUltraSonic.setTriggerPin(LeftUltrasonicPin1)
    LeftUltraSonic.setEchoPin(LeftUltrasonicPin2)
    LeftUltraSonic.attach(runtime.getService(LeftUltrasonicAttachment))
    #python.subscribe('LeftUltraSonic', 'onRange', 'python', 'onRangeLeft')

EnableRightUltraSonic = TestArduinoControllerExists(RightUltrasonicAttachment, EnableRightUltraSonic)
if EnableRightUltraSonic:
    arduinoNano.pinMode(2, Arduino.OUTPUT)
    arduinoNano.digitalWrite(2,1)
    RightUltraSonic = Runtime.start("RightUltraSonic", "UltrasonicSensor")
    RightUltraSonic.setTriggerPin(RightUltrasonicPin1)
    RightUltraSonic.setEchoPin(RightUltrasonicPin2)
    RightUltraSonic.attach(runtime.getService(RightUltrasonicAttachment))
    #python.subscribe('RightUltraSonic', 'onRange', 'python', 'onRangeRight')

#################################################################
#                                                               #
# The Battery Voltage Monitor                                   #
#                                                               #
#################################################################
BatteryLevel = [0, 0]
EnableBatteryMonitor = TestArduinoControllerExists(BatteryMonitorAttachment, EnableBatteryMonitor)
if EnableBatteryMonitor > 0 and EnableBatteryMonitor < 5:
    # Lets set a default value for the Battery Monitor value
    # Once the first poll sequence is complete, this will be more accurate
    BatteryLevel[0] = 1
    if EnableBatteryMonitor > 1:
        BatteryLevel[1] = 1
    def BattMonPublishedPins(pins):
        if pins != None:
            for pin in range(0, len(pins)):
                if pins[pin].pin == BatteryMonitorPin1:
                    BatteryLevel[0] = pins[pin].value
                elif pins[pin].pin == BatteryMonitorPin2:
                    BatteryLevel[1] = pins[pin].value
    # Because we are dealing with the controller itself, we 
    # need to reference the controller directly.
    # That means creating the control program for each of 
    # the variations that may be used in the config. 
    if BatteryMonitorAttachment == "arduinoNano":
        arduinoNano.setBoardNano() 
        arduinoNano.setAref("DEFAULT")
        arduinoNano.addListener("publishPinArray","python","BattMonPublishedPins")
        arduinoNano.enablePin(BatteryMonitorPin1, 1)
        if EnableBatteryMonitor > 1:
            arduinoNano.enablePin(BatteryMonitorPin2, 1)

#################################################################
#                                                               #
# MPU6050 Inertial Measurment Unit (IMU)                        #
#                                                               #
#################################################################
# The first parameter is the service we want to attach it to,   #
# normally either the RasPi or one of the Arduinos              #
# in our case it will be the Raspi4.                            #
#                                                               #
# The second parameter is the bus, This is normally 1 for the   #
# RasPi or 0 for an Arduino.                                    #
#################################################################
EnableMPU6050A = TestI2CControllerExists(MPU6050AAttached, EnableMPU6050A)
if EnableMPU6050A == True:
    MPU6050A = Runtime.start("MPU6050A","Mpu6050")
    MPU6050A.setBus(MPU6050ABus)
    MPU6050A.setAddress(MPU6050AAddr)
    MPU6050A.attach(runtime.getService(MPU6050AAttached))
    #MPU6050A.attach(runtime.getService(MPU6050AAttached), MPU6050ABus, MPU6050AAddr)
    #MPU6050A.initialize()
    MPU6050A.dmpInitialize()
    MPU6050A.start()
    PlatformStructure = runtime.getPlatform()
    if PlatformStructure.getVersion() > "1.1.810":
        sleep(1)
        MPU6050A.setXGyroOffset(MPU6050AgyroXOffset)
        MPU6050A.setYGyroOffset(MPU6050AgyroYOffset)
        MPU6050A.setZGyroOffset(MPU6050AgyroZOffset)
    #MPU6050A.refresh()
    #MPU6050A.getRaw() 
    #MPU6050A.startOrientationTracking()
    #MPU6050A.stopOrientationTracking()
    #python.subscribe('MPU6050A', 'publishOrientation', 'python', 'MPU6050Head')
    #publishOrientation(Orientation data) 

EnableMPU6050B = TestI2CControllerExists(MPU6050BAttached, EnableMPU6050B)
if EnableMPU6050B == True:
    MPU6050B = Runtime.start("MPU6050B","Mpu6050")
    MPU6050B.setBus(MPU6050BBus)
    MPU6050B.setAddress(MPU6050BAddr)
    MPU6050B.attach(runtime.getService(MPU6050BAttached))
    #MPU6050B.attach(runtime.getService(MPU6050BAttached), MPU6050BBus, MPU6050BAddr)
    #MPU6050B.initialize()
    MPU6050B.dmpInitialize()
    MPU6050B.setXGyroOffset(MPU6050BgyroXOffset)
    MPU6050B.setYGyroOffset(MPU6050BgyroYOffset)
    MPU6050B.setZGyroOffset(MPU6050BgyroZOffset)
    MPU6050B.start()
    #MPU6050B.refresh()
    #MPU6050B.getRaw() 
    #MPU6050B.startOrientationTracking()
    #MPU6050B.stopOrientationTracking()
    #python.subscribe('MPU6050B', 'publishOrientation', 'python', 'MPU6050Body')
    #publishOrientation(Orientation data) 

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
EnableLCD = TestI2CControllerExists(LCDAttached, EnableLCD)
if EnableLCD == True:
    LCDPCF8574 = Runtime.start("LCDPCF8574","Pcf8574")
    LCDPCF8574.setBus(LCDBus)
    LCDPCF8574.setAddress(LCDAddr)
    LCDPCF8574.attach(runtime.getService(LCDAttached))
    #LCDPCF8574.attach(runtime.getService(LCDAttached), LCDBus, LCDAddr)
    LCD = Runtime.start("LCD","Hd44780")
    LCD.attach(LCDPCF8574)
    LCD.clear()
    LCD.display(LCDStartMessage1, 0)
    LCD.display(LCDStartMessage2, 1)
    LCD.setBackLight(True)


#################################################################
#                                                               #
# Ibus Remote Control Service                                   #
#                                                               #
#################################################################
# Not yet available :-(
if EnableIBus:
    IBus = Runtime.start("IBus","IBus")
    IBus.attach(IbuSerial)
#All Methods Static Methods Instance Methods Concrete Methods 
#Modifier and Type  Method  Description
#void               attach(SerialDevice serial) 
#static void        main(String[] args) 
#void               onBytes(byte[] bytes) 
#void               onConnect(String portName) 
#void               onDisconnect(String portName) 
#int[]              publishChanel(int[] channel) 
#int                readChannel(int channelNr)
