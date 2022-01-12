# SpotMicro_MRL
This dog looks similar to the Boston Dynamic four legged robot named spot.
This version was created by KDY0523 and named Spotmicro after the Boston Dynamics robot.

Already there have been other creators out there modifying the design to change or add features, so you know I will be looking at those as well.
In the original design, an ArduinoMega 2560 was used to run Spotmicro, however there are mods to allow the use of a Raspberry Pi, so this is the way I will be going :-)

Building the robot is not overly complex, but I have created a set of instructions:
https://github.com/Cyber-One/SpotMicro_MRL/blob/main/Docs/Spot_Micro_Hardware.md
as well as a series of videos:
https://youtube.com/playlist?list=PLgXTfFM40HqF6YqVjWtEtDC-ekbIkpkyE

The Parts list.md file contains a list of the different hardware I used as well as the locations and creators where I found these files and the files I used from those uploads.:
https://github.com/Cyber-One/SpotMicro_MRL/blob/main/Docs/Spot_Micro_Parts_List.md

The system will be running on My Robot Lab (MRL), available from http://myrobotlab.org/
I also have a set of instructions on setting up the Raspberry pi and installing My Robot Lab onto the Raspberry pi.:
https://github.com/Cyber-One/SpotMicro_MRL/blob/main/Docs/Spot_Micro_Operating_System.md


## Configuring Spot Micro 
If your not really interested in learning to program, and just want to run spot, you will need to setup the configurations.
In the Spot/1_Configuration folder, you will find a number of files.
Each of these files holds a different part of the system configuration.

### 1_Sys_Config.py 
holds all the system based configurations.
Here you will set the bots name and how the Web based Graphical User Interface works.
```
RobotsName = "Spot"

RunWebGUI = True
RunWebGUIbrowser = False
```

###2_Controller_Config.py
There are a number of controllers used in the SpotMicro build, starting with the Raspberry pi
If however you build your robot using something other than a Raspberry Pi, then you can disable the RasPi service in here.
```
EnableRaspberryPi = True

EnableArduinoNano = True
ArduinoNanoComPort = "/dev/ttyAMA0"

EnableAdafruit16CServoDriverBack = True
BackServoDriverAddr = "0x40"
BackServoDriverBus = "1"
BackServoDriverAttached = "raspi"

EnableAdafruit16CServoDriverFront = False
FrontArmServoDriverAddr = "0x41"
FrontArmServoDriverBus = "1"
FrontArmServoDriverAttached = "raspi"
```

###3_Servo_Config.py
There are 4 legs in SpotMicro, below is the configuration data for one of the legs, Front Left Leg.
The other 4 legs are similar but have a look in the config file as the orientation between the left and right sides will change.
```
EnableFLShoulder = True # True or False
FLShoulderAttachment = "Back"
FLShoulderPin = 12
FLShoulderMinPos = 0
FLShoulderMaxPos = 180
FLShoulderVelocity = 375

EnableFLArm = True
FLArmAttachment = "Back"
FLArmPin = 13
FLArmMinPos = 0
FLArmMaxPos = 180
FLArmVelocity = 375

EnableFLWrist = True
FLWristAttachment = "Back"
FLWristPin = 14
FLWristMinPos = 0
FLWristMaxPos = 180
FLWristVelocity = 375
```

###A_IO_Config.py

