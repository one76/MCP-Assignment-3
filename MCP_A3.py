from manim import *

# == UNIT CONVERSION FROM MM TO MUNIT ==
# Height of layout is 6 munits
H=1800 #mm | Height of layouts
U=6/H

STATIC          = 0
ANIMATE         = 1
DRIVE_SPEED     = 150*U #mm/s
ROTATE_SPEED    = 360 #deg/s

class Layouts(Scene):
    R1Pos=[[0,0,0],[0,0,0],[0,0,0]]
    R2Pos=[[0,0,0],[0,0,0],[0,0,0]]
    RockRad=40 # mm

    def DrawLayout1(self, staticOrAnimate):
        W=1600 # mm
        L1=Rectangle(
                width=W*U,
                height=H*U,
                color=WHITE
            ).set_fill(GOLD_A, opacity=1)

        # Lines
        HLine=Line([U*(-W/2),U*(-H/2+600),0],[U*(W/2),U*(-H/2+600),0])
        VLine=Line([0,U*(H/2),0],[0,U*(-H/2),0])
        
        # Rocks
        Layouts.R1Pos[0]=[U*(-W/2+80),U*(-H/2+680),0]
        Layouts.R2Pos[0]=[400*U,300*U,0] # Estimated starting position
        R1=Circle(radius=Layouts.RockRad*U, color=GREY_D).set_fill(GREY_C, opacity=1)
        R2=Circle(radius=Layouts.RockRad*U, color=GREY_D).set_fill(GREY_C, opacity=1)
        R1.move_to(Layouts.R1Pos[0])
        R2.move_to(Layouts.R2Pos[0])
        
        Layout1=VGroup(L1, HLine, VLine, R1, R2)

        # Draw
        if staticOrAnimate==STATIC:
            self.add(Layout1)
        elif staticOrAnimate==ANIMATE:
            self.play(DrawBorderThenFill(Layout1, lag_ratio=0.15))

        return Layout1, W # Return layout group, width of layout

class Kobuki(Scene):
    Radius=175 # mm
    Circumference=2*PI*Radius # mm
    current_angle=0 # in deg

    def setCurrAngle(angle):
        Kobuki.current_angle=angle

    def DrawKobuki(self, staticOrAnimate, startPos, startAngle):
        kobuki_body=Circle(radius=Kobuki.Radius*U,color=GREY_E).set_fill(GREY_C, opacity=1)
        frontMarker=Arrow(
            start   = kobuki_body.get_center() + RIGHT*(Kobuki.Radius*U/4), 
            end     = kobuki_body.get_center() + RIGHT*(Kobuki.Radius*U),
            color   = BLACK
        )
        kobuki=VGroup(kobuki_body,frontMarker)

        kobuki.move_to(startPos)
        kobuki.rotate(startAngle*(PI/180))
        
        if staticOrAnimate==STATIC:
            self.add(kobuki)
        elif staticOrAnimate==ANIMATE:
            self.play(DrawBorderThenFill(kobuki))

        return kobuki
    
    def Drive(self, kobuki, distance, speed):
        self.play(
            kobuki.animate.shift([
                distance*np.cos(Kobuki.current_angle*(PI/180)),
                distance*np.sin(Kobuki.current_angle*(PI/180)),
                0
            ]),
            run_time=distance/speed,
            rate_func=linear
        )
    
    def Rotate(self, kobuki, angle, speed):
        Kobuki.current_angle=(Kobuki.current_angle+angle)%360
        angle_rad=angle*(PI/180)

        self.play(Rotate(
            kobuki, 
            angle_rad,
            run_time=(360/speed), 
            rate_func=linear
        ))

class MarsRoverNavigation(Scene):
    rover=Circle()

    def SetTest1(self):
        Layout1, W = Layouts.DrawLayout1(self,STATIC)

        roverStartPos=[
            U*(-W/2+225+Kobuki.Radius),
            U*(-H/2+Kobuki.Radius),
            0
        ]
        roverStartAngle=90
        MarsRoverNavigation.rover=Kobuki.DrawKobuki(self,STATIC,roverStartPos,roverStartAngle)
        Kobuki.setCurrAngle(90)

    def construct(self):
       MarsRoverNavigation.SetTest1(self)
       Kobuki.Drive (self,MarsRoverNavigation.rover,200*U,DRIVE_SPEED) # drive 200mm
       Kobuki.Rotate(self,MarsRoverNavigation.rover,-90,ROTATE_SPEED) # rotate 90˚
       Kobuki.Drive (self,MarsRoverNavigation.rover,200*U,DRIVE_SPEED)
       self.wait(2)
