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
    
    def __init__(self, type=0, x=0, y=0, z=0):
        # Foot type: 0=Front Left, 1=Front Right, 2=Back Left, 3=Back Right
        self.type = type
        # Foot Positions, X, Y and X
        self.x = x
        self.y = y
        self.z = z
        self.ShoulderMin = 50.0
        self.ShoulderRest = 90.0
        self.ShoulderMax = 130.0
        self.ArmMin = 15.0
        self.ArmRest = 120.0
        self.ArmMax = 165.0
        self.WristMin = 50.0
        self.WristRest = 125.0
        self.WristMax = 180.0
        # Servo current Angles
        self.Shoulder = self.ShoulderRest
        self.Arm = self.ArmRest
        self.Wrist = self.WristRest
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

    def updateFK(self):
        data = forwardKinematics(self, self.Shoulder, self.Arm, self.Wrist)
        self.x = data.get("X")
        self.y = data.get("Y")
        self.z = data.get("Z")
        
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
        # Now we can calculate the new X, Y, and Z based on the new 
        # origin and angle.
        ImuX = math.sin(imuXZA)*xzL
        ImuY = math.sin(imuYZA)*yzL
        ImuZ = math.cos(imuYZA)*yzL
        retrun {"X":ImuX, "Y":ImuY, "Z":ImuZ}

    def imuUpdateFK(self):
        data = self.imuForwardKinimatics(self.x, self.y, self.z)
        self.imuX = data.get("X")
        self.imuY = data.get("Y")
        self.imuZ = data.get("Z")
    
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
        soulder = 180 - math.degrees(Ai + Ao)-self.ShoulderOffset
        # Now that we know what the shoulder servo angle 
        # should be, lets see it's within the servos 
        #range limit
        if soulder < self.ShoulderMin:
            error = 1
            soulder = self.ShoulderMin
        if soulder > self.ShoulderMax:
            error = 2
            soulder = self.ShoulderMax
        LTF = math.sqrt((LTFz*LTFz) + (legY*legY))
        if (self.LTW + self.LWF) < LTF:
            # "Warning, LTF is longer than LTW and LWF combined, this is impossible"
            error = 7
            arm = 0
            wrist = 0
        else:
            ServoWR = math.acos(((LTW*LTW) + (LWF*LWF) - (LTF*LTF))/(2*LTW*LWF))
            wrist = math.degrees(ServoWR)
            if wrist < self.WristMin:
                error = 5
                wrist = self.WristMin
            if wrist > self.WristMax:
                error = 6
                wrist = self.WristMax
            Afw = math.asin((math.sin(math.radians(wrist))*LWF)/LTF)
            if LAFy>0:
                Af = math.acos(LTFz/LTF)
            else:
                Af = -math.acos(LTFz/LTF)
            arm = math.degrees(Afw - Af) - self.ArmOffset
            if arm < self.ArmMin:
                error = 3
                arm = self.ArmMin
            if arm > self.ArmMax:
                error = 4
                arm = self.ArmMax
        return {"Error":error, "Shoulder":soulder, "Arm":arm, "Wrist":wrist}
        #LSFx, LAFy, Zt