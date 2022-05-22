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
print("creating the Foot and Feet classes")

# The Foot class contains a number of routines required to
# manage the location of a single foot.
# This include links to the Servos for that foot and calculating
# the position based on forward kinematics and also working out
# the required servo positions for a requested set of X, Y, Z
# coordinates in eaither the Robot Plane of Reference or the
# Inertial Centre of Mass Plane of Reference.
class Foot():
    # The definition of a single foot
    # When creating pass in the foot type and the 3 servos for 
    # the leg.
    # Foot type: 
    #   0=Front Left, 
    #   1=Front Right, 
    #   2=Back Left, 
    #   3=Back Right
    def __init__(self, type=0):
        self.type = type
        # Servo limits
        self.ShoulderMin = 50.0
        self.ShoulderRest = 90.0
        self.ShoulderMax = 130.0
        self.ArmMin = 15.0
        self.ArmRest = 138.0
        self.ArmMax = 165.0
        self.WristMin = 50.0
        self.WristRest = 50.0
        self.WristMax = 180.0
        # Servo current Angles
        self.Shoulder = self.ShoulderRest
        self.Arm = self.ArmRest
        self.Wrist = self.WristRest
        # Servo angle offsets. I'm assuming a servo range of 0 - 180 degrees
        # the rotation of the servo can give us a better range, but will
        # upset the math, so we need to know the offset.
        self.ShoulderOffset = 0
        self.ArmOffset = 90
        self.WristOffset = 0
        # Length between the Wrist joint and the foot
        self.LWF = 124
        self.LWF2 = self.LWF * self.LWF
        # Length between the Arms joint and the Wrist joint
        self.LTW = 110
        self.LTW2 = self.LTW * self.LTW
        self.LTWxLWFx2 = 2 * self.LTW * self.LWF
        # Length between the Shoulder joint and the center line of the Arm
        self.LST = 55 
        self.LST2 = self.LST * self.LST
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
        self.x = 1
        self.y = 1
        self.z = 1
        #self.updateFK()
        # IMU/COM based foot position.
        self.imuX = self.x
        self.imuY = self.y
        self.imuZ = self.z
        
    def setServos(self, Shoulder, Arm, Wrist):        
        self.ServoS = Shoulder
        self.ServoA = Arm
        self.ServoW = Wrist
        self.ShoulderMin = self.ServoS.getMin()
        self.ShoulderRest = self.ServoS.getRest()
        self.ShoulderMax = self.ServoS.getMax()
        self.ArmMin = self.ServoA.getMin()
        self.ArmRest = self.ServoA.getRest()
        self.ArmMax = self.ServoA.getMax()
        self.WristMin = self.ServoW.getMin()
        self.WristRest = self.ServoW.getRest()
        self.WristMax = self.ServoW.getMax()
        self.syncServoPosition()

    def setLWF(self, lwf):
        self.LWF = lwf
        self.LWF2 = self.LWF * self.LWF
        self.LTWxLWFx2 = 2 * self.LTW * self.LWF
        self.MaxLTF = self.LTW + self.LWF
        
    def setLTW(self, ltw):
        self.LTW = ltw
        self.LTW2 = self.LTW * self.LTW
        self.LTWxLWFx2 = 2 * self.LTW * self.LWF
        self.MaxLTF = self.LTW + self.LWF
        
    def setLST(self, lst):
        self.LST = lst
        self.LST2 = self.LST * self.LST
        
    def setLYS(self, lys):
        self.LYS = lys
        
    def setLXS(self, lxs):
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
        self.imuUpdateFK()
    
    # Using the servo positions passed in, this routine will 
    # calculate where the foot is relative to the Robot Plane 
    # of Reference.
    def forwardKinematics(self, shoulder, arm, wrist):
        LTF = math.sqrt(self.LWF*self.LWF + self.LTW*self.LTW - 2*self.LWF*self.LTW*math.cos(math.radians(wrist+self.WristOffset)))
        AFW = math.degrees(math.acos((LTF*LTF + self.LTW*self.LTW - self.LWF*self.LWF)/(2*LTF*self.LTW)))
        LTFa = math.cos(math.radians(AFW - arm + self.ArmOffset)) * LTF
        LSF = math.sqrt(self.LST*self.LST + LTFa*LTFa)
        workX = (math.sin(math.acos(self.LST/LSF)+math.radians(shoulder + self.ShoulderOffset))*LSF)
        if self.type == 0 or self.type == 2:
            X = -workX - self.LXS
        else:
            X = workX + self.LXS
        workY = (LTF * math.sin(math.radians(arm - AFW + self.ArmOffset)))
        if self.type == 0 or self.type == 1:
            Y = workY + self.LYS
        else:
            Y = workY - self.LYS
        Z = math.cos(math.acos(self.LST/LSF) + math.radians(shoulder + self.ShoulderOffset))*LSF
        # Only need the X, Y and Z, there rest is for debugging :-)
        return {"X":X, "Y":Y, "Z":Z, "Shoulder":shoulder, "Arm":arm, "Wrist":wrist, "LTF":LTF, "AFW":AFW, "LTFa":LTFa, "LSF":LSF, "WorkY":workY, "WorkX":workX}

    # This routine call the Forward Kinimatics routine passing 
    # the current remembered servo positions then saves the 
    # foot coordinates.
    def updateFK(self):
        data = self.forwardKinematics(self.Shoulder, self.Arm, self.Wrist)
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
        imuXZA = xzA + self.Roll
        imuYZA = yzA + self.Pitch
        # Now we can calculate the new X, Y, and Z based on the 
        # new origin and angle.
        ImuX = math.sin(imuXZA)*xzL
        ImuY = math.sin(imuYZA)*yzL
        ImuZ = -math.cos(imuYZA)*yzL
        #print("ImuX:", ImuX, "ImuY:", ImuY, "ImuZ:", ImuZ, "imuXZA:", imuXZA, "imuYZA:", imuYZA, "xzA:", xzA, "yzA:", yzA, "xzL:", xzL, "yzL:", yzL)
        return {"X":ImuX, "Y":ImuY, "Z":ImuZ}

    # This will make sure the current Inertial Centre of Mass 
    # Frame of Reference is up to date
    def imuUpdateFK(self):
        self.updateFK()
        IComPoR = self.imuForwardKinimatics(self.x, self.y, self.z)
        self.imuX = IComPoR.get("X")
        self.imuY = IComPoR.get("Y")
        self.imuZ = IComPoR.get("Z")
    
    # This is a request to work out where to set the servos 
    # in order to place the foot at the requested coordinates.
    # The preceding R in the coordinates is the Request.
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
        LSF = math.sqrt((legX * legX) + (legZ * legZ))
        # Now that we have Length Shoulder Foot and 
        # we know Length Shoulder Top, lets work out 
        # the Length Top Foot z
        # we use the z suffix here, because this only 
        # relative to the X-Z plane and not the XY plane
        print(self.type, LSF, self.LST, self.LST2, legX, legY, legZ)
        sleep(0.1)
        LTFz = math.sqrt((LSF * LSF) - self.LST2)
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
            wrist = self.WristMax
        else:
            # Now we can work out the wrist servo position.
            # Python work in Radians
            WristCosC = (self.LTW2 + self.LWF2 - (LTF * LTF)) / self.LTWxLWFx2
            print("IK ServoWrist cosC:", WristCosC)
            if WristCosC > 1.0:
                WristCosC = 1.0
            ServoWR = math.acos(WristCosC)
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
            Afw = math.asin((math.sin(math.radians(wrist))*self.LWF)/LTF)
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
        
    # The preceding R in the coordinates is the Request.
    def imuIK(self, RX, RY, RZ):
        # For this one it is the reverse process to the 
        # imuForwardKinimatics translation.
        # Lets first work out the distance from the foot 
        # to the ICoMPoR
        xzL = math.sqrt((RX*RX)+(RZ*RZ))
        yzL = math.sqrt((RY*RY)+(RZ*RZ))
        # Now that we have the length, lets work out the angles
        xzA = math.asin(RZ/xzL)
        yzA = math.asin(RZ/yzL)
        # using the angle, lets subtract off that the Pitch and Roll
        CoMxA = xzA - self.Roll
        CoMyA = yzA - self.Pitch
        # With the new angle and the line lengths, we can work 
        # out the XYZ coordinates of the relative to the CoM
        CoMx = math.sin(CoMxA)*xzL
        CoMy = math.sin(CoMyA)*yzL
        CoMz = math.cos(CoMyA)*yzL
        # So now that it is orientated correctly, lets adjust the offset
        RPoRx = CoMx + self.CoMxOffset
        RPoRy = CoMy + self.CoMyOffset
        RPoRz = -CoMz + self.CoMzOffset
        return {"X":RPoRx, "Y":RPoRy, "Z":RPoRz}

    # The RX, RY and RZ are the requested coordinated relative
    # to the Robot Plane of Reference.
    # This also stores in the class the last set of positions 
    # we requested the servos move to.
    def moveToRPoR(self, RX, RY, RZ):
        servos = self.inverseKinematics(RX, RY, RZ)
        if servos.get("Error") == 0:
            self.Shoulder = servos.get("Shoulder")
            self.Arm = servos.get("Arm")
            self.Wrist = servos.get("Wrist")
            self.ServoS.moveTo(self.Shoulder)
            self.ServoA.moveTo(self.Arm)
            self.ServoW.moveTo(self.Wrist)
            return {"Error":servos.get("Error"), "Shoulder":self.Shoulder, "Arm":self.Arm, "Wrist":self.Wrist}
        else:
            return {"Error":servos.get("Error"), "Shoulder":self.Shoulder, "Arm":self.Arm, "Wrist":self.Wrist}
    
    def rotateAboutCoM(self, pitch, roll):
        # self.imuX = self.x
        # self.imuY = self.y
        # self.imuZ = self.z
        xzL = math.sqrt((self.imuX*self.imuX)+(self.imuZ*self.imuZ))
        yzL = math.sqrt((self.imuY*self.imuY)+(self.imuZ*self.imuZ))
        xzA = math.asin(self.imuX/xzL) + pitch
        yzA = math.asin(self.imuY/yzL) + roll
        CoMx = math.sin(xzA)*xzL
        CoMy = math.sin(yzA)*yzL
        CoMz = -math.cos(yzA)*yzL
        return {"X":CoMx, "Y":CoMy, "Z":CoMz}

    
    # The RX, RY and RZ are the requested coordinated relative 
    # to the Inertial Center of Mass Plane of Reference.
    # This also stores in the class the last set of positions 
    # we requested the servos move to.
    def moveToICoMPoR(self, RX, RY, RZ):
        RPoR = self.imuIK(RX, RY, RZ)
        #print("moveToICoMPoR:", RPoR)
        servos = self.inverseKinematics(RPoR.get("X"), RPoR.get("Y"), RPoR.get("Z"))
        if servos.get("Error") == 0:
            self.Shoulder = servos.get("Shoulder")
            self.Arm = servos.get("Arm")
            self.Wrist = servos.get("Wrist")
            self.ServoS.moveTo(self.Shoulder)
            self.ServoA.moveTo(self.Arm)
            self.ServoW.moveTo(self.Wrist)
            return {"Error":servos.get("Error"), "Shoulder":self.Shoulder, "Arm":self.Arm, "Wrist":self.Wrist}
        else:
            return {"Error":servos.get("Error"), "Shoulder":self.Shoulder, "Arm":self.Arm, "Wrist":self.Wrist}
    
    #def moveToLevel(self):
        
    
# The Feet class creates 4 Foot objects based on the Foot class.
# It also provide a number of common update interfaces such as
# update the roll and pitch of the robot.
# It also has a number of unified movement functions that
# combine all 4 feet to assist with ballance and other
# coordinated movements.
class Feet():
    def __init__(self):
        self.FL = Foot(0)
        self.FR = Foot(1)
        self.BL = Foot(2)
        self.BR = Foot(3)
        self.Pitch = 0
        self.Roll = 0
        self.targetPitch = 0
        self.targetRoll = 0
        self.autoLevel = 0
    
    # enable or disable the auto level feature.
    def setAutoLevel(self, state):
        if state == 0:
            self.autoLevel = 0
        elif state == 1:
            self.autoLevel = 1
    
    def enableAutoLevel(self):
        self.autoLevel = 1
        self.levelRobot()
    
    def disableAutoLevel(self):
        self.autoLevel = 0
    
    
    def setLevel(self, pitch, roll):
        self.targetPitch = pitch
        self.targetRoll = roll
    
    def syncServos(self):
        self.FL.syncServoPosition()
        self.FR.syncServoPosition()
        self.BL.syncServoPosition()
        self.BR.syncServoPosition()

    # This routine updates the Pitch and Roll of each of the sub classes
    def updateIMU(self, pitch, roll):
        #print("UpdateIMU")
        if self.Pitch <> pitch or self.Roll <> roll:
            self.Pitch = pitch
            self.Roll = roll
            self.FL.setIMUdata(self.Pitch, self.Roll)
            self.FR.setIMUdata(self.Pitch, self.Roll)
            self.BL.setIMUdata(self.Pitch, self.Roll)
            self.BR.setIMUdata(self.Pitch, self.Roll)
            if self.autoLevel == 1:
                self.levelRobot()


    def levelRobot(self):
        print("Level Robot - Pitch:", self.Pitch, "Roll:", self.Roll)
        FLdata = self.FL.rotateAboutCoM(self.targetPitch-self.Pitch, self.targetRoll-self.Roll)
        print("FL", FLdata)
        FRdata = self.FR.rotateAboutCoM(self.targetPitch-self.Pitch, self.targetRoll-self.Roll)
        print("FR", FRdata)
        BLdata = self.BL.rotateAboutCoM(self.targetPitch-self.Pitch, self.targetRoll-self.Roll)
        print("BL", BLdata)
        BRdata = self.BR.rotateAboutCoM(self.targetPitch-self.Pitch, self.targetRoll-self.Roll)
        print("BR", BRdata)
        print("FL", self.FL.moveToICoMPoR(FLdata.get("X"), FLdata.get("Y"), FLdata.get("Z")))
        print("FR", self.FR.moveToICoMPoR(FRdata.get("X"), FRdata.get("Y"), FRdata.get("Z")))
        print("BL", self.BL.moveToICoMPoR(BLdata.get("X"), BLdata.get("Y"), BLdata.get("Z")))
        print("BR", self.BR.moveToICoMPoR(BRdata.get("X"), BRdata.get("Y"), BRdata.get("Z")))
        