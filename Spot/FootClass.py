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

# The Coordinates class is a data holder for different X, Y and 
# Z coordinates and Inertial Measuerment Unit (IMU) Pitch and 
# Roll values.
class Coordinates():
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.roll = 0
        self.pitch = 0

class Servos():
    def __init__(self, ServoObject):
        self.Servo = ServoObject
        self.updateServo()
        self.offset = 0
        self.pos = self.rest
           
    def setOffset(self, Offset):
        self.offset = Offset

    def updateServo(self):
        self.min = self.Servo.getMin()
        self.rest = self.Servo.getRest()
        self.max = self.Servo.getMax()
        self.syncServo()
        
    def syncServo(self):
        self.pos = self.Servo.getTargetPos()

    def setServoPos(self, Pos):
        if Pos > self.max:
            self.Servo.moveTo(self.max)  
            self.pos = self.max        
        elif Pos < self.min:
            self.Servo.moveTo(self.min)  
            self.pos = self.min 
        else:
            self.Servo.moveTo(Pos)  
            self.pos = Pos 
            
    
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
    def __init__(self, type, ShoulderServo, ArmServo, WristServo):
        self.type = type
        # Create the Servo entries
        self.shoulder = Servos(ShoulderServo)
        self.arm = Servos(ArmServo)
        self.wrist = Servos(WristServo)
        #self.Wrist = self.WristRest
        # Servo angle offsets. I'm assuming a servo range of 
        # 0 - 180 degrees the rotation of the servo body can 
        # give us a better usable range, but will upset the math, 
        # so we need to know the offset.
        self.shoulder.setOffset(0)
        self.arm.setOffset(90)
        self.wrist.setOffset(0)
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
        # to help speed up the class, we will use some 
        # pre-calculated values
        self.calulateStaticValues()
        # Centre of Mass offsets
        self.CoMxOffset = 0
        self.CoMyOffset = 0
        self.CoMzOffset = 0
        # Foot Positions, X, Y and Z in the Robot Plane of 
        # Reference (RPoR)
        self.RPoR = Coordinates()
        # Foot Positions, X, Y and Z in the Inertial Center 
        # of Mass Plane of Reference (ICoMPoR) the IMU will 
        # feed it's pitch and roll data to here.
        self.ICoMPoR = Coordinates()
        # Now we have the required info set, lets update the 
        # RPoR and ICoMPoR values.
        self.imuUpdateFK()
        
    def __repr__(self):
        return "Foot Class"
        
    def __str__(self):
        if self.type == 0:
            print_str = "Front Left Foot Class Status"
        elif self.type == 1:
            print_str = "Front Right Foot Class Status"
        elif self.type == 2:
            print_str = "Back Left Foot Class Status"
        else:
            print_str = "Back Right Foot Class Status"
        print ("  Servos - Shoulder: %.2f Arm: %.2f Wrist: %.2f" % (self.shoulder.pos, self.arm.pos, self.wrist.pos))
        print ("  RPoR - X:%.2f, Y:%.2f, Z:%.2f" % (self.RPoR.X, self.RPoR.Y, self.RPoR.Z))
        print ("  IComPoR - X:%.2f, Y:%.2f, Z:%.2f" % (self.ICoMPoR.X, self.ICoMPoR.Y, self.ICoMPoR.Z))
        return print_str

    # Some maths operation can be slow, so if we don't need to 
    # use math operations, we can speed up the program speed.
    # While we need math to work out these values, the values
    # rearly change, so we only need to calculate them when 
    # they do change.
    def calulateStaticValues(self):
        self.LWF2 = self.LWF * self.LWF
        self.LTW2 = self.LTW * self.LTW
        self.LTWxLWFx2 = 2 * self.LTW * self.LWF
        self.LST2 = self.LST * self.LST
        self.MaxLTF = self.LTW + self.LWF
        self.MinLTF = math.sqrt(self.LWF2 + self.LTW2 - (self.LTWxLWFx2 * math.cos(math.radians(self.wrist.min))))
    
    def setLWF(self, lwf):
        self.LWF = lwf
        self.calulateStaticValues()
        
    def setLTW(self, ltw):
        self.LTW = ltw
        self.calulateStaticValues()
        
    def setLST(self, lst):
        self.LST = lst
        self.calulateStaticValues()
        
    def setLYS(self, lys):
        self.LYS = lys
        
    def setLXS(self, lxs):
        self.LXS = lxs
    
    def setComOffsets(self, x, y, z):
        self.CoMxOffset = x
        self.CoMyOffset = y
        self.CoMzOffset = z
        self.imuUpdateFK()
        
    # The data coming back from the Inertial Measurement Unit
    # should be used to update this function.
    #This will trigger the current feet position in the Inertial 
    # Centre of Mass Plane of Reference to be updated as well.
    def setIMUdata(self, pitch, roll):
        self.ICoMPoR.pitch = pitch
        self.ICoMPoR.roll = roll
        self.imuUpdateFK()

    # From time to time, the current servo position and the 
    # actual servo positions can get out of sysnc, if something 
    # from outside this class commands the servo to move.
    # This routine updates the calsses data from the actual 
    # servo positions then calls to update the Forward Kinematics
    # X,Z and Z position.
    def syncServoPosition(self):
        self.shoulder.syncServo()
        self.arm.syncServo()
        self.wrist.syncServo()
        self.imuUpdateFK()
    
    # When we need to move the joints of the robot, using this 
    # function will make sure everything stays syncronized.
    def setServoPos(self, Shoulder, Arm, Wrist):
        self.shoulder.setServoPos(Shoulder)
        self.arm.setServoPos(Arm)
        self.wrist.setServoPos(Wrist)
        self.imuUpdateFK()
    
    def setServoRest(self):
        self.shoulder.setServoPos(self.shoulder.rest)
        self.arm.setServoPos(self.arm.rest)
        self.wrist.setServoPos(self.wrist.rest)
        self.imuUpdateFK()
    
    
    # If for any reason you need to adjust the Min or Max of a 
    # servo, then you need to also update the class.
    def updateServo(self):
        self.shoulder.updateServo()
        self.arm.updateServo()
        self.wrist.updateServo()
        self.imuUpdateFK()
    

    # Using the servo positions passed in, this routine will 
    # calculate where the foot is relative to the Robot Plane 
    # of Reference. (RPoR) Since this could be used in planning
    # the current position in the class is not updated.
    def forwardKinematics(self, shoulder, arm, wrist):
        LTF = math.sqrt(self.LWF2 + self.LTW2 - 2*self.LWF*self.LTW*math.cos(math.radians(wrist+self.wrist.offset)))
        AFW = math.degrees(math.acos((LTF*LTF + self.LTW2 - self.LWF2)/(2*LTF*self.LTW)))
        LTFa = math.cos(math.radians(AFW - arm + self.arm.offset)) * LTF
        LSF = math.sqrt(self.LST2 + LTFa*LTFa)
        workX = (math.sin(math.acos(self.LST/LSF)+math.radians(shoulder + self.shoulder.offset))*LSF)
        if self.type == 0 or self.type == 2:
            X = -workX - self.LXS
        else:
            X = workX + self.LXS
        workY = (LTF * math.sin(math.radians(arm - AFW + self.arm.offset)))
        if self.type == 0 or self.type == 1:
            Y = workY + self.LYS
        else:
            Y = workY - self.LYS
        Z = math.cos(math.acos(self.LST/LSF) + math.radians(shoulder + self.shoulder.offset))*LSF
        # Only need the X, Y and Z, there rest is for debugging :-)
        return {"X":X, "Y":Y, "Z":Z}

    # This routine call the Forward Kinimatics routine passing 
    # the current remembered servo positions then saves the 
    # foot coordinates to the Class storage.
    def updateFK(self):
        data = self.forwardKinematics(self.shoulder.pos, self.arm.pos, self.wrist.pos)
        self.RPoR.X = data.get("X")
        self.RPoR.Y = data.get("Y")
        self.RPoR.Z = data.get("Z")

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
        imuXZA = xzA + self.ICoMPoR.roll
        imuYZA = yzA + self.ICoMPoR.pitch
        # Now we can calculate the new X, Y, and Z based on the 
        # new origin and angle.
        ImuX = math.sin(imuXZA)*xzL
        ImuY = math.sin(imuYZA)*yzL
        ImuZ = -math.cos(imuYZA)*yzL
        return {"X":ImuX, "Y":ImuY, "Z":ImuZ}

    # This will make sure the current Inertial Centre of Mass 
    # Frame of Reference is up to date
    def imuUpdateFK(self):
        self.updateFK()
        IComPoR = self.imuForwardKinimatics(self.RPoR.X, self.RPoR.Y, self.RPoR.Z)
        self.ICoMPoR.X = IComPoR.get("X")
        self.ICoMPoR.Y = IComPoR.get("Y")
        self.ICoMPoR.Z = IComPoR.get("Z")
    
    # This is a request to work out where to set the servos 
    # in order to place the foot at the requested coordinates.
    # The preceding R in the coordinates is the Request.
    def inverseKinematics(self, RX, RY, RZ):
        # Lets first clear the error indication.
        error = 0
        # Next we need to translate the coordinates from the 
        # RPoR to the Shoulder Plane of Reference (SPoR).
        # X-Axis, Note: the shoulders on the left and right work 
        # opposite to each other, With the left being the 
        # negative side, we need to invert the axis for the 
        # left side
        if self.type == 0 or self.type == 2:
            legX = -RX - self.LXS
        else:
            legX = RX - self.LXS
        # Y-Axis
        if self.type == 0 or self.type == 1:
            legY = RY - self.LYS
        else:
            legY = RY + self.LYS
        # Z-Axis, Since we made the RPoR the same height as the 
        # shoulder, there is no offset required here.
        legZ = RZ
        # Lets work out the Length Shoulder Foot (LSF)
        # Note this is in the XZ Plane relative to the SPoR
        LSF = math.sqrt((legX * legX) + (legZ * legZ))
        # Now that we have Length Shoulder Foot and we know 
        # Length Shoulder Top, lets work out the 
        # Length Top Foot z (LTFz), we use the z suffix here, 
        # because this only relative to the X-Z plane and not 
        # the XY plane
        LTFz = math.sqrt((LSF * LSF) - self.LST2)
        # Next we need to work out the position the shoulder 
        # servo has to be in.  This is made of two angles.
        # The angle formed by the triangle consisting of the 
        # foot, shoulder and the top of the arm, the outside 
        # angle and the triangle formed by the shoulder, foot 
        # and the 90 degree angle dictly below the shoulder.
        Ai = math.asin(legX/LSF) # Angle inside
        Ao = math.acos(self.LST/LSF)  # Angle Outside
        # Just a reminder that all angle math in Python is in 
        # Radians, however the servo control and out offsets 
        # are all in degrees.
        shoulder = 180 - math.degrees(Ai + Ao)-self.shoulder.offset
        # Now that we know what the shoulder servo angle should 
        # be, lets see if it's within the servos range limit
        if shoulder < self.shoulder.min:
            error = 1
            shoulder = self.shoulder.min
        if shoulder > self.shoulder.max:
            error = 2
            print("Error 2 - Shoulder:%.2f, Max:%.2f" % (shoulder, self.shoulder.max))
            shoulder = self.shoulder.max
        # Now we need to work out the Length Top of arm to the 
        # Foot in the Y-Axis
        LTF = math.sqrt((LTFz*LTFz) + (legY*legY))
        print("Leg Number %d, X:%0.1f, Y:%0.1f, Z:%0.1f, LSF:%0.3f, LTF:%0.2f, LST:%0.3f, LST2:%0.3f" % (self.type, legX, legY, legZ, LSF, LTF, self.LST, self.LST2))
        sleep(0.1)
        if self.MaxLTF < LTF:
            # "Warning, LTF is longer than LTW and LWF combined, this is impossible"
            error = 7
            arm = 0
            LTF = self.MaxLTF
            wrist = self.wrist.max
            ServoWR = math.radians(wrist)
        elif self.MinLTF > LTF:
            # "Warning, LTF is less than LTW and LWF bent at the 
            # wrist to the min pos"
            error = 8
            arm = 0
            LTF = self.MinLTF
            wrist = self.wrist.min
            ServoWR = math.radians(wrist)
        else:
            # Now we can work out the wrist servo position using 
            # the Law of Cosines.
            # Python work in Radians
            WristCosC = (self.LTW2 + self.LWF2 - (LTF * LTF)) / self.LTWxLWFx2
            #print("IK ServoWrist cosC:", WristCosC)
            if WristCosC > 1.0:
                WristCosC = 1.0
            ServoWR = math.acos(WristCosC)
            # Now that we have the servo position in radian we 
            # convert it to degrees
            wrist = math.degrees(ServoWR)
            # In theory we don't need to do these checks with the 
            # error trap for errors 7 and 8, but we will leave it 
            # in for now.
            if wrist < self.wrist.min:
                error = 5
                wrist = self.wrist.min
            elif wrist > self.wrist.max:
                error = 6
                wrist = self.wrist.max
            ServoWR = math.radians(wrist)
        # Now we can work out the angle for the arm relative to the line to the foot
        #print("Afw = asin(%.3f), sin(wrist):%.3f, LWF:%.3f, LTF:%0.3f Error:%d" % ((math.sin(ServoWR)*self.LWF)/LTF, math.sin(ServoWR), self.LWF, LTF, error))
        #sleep(0.1)
        Afw = math.asin((math.sin(ServoWR)*self.LWF)/LTF)
        # When you square legY as we did in an equation above, 
        # you will always get a positive result.  The thing is, 
        #sometimes we want the foot to move in the negative 
        # direction.  For this reason, we check to see if that 
        # was the case and invert the value if it was.
        if legY>0:
            Af = math.acos(LTFz/LTF)
        else:
            Af = -math.acos(LTFz/LTF)
        # Then combine with the angle we need the foot at 
        # relative to the top of the arm to get the servo 
        # position
        arm = self.arm.offset + math.degrees(Afw - Af)
        #print("Arm Servo:%.2f, Afw:%.3f, Af:%.3f, ArmOffset:%.2f" % (arm, Afw, Af, self.arm.offset))
        if arm < self.arm.min:
            error = 3
            arm = self.arm.min
        if arm > self.arm.max:
            error = 4
            arm = self.arm.max
        # In theory, we should be able to use this result even if 
        # it was not able to get the correct target position.
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
        CoMxA = xzA - self.ICoMPoR.roll
        CoMyA = yzA - self.ICoMPoR.pitch
        # With the new angle and the line lengths, we can work 
        # out the XYZ coordinates of the relative to the CoM
        if RX <0:
            CoMx = -math.cos(CoMxA)*xzL
        else:
            CoMx = math.cos(CoMxA)*xzL
        CoMy = math.cos(CoMyA)*yzL
        CoMz = math.sin(CoMyA)*yzL
        # So now that it is orientated correctly, lets adjust the offset
        RPoRx = CoMx + self.CoMxOffset
        RPoRy = CoMy + self.CoMyOffset
        RPoRz = CoMz + self.CoMzOffset
        print("imuIK - xzL:%.2f, yzL:%.2f - xzA:%.3f, yzA:%.3f - CoMxA:%.3f, CoMyA:%.3f" % (xzL, yzL, xzA, yzA, CoMxA, CoMyA))
        print("imuIK - RX:%.2f, RY:%.2f, RZ:%.2f - CoMx:%.2f, CoMy:%.2f, CoMz:%.2f - RPoRx:%.2f, RPoRy:%.2f, RPoRz:%.2f" %(RX, RY, RZ, CoMx, CoMy, CoMz, RPoRx, RPoRy, RPoRz))
        return {"X":RPoRx, "Y":RPoRy, "Z":RPoRz}

    # The RX, RY and RZ are the requested coordinated relative
    # to the Robot Plane of Reference.
    # This also stores in the class the last set of positions 
    # we requested the servos move to.
    def moveToRPoR(self, RX, RY, RZ):
        servos = self.inverseKinematics(RX, RY, RZ)
        if servos.get("Error") == 0:
            self.setServoPos(servos.get("Shoulder"), servos.get("Arm"), servos.get("Wrist"))
            return {"Error":servos.get("Error"), "Shoulder":self.shoulder.pos, "Arm":self.arm.pos, "Wrist":self.wrist.pos}
        else:
            return {"Error":servos.get("Error"), "Shoulder":self.shoulder.pos, "Arm":self.arm.pos, "Wrist":self.wrist.pos}
    
    def rotateAboutCoM(self, pitch, roll):
        xzL = math.sqrt((self.ICoMPoR.X*self.ICoMPoR.X)+(self.ICoMPoR.Z*self.ICoMPoR.Z))
        yzL = math.sqrt((self.ICoMPoR.Y*self.ICoMPoR.Y)+(self.ICoMPoR.Z*self.ICoMPoR.Z))
        xzA = math.asin(self.ICoMPoR.X/xzL) + pitch
        yzA = math.asin(self.ICoMPoR.Y/yzL) + roll
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
        print("moveToICoMPoR:", RPoR)
        servos = self.inverseKinematics(RPoR.get("X"), RPoR.get("Y"), RPoR.get("Z"))
        if servos.get("Error") == 0:
            self.setServoPos(servos.get("Shoulder"), servos.get("Arm"), servos.get("Wrist"))
            return {"Error":servos.get("Error"), "Shoulder":self.shoulder.pos, "Arm":self.arm.pos, "Wrist":self.wrist.pos}
        else:
            return {"Error":servos.get("Error"), "Shoulder":self.shoulder.pos, "Arm":self.arm.pos, "Wrist":self.wrist.pos}
       
    
# The Feet class creates 4 Foot objects based on the Foot class.
# It also provide a number of common update interfaces such as
# update the roll and pitch of the robot.
# It also has a number of unified movement functions that
# combine all 4 feet to assist with ballance and other
# coordinated movements.
class Feet():
    def __init__(self, FLShoulder, FLArm, FLWrist, FRShoulder, FRArm, FRWrist, BLShoulder, BLArm, BLWrist, BRShoulder, BRArm, BRWrist):
        # These are the objects representing each of the feet
        self.FL = Foot(0, FLShoulder, FLArm, FLWrist)
        self.FR = Foot(1, FRShoulder, FRArm, FRWrist)
        self.BL = Foot(2, BLShoulder, BLArm, BLWrist)
        self.BR = Foot(3, BRShoulder, BRArm, BRWrist)
        # This is the last updated Inertial Measurement Unit 
        # (IMU) input
        self.Pitch = 0
        self.Roll = 0
        # This is where we want the current Pitch and roll to be
        self.targetPitch = 0
        self.targetRoll = 0
        # This value correct for an error in mounting of the IMU
        self.rollOffset = 0.06701
        self.pitchOffset = 0.06604
        # To help with setting this up, we will take a number of 
        # samples and average them out. Set this to the number 
        # of samples to be used, as each sample comes in, this 
        # value will be decremented.
        self.imuCalibrate = 0
        self.imuLastCalibration = 0
        self.imuCalibrationRoll = 0
        self.imuCalibrationPitch = 0
        # When set to 1, the robot will activly try to keep the 
        # body at the target pitch and roll.
        self.autoLevel = 0
    
    def __repr__(self):
        PrintStr = "Feet Class - "
        if self.autoLevel == 1:
            AutoLevelStr = "Auto Level is On "
        else:
            AutoLevelStr = "Auto Level is Off "
        return PrintStr + AutoLevelStr

    def __str__(self):
        print("Feet Class Status")
        print(self.FL)
        print(self.FR)
        print(self.BL)
        print(self.BR)
        print("Roll:%.4f[%.3f] Pitch:%.4f[%.3f] TargetRoll:%.2f TargetPitch:%.2f Radians[Degrees]" % (self.Roll, math.degrees(self.Roll), self.Pitch, math.degrees(self.Pitch), self.targetRoll, self.targetPitch))
        if self.autoLevel == 1:
            al_State = "Auto Level is On"
        else:
            al_State = "Auto Level is Off"
        return al_State
        
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
        if self.imuCalibrate > 0:
            if self.imuLastCalibration == 0:
                self.imuLastCalibration = self.imuCalibrate
                self.imuCalibrationRoll = 0
                self.imuCalibrationPitch = 0
            if self.imuCalibrate == 1:
                self.imuCalibrate = 0
                self.rollOffset = -self.imuCalibrationRoll / self.imuLastCalibration
                self.pitchOffset = -self.imuCalibrationPitch / self.imuLastCalibration
                self.imuLastCalibration = 0
            else:
                self.imuCalibrate = self.imuCalibrate - 1
                self.imuCalibrationRoll = self.imuCalibrationRoll + roll
                self.imuCalibrationPitch = self.imuCalibrationPitch + pitch
        if self.Pitch <> (pitch + self.pitchOffset) or self.Roll <> (roll + self.rollOffset):
            self.Pitch = pitch  + self.pitchOffset
            self.Roll = roll + self.rollOffset
            self.FL.setIMUdata(self.Pitch, self.Roll)
            self.FR.setIMUdata(self.Pitch, self.Roll)
            self.BL.setIMUdata(self.Pitch, self.Roll)
            self.BR.setIMUdata(self.Pitch, self.Roll)
            if self.autoLevel == 1:
                self.levelRobot()

    # This routine calculates the changes that are required to 
    # level the robots RPoR with the ICoMPoR then calls the 
    # commands to move the servos.
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
        
    def rest(self):
        self.FL.setServoRest()
        self.FR.setServoRest()
        self.BL.setServoRest()
        self.BR.setServoRest()
    
    # This routine calls the system to make a simle 4 leeg 
    # linear movement.
    def moveRobotICoMPoR(self, X, Y, Z):
        print("FL", self.FL.moveToICoMPoR(self.FL.ICoMPoR.X + X, self.FL.ICoMPoR.Y + Y, self.FL.ICoMPoR.Z - Z))
        print("FR", self.FR.moveToICoMPoR(self.FR.ICoMPoR.X + X, self.FR.ICoMPoR.Y + Y, self.FR.ICoMPoR.Z - Z))
        print("BL", self.BL.moveToICoMPoR(self.BL.ICoMPoR.X + X, self.BL.ICoMPoR.Y + Y, self.BL.ICoMPoR.Z - Z))
        print("BR", self.BR.moveToICoMPoR(self.BR.ICoMPoR.X + X, self.BR.ICoMPoR.Y + Y, self.BR.ICoMPoR.Z - Z))
    
    def moveRobotRPoR(self, X, Y, Z):
        print("FL", self.FL.moveToRPoR(self.FL.RPoR.X + X, self.FL.RPoR.Y + Y, self.FL.RPoR.Z - Z))
        print("FR", self.FR.moveToRPoR(self.FR.RPoR.X + X, self.FR.RPoR.Y + Y, self.FR.RPoR.Z - Z))
        print("BL", self.BL.moveToRPoR(self.BL.RPoR.X + X, self.BL.RPoR.Y + Y, self.BL.RPoR.Z - Z))
        print("BR", self.BR.moveToRPoR(self.BR.RPoR.X + X, self.BR.RPoR.Y + Y, self.BR.RPoR.Z - Z))
    
    