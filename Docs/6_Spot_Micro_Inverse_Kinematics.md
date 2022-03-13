# 6) Spot Micro Inverse Kinematics

# Introduction

It’s one thing to know where the foot is in 3D space, but it’s another to know how to set the joints to place the foot into a given target set of X, Y and Z coordinates.
Lets call these values Xt, Yt and Zt.
In a setup with only 3 joints to work with, and only two of them in the same axis, it is possible to work out how to set the servos to get to a known position.

## The Shoulder Servo

For Spot, it’s easiest to work out the Shoulder servo first.

![X-Z plane view of the leg](https://paper-attachments.dropbox.com/s_3312125F65CA3DC01444C81917CB3E917B429E9A33B5A513DF0D3BDF0783359C_1641199376333_IK_XZ_View.jpg)


There is a triangle formed by the Shoulder, the Foot and the right angle point Z down from the Shoulder joint relative to the robots body.   The length between the Shoulder and the foot (LSF can be found using the equation:
$$LSF = \sqrt{(Xt-LXS)^2 + Zt^2}$$
Now that we know that, we can calculate the effective length of the leg between the Top of the arm and the Foot is the Z-Axis LTFz.  Keep in mind we know the fixed length LST.
$$LTFz = \sqrt{LSF^2 - LST^2}$$
We will need to remember this value as we will need it again later.
We need to work out two more angles:

- Ai or Angle inside is the angle between the two lines Z-Axis relative to the body and the LSF line.
- Ao or the Angle outside is the angle between the LST line and the LSF lines.

$$Ai = asin(\frac{Xt-LXS}{LSF})$$
$$Ao = acos(\frac{LST}{LSF})$$
The servo position we need for S is now able to be worked out.
$$S = Ai + Ao - 90$$
Keep in mind that a 0° position is centered with the leg pointing straight down, that is $$Xt = LXS + LST$$ or 88 mm, therefore an offset may need to be added to the Actual Servo command position.
That’s one of three worked out, now lets change our working plane 🙂 
We will need to work on the plane where both the Top of arm and the wrist work in.
We don’t need to worry too much about the X or Z axis now as we have the LTFz from above, we also know the LTW and LWF lengths, so all we realy need now is the Y-Axis.

![Y-LTFz Plane view of leg](https://paper-attachments.dropbox.com/s_3312125F65CA3DC01444C81917CB3E917B429E9A33B5A513DF0D3BDF0783359C_1641200436772_IK_YZ_View.jpg)


As you might guess, we have another set of triangles to work with. 🙂 
First thing we need to work out is the Length between the Top of arm and the Foot (LTF).
Essentially we have the lengths of two side of a right angle triangle, here is the formula:
$$LTF = \sqrt{LTFz^2 + (Yt - LYS)^2}$$
Now that we have the three side of the Top of arm, Wrist and Foot triangle, we can work out the angle of the Wrist.  Back to the law of cosines 🙂 
$$c^2 = a^2 + b^2 -2*a*b*\cos(C)$$ or $$\cos(C) = \frac{a^2 + b^2 - c^2}{2*a*b}$$

$$Wrist = acos(\frac{LTW^2 + LWF^2 - LTF^2}{2*LTW*LWF})$$
Now we have two of the three servo positions, lets work on the last one.
We need to work out two angles here Af and Afw.
For Afw we will use the law of sines.
$$\frac{\sin(A)}{a} = \frac{\sin(B)}{b} = \frac{\sin(C)}{c}$$
$$Afw = asin(\frac{\sin(Wrist)*LWF}{LTF})$$
$$Af = acos(\frac{LTFz}{LTF})$$
Next we can calculate the position for the Top of arm Servo T.
$$T = Afw+Af -90$$
So now we have all three angles.

**Just a couple of notes:**
In this example, I used degrees, in Python, most of the functions will be in radians, so we will need to do some conversions.
90° = $$\pi/2$$

