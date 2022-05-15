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
# FootClass.py                                                  #
# This file is a group of commands that perform actions         #
#                                                               #
#################################################################
import math

class Foot():
    # The definition of a single foot
    # When creating pass in the foot type and the 3 servos for 
    # the leg.
    # Foot type: 
    #   0=Front Left, 
    #   1=Front Right, 
    #   2=Back Left, 
    #   3=Back Right
    def __init__(self, type=0, Shoulder, Arm, Wrist):
        self.type = type
        self.ServoS = Shoulder
        self.ServoA = Arm
        self.ServoW = Wrist
        # Servo limits
        self.ShoulderMin = self.ServoS.getMin()
        self.ShoulderRest = self.ServoS.getRest()
        self.ShoulderMax = self.ServoS.getMax()
        self.ArmMin = self.ServoA.getMin()
        self.ArmRest = self.ServoA.getRest()
        self.ArmMax = self.ServoA.getMax()
        self.WristMin = self.ServoW.getMin()
        self.WristRest = self.ServoW.getRest()
        self.WristMax = self.ServoW.getMax()
        # Servo current Angles
        self.Shoulder = self.ServoS.getCurrentInputPos()
        self.Arm = self.ServoA.getCurrentInputPos()
        self.Wrist = self.ServoW.getCurrentInputPos()
        # Servo angle offsets. I'm assuming a servo range of 0 - 180 degrees
        # the rotation of the servo can give us a better range, but will
        # upset the math, so we need to know the offset.
        self.ShoulderOffset = 0
        self.ArmOffset = -90
        self.WristOffset = 0
        # Length between the Wrist joint and the foot
        self.LWF = 124   
        # Length between the Arms joint and the Wrist joint
        self.LTW = 110   
        # Length between the Shoulder joint and the center line of the Arm
        self.LST = 55    
        # Length between the center Y plane and the shoulder joint
        self.LYS = 90    
        # Length between the center X plane and the shoulder joint
        self.LXS = 38
        self.MaxLTF = self.LTW + self.LWF
        # IMU data
        self.Pitch = 0
        self.Roll = 0
        # Centre of Mass offsets
        self.CoMxOffset = 0
        self.CoMyOffset = 0
        self.CoMzOffset = 0
        # Foot Positions, X, Y and Z
        self.x = 0
        self.y = 0
        self.z = 0
        self.updateFK()
        # IMU/COM based foot position.
        self.imuX = self.x
        self.imuY = self.y
        self.imuZ = self.z
        
    def setLWF(self, lwf=self.LWF):
        self.LWF = lwf
        self.MaxLTF = self.LTW + self.LWF
        
    def setLTW(self, ltw=self.LTW):
        self.LTW = ltw
        self.MaxLTF = self.LTW + self.LWF
        
    def setLST(self, lst=self.LST):
        self.LST = lst
        
    def setLYS(self, lys=self.LYS):
        self.LYS = lys
        
    def setLXS(self, lxs=self.LXS):
        self.LXS = lxs
    
    def setComOffsets(self, x, y, z):
        self.CoMxOffset = x
        self.CoMyOffset = y
        self.CoMzOffset = z
        
    def setServoPos(self, shoulder, arm, wrist):
        self.Shoulder = shoulder
        self.Arm = arm
        self.Wrist = wrist
        self.updateFK()
        
    def setIMUdata(self, pitch, roll):
        self.Pitch = pitch
        self.Roll = roll
        self.imuUpdateFK()
    
    # From time to time, the current servo position and the 
    # actual servo positions can get out of sysnc.
    # This routine updates the calsses data from the actual 
    # servo pos.
    def syncServoPosition(self):
        self.Shoulder = self.ServoS.getCurrentInputPos()
        self.Arm = self.ServoA.getCurrentInputPos()
        self.Wrist = self.ServoW.getCurrentInputPos()
        self.updateFK()
    
    # Using the servo positions passed in, this routine will 
    # calculate where the foot is relative to the Robot Plane 
    # of Reference.
    def forwardKinematics(self, shoulder, arm, wrist):
        LTF = math.sqrt(self.LWF*self.LWF + self.LTW*self.LTW - 2*self.LWF*self.LTW*math.cos(math.radians(self.wrist+self.WristOffset)))
        AFW = math.degrees(math.acos((LTF*LTF + self.LTW*self.LTW - self.LWF*self.LWF)/(2*LTF*self.LTW)))
        LTFa = math.cos(math.radians(AFW - arm + self.ArmOffset)) * LTF
        LSF = math.sqrt(self.LST*self.LST + LTFa*LTFa)
        if self.type == 0 or self.type == 2:
            X = (math.sin(math.acos(self.LST/LSF)+math.radians(shoulder + self.ShoulderOffset))*LSF)-self.LXS
        else:
            X = (math.sin(math.acos(self.LST/LSF)+math.radians(shoulder + self.ShoulderOffset))*LSF)+self.LXS
        if self.type == 0 or self.type == 1:
            Y = (LTF * math.sin(math.radians(arm - AFW + self.ArmOffset)))+self.LYS
        else:
            Y = (LTF * math.sin(math.radians(arm - AFW + self.ArmOffset)))-self.LYS
        Z = math.cos(math.acos(self.LST/LSF) + math.radians(shoulder + self.ShoulderOffset))*LSF
        return {"X":X, "Y":Y, "Z":Z}

    # This routine call the Forward Kinimatics routine passing 
    # the current servo positions then saves the foot coordinates.
    def updateFK(self):
        data = forwardKinematics(self, self.Shoulder, self.Arm, self.Wrist)
        self.x = data.get("X")
        self.y = data.get("Y")
        self.z = data.get("Z")
    
    # This is a simple conversion of the foot coordinates from 
    # the Robot Plane of Reference to the Inertial Center of 
    # Mass Plane of Reference based on the coordinates passed in.
    def imuForwardKinimatics(self, X, Y, Z):
        # Lets change our reference from the Robot origin to the 
        # Centre of Mass origin
        CoMX = X - self.CoMxOffset
        CoMY = Y - self.CoMyOffset
        CoMZ = Z - self.CoMzOffset
        # Next lets work out the distance between the Centre of 
        # Mass and the feet
        xzL = math.sqrt((CoMX*CoMX)+(CoMZ*CoMZ))
        yzL = math.sqrt((CoMY*CoMY)+(CoMZ*CoMZ))
        # We also need to know the angle of the line between the
        # Centre of Mass and the feet
        xzA = math.asin(CoMX/xzL)
        yzA = math.asin(CoMY/yzL)
        # Now simpley add the Roll and Pitch to the current angles
        imuXZA = xZA + self.Roll
        imuYZA = yZA + self.Pitch
        # Now we can calculate the new X, Y, and Z based on the 
        # new origin and angle.
        ImuX = math.sin(imuXZA)*xzL
        ImuY = math.sin(imuYZA)*yzL
        ImuZ = math.cos(imuYZA)*yzL
        retrun {"X":ImuX, "Y":ImuY, "Z":ImuZ}

    # This will make sure the current Inertial Centre of Mass 
    # Frame of Reference is up to date
    def imuUpdateFK(self):
        updateFK()
        IComPoR = self.imuForwardKinimatics(self.x, self.y, self.z)
        self.imuX = IComPoR.get("X")
        self.imuY = IComPoR.get("Y")
        self.imuZ = IComPoR.get("Z")
    
    # This is a request to work out where to set the servos 
    # in order to place the foot at the requested coordinates.
    # the preceding R in the coordinates is the Request.
    def inverseKinematics(self, RX, RY, RZ):
        error = 0
        if self.type == 0 or self.type == 2:
            legX = RX + self.LXS
        else:
            legX = RX - self.LXS
        if self.type == 0 or self.type == 1:
            legY = RY - self.LYS
        else:
            legY = RY + self.LYS
        legZ = RZ
        # Lets work out the Length Shoulder Foot (LSF)
        LSF = math.sqrt((legX*legX) + (legZ*legZ))
        # Now that we have Length Shoulder Foot and 
        # we know Length Shoulder Top, lets work out 
        # the Length Top Foot z
        # we use the z suffix here, because this only 
        # relative to the X-Z plane and not the XY plane
        LTFz = math.sqrt(LSF*LSF - self.LST*self.LST)
        Ai = math.asin(legX/LSF) # Angle inside
        Ao = math.acos(self.LST/LSF)  # Angle Outside
        shoulder = 180 - math.degrees(Ai + Ao)-self.ShoulderOffset
        # Now that we know what the shoulder servo angle 
        # should be, lets see it's within the servos 
        #range limit
        if shoulder < self.ShoulderMin:
            error = 1
            shoulder = self.ShoulderMin
        if shoulder > self.ShoulderMax:
            error = 2
            shoulder = self.ShoulderMax
        # Now we need to work out the Length Top of arm to the Foot
        LTF = math.sqrt((LTFz*LTFz) + (legY*legY))
        if (self.LTW + self.LWF) < LTF:
            # "Warning, LTF is longer than LTW and LWF combined, this is impossible"
            error = 7
            arm = 0
            wrist = 0
        else:
            # Now we can work out the wrist servo position.
            # Python work in Radians
            ServoWR = math.acos(((LTW*LTW) + (LWF*LWF) - (LTF*LTF))/(2*LTW*LWF))
            # Now that we have the servo position in radian we 
            # convert it to degrees
            wrist = math.degrees(ServoWR)
            if wrist < self.WristMin:
                error = 5
                wrist = self.WristMin
            if wrist > self.WristMax:
                error = 6
                wrist = self.WristMax
            # Now we can work out the for the are relative to the line to the foot
            Afw = math.asin((math.sin(math.radians(wrist))*LWF)/LTF)
            if legY>0:
                Af = math.acos(LTFz/LTF)
            else:
                Af = -math.acos(LTFz/LTF)
            # Then combine with the angle we need the foot at 
            # relative to the top of the arm to get the servo 
            # position
            arm = math.degrees(Afw - Af) - self.ArmOffset
            if arm < self.ArmMin:
                error = 3
                arm = self.ArmMin
            if arm > self.ArmMax:
                error = 4
                arm = self.ArmMax
        return {"Error":error, "Shoulder":shoulder, "Arm":arm, "Wrist":wrist}
        #LSFx, LAFy, Zt