#  =========================
# |    MCP Assignment 3     |
# |   Michael and Michael   |
#  =========================


# ==== IMPORTS ====
from manim import *
from tkinter import N
from charset_normalizer import detect
from enum import Enum
from pathlib import Path
from numpy import poly
from ANSI_COLOR_ESCAPE_CODES import *
import random
import math
# ==== IMPORTS ====


# ==== DEBUGGING OUTPUT FILE ====
output = open("output.txt","w")
output.write(Red+"===== START =====\n"+Color_Off)
# ==== DEBUGGING OUTPUT FILE ====


# ==== UNIT CONVERSION ====
# Manim uses "munits"
# Height of layout is 6 munits
H=1800  # mm | Height of layouts
U=6/H   # Use U to convert from mm to munits
# ==== UNIT CONVERSION ====


# ==== MACROS ====
DRIVE_SPEED     = 250*U # mm/s  | Kinda broken
ROTATE_SPEED    = 200   # deg/s | Kinda broken
CCW             = 1
CW              = -1
# ==== MACROS ====


# ==== MANIM SET-UP CLASSES AND FUNCTIONS ====

class Layouts(Scene):
    R1Pos=[[0,0,0],[0,0,0],[0,0,0]] # Rock 1 position on screen
    R2Pos=[[0,0,0],[0,0,0],[0,0,0]] # Rock 2 position on screen
    L1_Positions=None       # Layout 1 outline coordinates
    L2and3_Positions=None   # Layout 2 and 3 outline coordinates
    RockRad=40 # mm. Estimated rock radius

    def DrawLayout1(self):
        W=1600 # mm
        L1=Rectangle(
            width=W*U,
            height=H*U,
            color=WHITE
        ).set_fill(GOLD_A, opacity=1)
        Layouts.L1_Positions=L1.get_all_points()

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
        self.add(Layout1)
        return Layout1 # Return layout group, width of layout

    def DrawLayout2(self):
        W=800       # mm
        Short_H=600 # mm
        Tall_H=1200 # mm
        L2_ORIGIN=ORIGIN+DOWN

        sections=[ # [BL, BR, TL, TR]
            Rectangle(
                width=W*U,
                height=Short_H*U,
                color=WHITE
            ).set_fill(GOLD_A, opacity=1),
            Rectangle(
                width=W*U,
                height=Short_H*U,
                color=WHITE
            ).set_fill(GOLD_A, opacity=1),
            Rectangle(
                width=W*U,
                height=Tall_H*U,
                color=WHITE
            ).set_fill(GOLD_A, opacity=1),
            Rectangle(
                width=W*U,
                height=Tall_H*U,
                color=WHITE
            ).set_fill(GOLD_A, opacity=1)
        ]

        # Moving sections into correct positions
        sections[0].shift(L2_ORIGIN + DOWN*(Short_H/2)*U + LEFT*(W/2)*U + RIGHT*(100)*U) # BL
        sections[1].shift(L2_ORIGIN + DOWN*(Short_H/2)*U + RIGHT*(W/2+100)*U) # BR
        sections[2].shift(L2_ORIGIN + UP*(Tall_H/2)*U + LEFT*(W/2+100)*U) #TL
        sections[3].shift(L2_ORIGIN + UP*(Tall_H/2)*U + RIGHT*(W/2)*U)

        # Manually setting coordinates of the outline of layout 2
        Layouts.L2and3_Positions=[
            [L2_ORIGIN[0],L2_ORIGIN[1],0],
            [L2_ORIGIN[0]-110*U,L2_ORIGIN[1],0],
            [L2_ORIGIN[0]-110*U,L2_ORIGIN[1]+Tall_H*U,0],
            [L2_ORIGIN[0]-110*U-W*U,L2_ORIGIN[1]+Tall_H*U,0],
            [L2_ORIGIN[0]-110*U-W*U,L2_ORIGIN[1],0],
            [L2_ORIGIN[0]-W*U+100*U,L2_ORIGIN[1],0],
            [L2_ORIGIN[0]-W*U+100*U,L2_ORIGIN[1]-Short_H*U,0],
            [L2_ORIGIN[0]+W*U+100*U,L2_ORIGIN[1]-Short_H*U,0],
            [L2_ORIGIN[0]+W*U+100*U,L2_ORIGIN[1],0],
            [L2_ORIGIN[0]+W*U,L2_ORIGIN[1],0],
            [L2_ORIGIN[0]+W*U,L2_ORIGIN[1]+Tall_H*U,0],
            [L2_ORIGIN[0],L2_ORIGIN[1]+Tall_H*U,0],
        ]
        
        # Rocks
        Layouts.R1Pos[1]=L2_ORIGIN + [(W/2+100)*U,(-Short_H/2)*U,0]
        Layouts.R2Pos[1]=L2_ORIGIN + [W/2*U,Tall_H/2*U,0]
        R1=Circle(radius=Layouts.RockRad*U, color=GREY_D).set_fill(GREY_C, opacity=1)
        R2=Circle(radius=Layouts.RockRad*U, color=GREY_D).set_fill(GREY_C, opacity=1)
        R1.move_to(Layouts.R1Pos[1])
        R2.move_to(Layouts.R2Pos[1])
        
        Layout2=VGroup(*sections, R1, R2)
        self.add(Layout2)

        return Layout2

    def DrawLayout3(self):
        W=800       # mm
        Short_H=600 # mm
        Tall_H=1200 # mm
        L3_ORIGIN=ORIGIN+DOWN

        sections=[ # [BL, BR, TL, TR]
            Rectangle(
                width=W*U,
                height=Short_H*U,
                color=WHITE
            ).set_fill(GOLD_A, opacity=1),
            Rectangle(
                width=W*U,
                height=Short_H*U,
                color=WHITE
            ).set_fill(GOLD_A, opacity=1),
            Rectangle(
                width=W*U,
                height=Tall_H*U,
                color=WHITE
            ).set_fill(GOLD_A, opacity=1),
            Rectangle(
                width=W*U,
                height=Tall_H*U,
                color=WHITE
            ).set_fill(GOLD_A, opacity=1)
        ]

        # Moving sections into correct positions
        sections[0].shift(L3_ORIGIN + DOWN*(Short_H/2)*U + LEFT*(W/2)*U + RIGHT*(100)*U) # BL
        sections[1].shift(L3_ORIGIN + DOWN*(Short_H/2)*U + RIGHT*(W/2+100)*U) # BR
        sections[2].shift(L3_ORIGIN + UP*(Tall_H/2)*U + LEFT*(W/2+100)*U) #TL
        sections[3].shift(L3_ORIGIN + UP*(Tall_H/2)*U + RIGHT*(W/2)*U)

        # Manually setting coordinates of the outline of layout 3
        Layouts.L2and3_Positions=[
            [L3_ORIGIN[0],L3_ORIGIN[1],0],
            [L3_ORIGIN[0]-110*U,L3_ORIGIN[1],0],
            [L3_ORIGIN[0]-110*U,L3_ORIGIN[1]+Tall_H*U,0],
            [L3_ORIGIN[0]-110*U-W*U,L3_ORIGIN[1]+Tall_H*U,0],
            [L3_ORIGIN[0]-110*U-W*U,L3_ORIGIN[1],0],
            [L3_ORIGIN[0]-W*U+100*U,L3_ORIGIN[1],0],
            [L3_ORIGIN[0]-W*U+100*U,L3_ORIGIN[1]-Short_H*U,0],
            [L3_ORIGIN[0]+W*U+100*U,L3_ORIGIN[1]-Short_H*U,0],
            [L3_ORIGIN[0]+W*U+100*U,L3_ORIGIN[1],0],
            [L3_ORIGIN[0]+W*U,L3_ORIGIN[1],0],
            [L3_ORIGIN[0]+W*U,L3_ORIGIN[1]+Tall_H*U,0],
            [L3_ORIGIN[0],L3_ORIGIN[1]+Tall_H*U,0],
        ]
        
        # Rocks
        Layouts.R1Pos[2]=L3_ORIGIN + [(-W-110+Layouts.RockRad+50)*U,(Layouts.RockRad+50)*U,0]
        Layouts.R2Pos[2]=L3_ORIGIN + [W/2*U,Tall_H/2*U,0]
        R1=Circle(radius=Layouts.RockRad*U, color=GREY_D).set_fill(GREY_C, opacity=1)
        R2=Circle(radius=Layouts.RockRad*U, color=GREY_D).set_fill(GREY_C, opacity=1)
        R1.move_to(Layouts.R1Pos[2])
        R2.move_to(Layouts.R2Pos[2])
        
        Layout3=VGroup(*sections, R1, R2)
        self.add(Layout3)

        return Layout3

class Kobuki(Scene):
    Radius=175                  # mm
    current_angle=0             # in deg
    Kobuki_Y=np.array([0,0,0])  # direction of kobuki face (arrow)
    Kobuki_X=np.array([0,0,0])  # perpendicular to the right of the kobuki face (arrow)

    US_View=None                # Mobject for the shape of the ultrasonic sensor's (US) 'cone' view

    def setCurrAngle(angle):
        Kobuki.current_angle=angle

    def UpdateKobukiFaceDirections(angle): # angle in degrees
        angle_rad=angle*DEGREES
        Kobuki.Kobuki_Y=np.array([np.cos(angle_rad),np.sin(angle_rad),0])
        Kobuki.Kobuki_X=np.array([np.cos(PI/2-angle_rad),-np.sin(PI/2-angle_rad),0])

    def DrawUS(self, kobuki, draw):
        # From Ultrasonic Sensor Data Sheet MB1043 at 3.3V Graph C
        US_ConeView_Height=1500*U
        Kobuki.US_View_Position_List=[ # Coordinates for the outline of the US's 'cone' view
            kobuki.get_center(),
            kobuki.get_center()-Kobuki.Kobuki_X*50*U    +   Kobuki.Kobuki_Y*300*U,
            kobuki.get_center()-Kobuki.Kobuki_X*300*U   +   Kobuki.Kobuki_Y*900*U,
            kobuki.get_center()-Kobuki.Kobuki_X*300*U   +   Kobuki.Kobuki_Y*1200*U,
            kobuki.get_center()-Kobuki.Kobuki_X*200*U   +   Kobuki.Kobuki_Y*(US_ConeView_Height-50*U),
            kobuki.get_center()+Kobuki.Kobuki_X*0       +   Kobuki.Kobuki_Y*US_ConeView_Height,
            kobuki.get_center()+Kobuki.Kobuki_X*200*U   +   Kobuki.Kobuki_Y*(US_ConeView_Height-50*U),
            kobuki.get_center()+Kobuki.Kobuki_X*300*U   +   Kobuki.Kobuki_Y*1200*U,
            kobuki.get_center()+Kobuki.Kobuki_X*300*U   +   Kobuki.Kobuki_Y*900*U,
            kobuki.get_center()+Kobuki.Kobuki_X*50*U    +   Kobuki.Kobuki_Y*300*U
        ]

        # Creating a Polygon Mobject
        Kobuki.US_View=Polygon(*Kobuki.US_View_Position_List)
        Kobuki.US_View.set_fill(color=BLUE_B,opacity=0.1)

        if draw==True:
            self.add(Kobuki.US_View)

    def DrawKobuki(self, startPos, startAngle, drawUSView):
        # KOBUKI STARTS OFF FACING TO THE RIGHT (0 DEG)
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
        kobuki.rotate(startAngle*DEGREES)

        # Update Kobuki Axis
        Kobuki.setCurrAngle(startAngle)
        Kobuki.UpdateKobukiFaceDirections(startAngle)
    
        # Draw to Screen
        self.add(kobuki)

        # Draw Ultrasonic Sensor Cone
        if drawUSView==True:
            Kobuki.DrawUS(self,kobuki,drawUSView)

        return kobuki

    def Drive(self, kobuki, distance, speed, my_run_time=None):
        my_run_time=abs(distance)/speed if my_run_time==None else my_run_time
        self.play(
            kobuki.animate.shift(distance*Kobuki.Kobuki_Y),
            Kobuki.US_View.animate.shift(distance*Kobuki.Kobuki_Y),
            run_time=my_run_time,
            rate_func=linear
        )
    
    def Rotate(self, kobuki, angle, speed, my_run_time=None):
        Kobuki.current_angle=(Kobuki.current_angle+angle)%360 # Keeps angle within 0 => 360
        Kobuki.UpdateKobukiFaceDirections(Kobuki.current_angle) # Update the relative X,Y kobuki face direction coordinates
        if angle>180: angle =- (360-angle) # Take shortest rotation

        if my_run_time==None: my_run_time=abs(angle)/speed
        self.play(
            Rotate(
                kobuki, 
                angle*DEGREES,
                run_time=my_run_time,
                rate_func=linear
            ),
            Rotate(
                Kobuki.US_View, 
                angle*DEGREES,
                about_point=kobuki.get_center(),
                run_time=my_run_time,
                rate_func=linear
            )
        )

    def UpdateDetection(layout_num):
        detectRock1=PointInsidePolygon.point_inside_polygon(
            Layouts.R1Pos[layout_num][0],
            Layouts.R1Pos[layout_num][1],
            Kobuki.US_View.get_all_points()
        )
        detectRock2=PointInsidePolygon.point_inside_polygon(
            Layouts.R2Pos[layout_num][0],
            Layouts.R2Pos[layout_num][1],
            Kobuki.US_View.get_all_points()
        )

        if detectRock1 : 
            distance=(
                math.dist(
                    Layouts.R1Pos[layout_num],
                    MarsRoverNavigation.rover.get_center()
                ) - (Kobuki.Radius + Layouts.RockRad)*U
            )/U # distance in mm
            return True, distance
        elif detectRock2 : 
            distance=(
                math.dist(
                    Layouts.R2Pos[layout_num],
                    MarsRoverNavigation.rover.get_center()
                ) - (Kobuki.Radius + Layouts.RockRad)*U
            )/U # distance in mm
            return True, distance
        else: return False, 0

    def UpdateBumper(layout_num):     
        dist_kobuki_r1=math.dist( #distance from kobuki to rock 1
            MarsRoverNavigation.rover.get_center(),
            Layouts.R1Pos[layout_num]
        )
        dist_kobuki_r2=math.dist( #distance from kobuki to rock 2
            MarsRoverNavigation.rover.get_center(),
            Layouts.R2Pos[layout_num]
        )

        ERROR=20*U
        if dist_kobuki_r1 <= (Kobuki.Radius+Layouts.RockRad+ERROR)*U:
            MarsRoverNavigation.mission[0]=True
            return True
        elif dist_kobuki_r2 <= (Kobuki.Radius+Layouts.RockRad+ERROR)*U:
            MarsRoverNavigation.mission[1]=True
            return True
        else: 
            return False

    def UpdateCliff(layout_num, self=None):
        cliff=False
        if layout_num==0:
            for angle in range(-20,20,10):
                theta=angle*PI/180
                layout_points=Layouts.L1_Positions
                pt=[
                    MarsRoverNavigation.rover.get_center()[0] + Kobuki.Kobuki_X[0]*(Kobuki.Radius+20)*U*np.cos(theta),
                    MarsRoverNavigation.rover.get_center()[1] + Kobuki.Kobuki_Y[1]*(Kobuki.Radius+20)*U*np.sin(theta),
                    0
                ]
                if not PointInsidePolygon.point_inside_polygon(pt[0],pt[1],layout_points):
                    cliff=True
                    break
        elif layout_num==1 or layout_num==2:
            for angle in range(-20,20,10):
                beta=np.arctan(Kobuki.Kobuki_Y[1]/Kobuki.Kobuki_Y[0])
                theta=angle*PI/180+beta
                layout_points=Layouts.L2and3_Positions
                pt=[
                    MarsRoverNavigation.rover.get_center()[0] + (Kobuki.Radius)*U*np.sin(theta),
                    MarsRoverNavigation.rover.get_center()[1] + (Kobuki.Radius)*U*np.cos(theta),
                    0
                ]
                if not PointInsidePolygon.point_inside_polygon(pt[0],pt[1],layout_points):
                    cliff=True
        return cliff

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

# ==== MANIM SET-UP CLASSES AND FUNCTIONS ====


# ==== ALGORITHM AND FSM ==== 

class State(Enum):
    IDLE        = 0
    SEARCH      = 1
    SEARCH_R1   = 2
    SEARCH_R2   = 3
    OBJECT      = 4
    OBSTACLE    = 5
    AVOID       = 6

class MarsRoverNavigation(Scene):
    rover=Circle()
    mission=[False,False] # mission=[collect rock 1, collect rock 2]

    def SetTest1(self):
        Layout1 = Layouts.DrawLayout1(self)
        roverStartPos=[
            U*(-800+225+Kobuki.Radius),
            U*(-H/2+Kobuki.Radius),
            0
        ]
        roverStartAngle=90

        # Draw the Kobuki
        MarsRoverNavigation.rover=Kobuki.DrawKobuki(self,roverStartPos,roverStartAngle,True)
        return Layout1, 0 # 0 ==> layout_num

    def SetTest2(self):
        Layout2 = Layouts.DrawLayout2(self)
        roverStartPos=[
            U*(-800+100+225+Kobuki.Radius),
            U*(-H/2+Kobuki.Radius),
            0
        ]
        roverStartAngle=0

        # Draw the Kobuki
        MarsRoverNavigation.rover=Kobuki.DrawKobuki(self,roverStartPos,roverStartAngle,True)
        return Layout2, 1 # 1 ==> layout_num

    def SetTest3(self):
        Layout3, W = Layouts.DrawLayout3(self)
        roverStartPos=[
            U*(-800+225+Kobuki.Radius),
            U*(-H/2+Kobuki.Radius),
            0
        ]
        roverStartAngle=random.randrange(0,360)

        # Draw the Kobuki
        MarsRoverNavigation.rover=Kobuki.DrawKobuki(self,roverStartPos,roverStartAngle,True)
        return Layout3, 2 # 1 ==> layout_num

    def viewLayout2(self):
        layout, layout_num=MarsRoverNavigation.SetTest2(self)
        # View the polygon formed by layout.get_all_points()
        # self.remove(layout)
        # for section in range(len(Layouts.L2and3_Positions)):
        #     self.add(Polygon(*Layouts.L2and3_Positions[section]))
        pass

    def viewLayout3(self):
        layout, layout_num=MarsRoverNavigation.SetTest3(self)
        self.play(FadeOut(layout), FadeIn(Polygon(*Layouts.L2and3_Positions)))
        # cliff=Kobuki.UpdateCliff(layout_num, self)
        # print(cliff)
        # Kobuki.Drive(self,MarsRoverNavigation.rover,500*U,DRIVE_SPEED)
        # cliff=Kobuki.UpdateCliff(layout_num, self)
        # print(cliff)
        # self.wait(2)
        pass

    def updateUS_View(self, detected):
        if detected==True:
            Kobuki.US_View.set_color(RED).set_fill(color=RED,opacity=0.5)
        else:
            Kobuki.US_View.set_color(BLUE).set_fill(color=BLUE_B,opacity=0.3)

    def MissionCompleted(self, layout):
        self.play(FadeOut(Kobuki.US_View),FadeOut(MarsRoverNavigation.rover),FadeOut(layout))
        self.play(FadeIn(Text("Mission Completed")))
        self.wait(2)

    def testAlgorithm(self):
        # Init stuff
        layout, layout_num=MarsRoverNavigation.SetTest1(self)
        DIR=CCW
        state=State.SEARCH_R1
        layout3=False
        detectObjectCounter=0
        objectRanges=[0,0]
        objectAngles=[0,0]

        WHILE_ESCAPE_COUNTER=300
        while (MarsRoverNavigation.mission != [True, True]) and WHILE_ESCAPE_COUNTER>0:
            WHILE_ESCAPE_COUNTER-=1

            # Update sensors
            detected, dist=Kobuki.UpdateDetection(layout_num)
            bumper=Kobuki.UpdateBumper(layout_num)
            cliff=Kobuki.UpdateCliff(layout_num)
            MarsRoverNavigation.updateUS_View(self, detected)
            
            output.write(str(state)+"\n")
            output.write("\tdetected: "+str(detected)+"\n")
            output.write("\tbumper: "+str(bumper)+"\n")
            output.write("\tcliff: "+str(cliff)+"\n")

            # FSM
            match state:
                case State.IDLE:
                    self.wait(2)

                case State.SEARCH_R1:
                    if detected:
                        output.write("\tDIST:"+str(dist)+"\n")
                        if not (int(objectRanges[0])==int(dist)):
                            objectRanges[1]=objectRanges[0]
                            objectRanges[0]=dist
                            objectAngles[1]=objectAngles[0]
                            objectAngles[0]=-11 if CCW else 11
                            detectObjectCounter+=1
                        if (detectObjectCounter%2 == 0):
                            state = State.OBJECT
                            if (objectRanges[0]<objectRanges[1]):
                                Kobuki.Rotate(self,MarsRoverNavigation.rover,objectAngles[0]*-DIR+11*-DIR,ROTATE_SPEED,0.5)
                                objectAngles[1]+=objectAngles[0]*-DIR+11*-DIR
                            else:
                                Kobuki.Rotate(self,MarsRoverNavigation.rover,objectAngles[1]*-DIR+11*-DIR,ROTATE_SPEED,0.5)
                                objectAngles[0]+=objectAngles[1]*-DIR+11*-DIR

                    elif bumper or cliff:
                        state=State.OBJECT

                    if (not detected or (detectObjectCounter%2 != 0)) and not bumper:
                        Kobuki.Rotate(self,MarsRoverNavigation.rover,2*DIR,ROTATE_SPEED,0.01)
                        objectAngles[0]+=2*DIR
                    
                case State.SEARCH_R2:
                    angle=0
                    if detected:
                        state=State.OBJECT
                        angle=11
                        Kobuki.Rotate(self,MarsRoverNavigation.rover,angle*DIR,ROTATE_SPEED,0.5)
                    elif not detected and not bumper:
                        angle=2
                        Kobuki.Rotate(self,MarsRoverNavigation.rover,angle*DIR,ROTATE_SPEED,0.01)

                    if (objectRanges[0]<objectRanges[1]):
                        objectAngles[1]+=angle
                    else:
                        objectAngles[0]+=angle

                case State.OBJECT:
                    if bumper or cliff:
                        state=State.OBSTACLE
                    elif detected:
                        mm=0
                        step=20
                        while mm < dist:
                            mm+=step
                            # Update sensors
                            bumper=Kobuki.UpdateBumper(layout_num)
                            cliff=Kobuki.UpdateCliff(layout_num)

                            if bumper or cliff:
                                state=State.OBSTACLE
                                if cliff and MarsRoverNavigation.mission[0]==True:
                                    layout3=True
                                break
                            Kobuki.Drive(self,MarsRoverNavigation.rover,step*U,DRIVE_SPEED,0.01)
                    else:
                        state=State.SEARCH_R2

                case State.OBSTACLE:
                    if not (bumper or cliff):
                        state=State.AVOID
                    else:
                        Kobuki.Drive(self,MarsRoverNavigation.rover,-50*U,DRIVE_SPEED)

                case State.AVOID:
                    #DIR = CW if DIR==CCW else CCW
                    Kobuki.Rotate(self,MarsRoverNavigation.rover,11*DIR,ROTATE_SPEED,0.5)
                    objectAngles[0]+=11*DIR
                    objectAngles[1]+=11*DIR
                    if (MarsRoverNavigation.mission[0]!=True):
                        state=State.SEARCH_R1
                    else:
                        if (layout3==True):
                            Kobuki.Rotate(self,MarsRoverNavigation.rover,100*CW,ROTATE_SPEED)
                            Kobuki.Drive(self,MarsRoverNavigation.rover,500*U,DRIVE_SPEED)
                            Kobuki.Rotate(self,MarsRoverNavigation.rover,90*CCW,ROTATE_SPEED)
                            Kobuki.Drive(self,MarsRoverNavigation.rover,500*U,DRIVE_SPEED)
                            DIR=CCW
                            state=State.SEARCH_R2
                        else:
                            DIR = CW if DIR==CCW else CCW
                            state=State.SEARCH_R2
                            if (objectRanges[0]<objectRanges[1]):
                                Kobuki.Rotate(self,MarsRoverNavigation.rover,objectAngles[1]*DIR,ROTATE_SPEED,0.5)
                                objectAngles[0]+=objectAngles[1]*DIR
                            else:
                                Kobuki.Rotate(self,MarsRoverNavigation.rover,objectAngles[0]*DIR,ROTATE_SPEED,0.5)
                                objectAngles[1]+=objectAngles[0]*DIR
        
        if (WHILE_ESCAPE_COUNTER<=0): output.write("ESCAPED WHILE LOOP")
        if (MarsRoverNavigation.mission == [True, True]): MarsRoverNavigation.MissionCompleted(self,layout)
        output.close()

    def construct(self):
        MarsRoverNavigation.testAlgorithm(self)
        #MarsRoverNavigation.viewLayout3(self)

# ==== ALGORITHM AND FSM ====