from manim import *
import random
import math
from enum import Enum

# == UNIT CONVERSION FROM MM TO MUNIT ==
# Height of layout is 6 munits
H=1800 #mm | Height of layouts
U=6/H

STATIC          = 0
ANIMATE         = 1
DRIVE_SPEED     = 150*U #mm/s
ROTATE_SPEED    = 180 #deg/s
CCW             = 1
CW              = -1

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
    # == KOBUKI VARIABLES ==
    Radius=175 # mm
    Circumference=2*PI*Radius # mm
    current_angle=0 # in deg

    # Kobuki_Y is in direction of kobuki face (arrow)
    # Kobuki_X is perpendicular to the right of the kobuki face (arrow)
    Kobuki_Y=np.array([0,0,0])
    Kobuki_X=np.array([0,0,0])

    # Ultrasonic Sensor Mobject
    US_View=None
    US_View_Position_List=None

    # == METHODS ==

    def setCurrAngle(angle):
        Kobuki.current_angle=angle

    def UpdateKobukiFaceDirections(angle):
        angle_rad=angle*(PI/180)
        Kobuki.Kobuki_Y=np.array([np.cos(angle_rad),np.sin(angle_rad),0])
        Kobuki.Kobuki_X=np.array([np.cos(PI/2-angle_rad),-np.sin(PI/2-angle_rad),0])

    def DrawUS(self, kobuki, draw):
        US_ConeView_Height=1500*U
        US_ConeView_Base=600*U

        # From Ultrasonic Sensor Data Sheet MB1043 at 3.3V Graph C
        Kobuki.US_View_Position_List=[
            kobuki.get_center(),
            kobuki.get_center()-Kobuki.Kobuki_X*50*U     +   Kobuki.Kobuki_Y*300*U,
            kobuki.get_center()-Kobuki.Kobuki_X*300*U   +   Kobuki.Kobuki_Y*900*U,
            kobuki.get_center()+Kobuki.Kobuki_X*0       +   Kobuki.Kobuki_Y*US_ConeView_Height,
            kobuki.get_center()+Kobuki.Kobuki_X*300*U   +   Kobuki.Kobuki_Y*900*U,
            kobuki.get_center()+Kobuki.Kobuki_X*50*U     +   Kobuki.Kobuki_Y*300*U
        ]

        Kobuki.US_View=Polygon(*Kobuki.US_View_Position_List)
        Kobuki.US_View.set_fill(color=BLUE_B,opacity=0.1)

        if draw==True:
            self.add(Kobuki.US_View)

    def DrawKobuki(self, staticOrAnimate, startPos, startAngle, drawUSView):
        # KOBUKI STARTS OFF FACING TO THE RIGHT
        
        # Kobuki Parts
        kobuki_body=Circle(radius=Kobuki.Radius*U,color=GREY_E).set_fill(GREY_C, opacity=1)
        frontMarker=Arrow(
            start   = kobuki_body.get_center() + RIGHT*(Kobuki.Radius*U/4), 
            end     = kobuki_body.get_center() + RIGHT*(Kobuki.Radius*U),
            color   = BLACK
        )

        # Putting kobuki together
        kobuki=VGroup(kobuki_body,frontMarker)
        kobuki.move_to(startPos)
        kobuki.rotate(startAngle*(PI/180))

        # Update Kobuki Axis
        Kobuki.setCurrAngle(startAngle)
        Kobuki.UpdateKobukiFaceDirections(startAngle)
    
        # Draw to Screen
        if staticOrAnimate==STATIC:
            self.add(kobuki)
        elif staticOrAnimate==ANIMATE:
            self.play(DrawBorderThenFill(kobuki))

        # Draw Ultrasonic Sensor Cone
        if drawUSView==True:
            Kobuki.DrawUS(self,kobuki,drawUSView)

        return kobuki

    def Drive(self, kobuki, distance, speed):
        print(Kobuki.Kobuki_Y)
        self.play(
            kobuki.animate.shift(distance*Kobuki.Kobuki_Y),
            Kobuki.US_View.animate.shift(distance*Kobuki.Kobuki_Y),
            run_time=distance/speed,
            rate_func=linear
        )
    
    def Rotate(self, kobuki, angle, speed):
        Kobuki.current_angle=(Kobuki.current_angle+angle)%360
        Kobuki.UpdateKobukiFaceDirections(Kobuki.current_angle)
        angle_rad=angle*(PI/180)

        self.play(
            Rotate(
                kobuki, 
                angle_rad,
                run_time=(angle/speed), 
                rate_func=linear
            ),
            Rotate(
                Kobuki.US_View, 
                angle_rad,
                about_point=kobuki.get_center(),
                run_time=(angle/speed), 
                rate_func=linear
            )
        )

    def UpdateDetection():
        detectRock1=PointInsidePolygon.point_inside_polygon(
            Layouts.R1Pos[0][0],
            Layouts.R1Pos[0][1],
            Kobuki.US_View.get_all_points()
        )
        detectRock2=PointInsidePolygon.point_inside_polygon(
            Layouts.R2Pos[0][0],
            Layouts.R2Pos[0][1],
            Kobuki.US_View.get_all_points()
        )
        if detectRock1 or detectRock2: return True
        else: return False

# Testing Point detection
class PointInsidePolygon(Scene):
    size=1
    poly_points=[
        [-size,size,0],
        [size,size,0],
        [size,-size,0],
        [-size,-size,0]
    ]
    
    def construct(self):
        poly=Polygon(*PointInsidePolygon.poly_points)
        self.add(poly)

        for dot in range(20):
            d_coord=[
                random.uniform(-(PointInsidePolygon.size+2),PointInsidePolygon.size+2),
                random.uniform(-(PointInsidePolygon.size+2),PointInsidePolygon.size+2),
                0
            ]
            d=Dot(d_coord)

            if PointInsidePolygon.point_inside_polygon(
                d_coord[0],
                d_coord[1],
                PointInsidePolygon.poly_points
            )==True:
                d.set_color(GREEN)
            else: 
                d.set_color(RED)
            
            self.add(d)

    def point_inside_polygon(x, y, poly, include_edges=True):
        '''
        Test if point (x,y) is inside polygon poly.

        poly is N-vertices polygon defined as 
        [(x1,y1),...,(xN,yN)] or [(x1,y1),...,(xN,yN),(x1,y1)]
        (function works fine in both cases)

        Geometrical idea: point is inside polygon if horisontal beam
        to the right from point crosses polygon even number of times. 
        Works fine for non-convex polygons.

        code from:
            https://stackoverflow.com/questions/39660851/deciding-if-a-point-is-inside-a-polygon
        '''
        n = len(poly)
        inside = False

        p1x, p1y, p1z = poly[0]
        for i in range(1, n + 1):
            p2x, p2y, p2z = poly[i % n]
            if p1y == p2y:
                if y == p1y:
                    if min(p1x, p2x) <= x <= max(p1x, p2x):
                        # point is on horisontal edge
                        inside = include_edges
                        break
                    elif x < min(p1x, p2x):  # point is to the left from current edge
                        inside = not inside
            else:  # p1y!= p2y
                if min(p1y, p2y) <= y <= max(p1y, p2y):
                    xinters = (y - p1y) * (p2x - p1x) / float(p2y - p1y) + p1x

                    if x == xinters:  # point is right on the edge
                        inside = include_edges
                        break

                    if x < xinters:  # point is to the left from current edge
                        inside = not inside

            p1x, p1y = p2x, p2y

        return inside

# ===

class State(Enum):
    IDLE    = 0
    SEARCH  = 1
    OBJECT  = 2

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

        # Draw the Kobuki
        MarsRoverNavigation.rover=Kobuki.DrawKobuki(self,STATIC,roverStartPos,roverStartAngle,True)

    def updateUS_View(self, detected):
        if detected==True:
            Kobuki.US_View.set_color(RED).set_fill(color=RED,opacity=0.5)
        else:
            Kobuki.US_View.set_color(BLUE).set_fill(color=BLUE_B,opacity=0.3)

    def construct(self):
        MarsRoverNavigation.SetTest1(self)
        state=State.IDLE
        
        for _ in range(50):
            detected=Kobuki.UpdateDetection()

            match state:
                case State.IDLE:
                    self.wait(0.5)
                    state=State.SEARCH
                case State.SEARCH:
                    if detected:
                        state=State.OBJECT
                        MarsRoverNavigation.updateUS_View(self, detected)
                    else:
                        Kobuki.Rotate(self,MarsRoverNavigation.rover,2*CCW,ROTATE_SPEED)
                case State.OBJECT:
                    if detected:
                        Kobuki.Drive(self,MarsRoverNavigation.rover,200*U,DRIVE_SPEED)
                    else:
                        MarsRoverNavigation.updateUS_View(self, detected)
                        state=State.IDLE