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
CLIFF_SHOW      = True
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
        #if angle>180: angle =- (360-angle) # Take shortest rotation
        MarsRoverNavigation.DIR = CCW if angle > 0 else CW
        Kobuki.current_angle=(Kobuki.current_angle+angle)%360 # Keeps angle within 0 => 360
        Kobuki.UpdateKobukiFaceDirections(Kobuki.current_angle) # Update the relative X,Y kobuki face direction coordinates

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

    def UpdateDetection(layout_num, self):
        detected=False
        distance=0
        
        # Detection Conditions for Ultrasonic Sensor
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

        # if detectRock 1 and Rock 1 not yet collected
        if detectRock1 and MarsRoverNavigation.mission[0]==False: 
            distance=( # Distance from edge of kobuki to edge of rock
                math.dist(
                    Layouts.R1Pos[layout_num],
                    MarsRoverNavigation.rover.get_center()
                )-(Kobuki.Radius+Layouts.RockRad)*U)/U # distance in mm
            detected = True
        elif detectRock2 : 
            distance=(
                math.dist(
                    Layouts.R2Pos[layout_num],
                    MarsRoverNavigation.rover.get_center()
                )-(Kobuki.Radius+Layouts.RockRad)*U)/U # distance in mm
            detected = True
        
        output.write("\tdetected: \t"+str(detected)+"\n") # Debugging Log
        output.write("\trange: \t\t"+str(distance)+"\n") # Debugging Log
        
        MarsRoverNavigation.updateUS_View(self, detected) # Update the ultrasonic sensor view 
        
        return detected, distance

    def UpdateBumper(layout_num, self):     
        bumper = False

        dist_kobuki_r1=math.dist( #distance from kobuki to rock 1
            MarsRoverNavigation.rover.get_center(),
            Layouts.R1Pos[layout_num]
        )
        dist_kobuki_r2=math.dist( #distance from kobuki to rock 2
            MarsRoverNavigation.rover.get_center(),
            Layouts.R2Pos[layout_num]
        )

        # Rock Collection Conditions
        ERROR=20*U # To stop the kobuki and rock overlapping 
        if dist_kobuki_r1 <= (Kobuki.Radius+Layouts.RockRad+ERROR)*U:
            bumper = True
        elif dist_kobuki_r2 <= (Kobuki.Radius+Layouts.RockRad+ERROR)*U:
            bumper = True
        else: 
            bumper = False

        output.write("\tbumper: \t"+str(bumper)+"\n")
        if bumper:
            MarsRoverNavigation.bumper.set_color(RED)
        else:
            MarsRoverNavigation.bumper.set_color(WHITE)

        return bumper

    def UpdateCliff(layout_num, self):
        cliff=False
        if layout_num==0:
            layout_points=Layouts.L1_Positions  
        else:
            layout_points=Layouts.L2and3_Positions
        # Check for cliff at points around the face of the kobuki (the arrow)
        for angle in range(-20,20+10,10):     
            pt=[
                MarsRoverNavigation.rover.get_center()[0] + (Kobuki.Radius)*U*np.cos((angle+Kobuki.current_angle)*DEGREES),
                MarsRoverNavigation.rover.get_center()[1] + (Kobuki.Radius)*U*np.cos((angle+Kobuki.current_angle)*DEGREES),
                0
            ]
            if not PointInsidePolygon.point_inside_polygon(pt[0],pt[1],layout_points): cliff=True

        if cliff:
            MarsRoverNavigation.cliff.set_color(GREEN)
        else:
            MarsRoverNavigation.cliff.set_color(WHITE)

        output.write("\tcliff: \t\t"+str(cliff)+"\n\n")
        return cliff

class PointInsidePolygon(Scene):    
    def construct(self): # Visual for testing the point inside polygon function
        size=1
        poly_points=[
            [-size,size,0],
            [size,size,0],
            [size,-size,0],
            [-size,-size,0]
        ]

        poly=Polygon(*poly_points)
        self.add(poly)

        for dot in range(20):
            d_coord=[
                random.uniform(-(size+2),size+2),
                random.uniform(-(size+2),size+2),
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
    SEARCH      = 0
    OBJECT      = 1
    OBSTACLE    = 2

class MarsRoverNavigation(Scene):
    rover=None
    mission=[False,False] # mission=[collect rock 1, collect rock 2]
    DIR = CCW
    bumper=None
    cliff=None
    # Cliff sensor points
    d=[
        Dot(color=BLUE),
        Dot(color=BLUE),
        Dot(color=BLUE),
        Dot(color=BLUE),
        Dot(color=BLUE)
    ]

    # Manim-specific functions
    def SetTest1(self):
        Layout1 = Layouts.DrawLayout1(self)
        roverStartPos=[
            U*(-800+225+Kobuki.Radius),
            U*(-H/2+Kobuki.Radius),
            0
        ]
        roverStartAngle=90
        
        MarsRoverNavigation.rover=Kobuki.DrawKobuki(self,roverStartPos,roverStartAngle,True)
        return Layout1, 0 # layout_num

    def SetTest2(self):
        Layout2 = Layouts.DrawLayout2(self)
        roverStartPos=[
            U*(-800+100+225+Kobuki.Radius),
            U*(-H/2+Kobuki.Radius),
            0
        ]
        roverStartAngle=0

        MarsRoverNavigation.rover=Kobuki.DrawKobuki(self,roverStartPos,roverStartAngle,True)
        return Layout2, 1 # layout_num

    def SetTest3(self):
        Layout3 = Layouts.DrawLayout3(self)
        roverStartPos=[
            U*(-800+225+Kobuki.Radius),
            U*(-H/2+Kobuki.Radius),
            0
        ]
        roverStartAngle=random.randrange(0,360)

        MarsRoverNavigation.rover=Kobuki.DrawKobuki(self,roverStartPos,roverStartAngle,True)
        return Layout3, 2 # layout_num

    def viewLayout2(self):
        layout, layout_num=MarsRoverNavigation.SetTest2(self)

    def viewLayout3(self):
        layout, layout_num=MarsRoverNavigation.SetTest3(self)
        self.play(FadeOut(layout), FadeIn(Polygon(*Layouts.L2and3_Positions)))

    def updateUS_View(self, detected):
        if detected==True: Kobuki.US_View.set_color(RED).set_fill(color=RED,opacity=0.5)
        else: Kobuki.US_View.set_color(BLUE).set_fill(color=BLUE_B,opacity=0.3)

    def MissionCompleted(self, layout):
        self.play(FadeOut(Kobuki.US_View),FadeOut(MarsRoverNavigation.rover),FadeOut(layout))
        self.play(FadeIn(Text("Mission Completed")))
        self.wait(2)

    def updateState(state, newState):
        output.write(UPurple+str(newState)+"\n"+Color_Off) # Debug log    
        return newState

    def driveWithSensor(self, layout_num, distance_to_rock, step): # distance_to_rock in mm
        for _ in range(0,int(distance_to_rock),step):
            bumper=Kobuki.UpdateBumper(layout_num, self)
            cliff=Kobuki.UpdateCliff(layout_num, self)
            MarsRoverNavigation.drawCliffSensorPoints(self, CLIFF_SHOW)
            _, dist  = Kobuki.UpdateDetection(layout_num, self)

            if bumper or cliff:
                return bumper, cliff
            Kobuki.Drive(self,MarsRoverNavigation.rover,step*U,DRIVE_SPEED,0.01)
        return 0,0

    def drawCliffSensorPoints(self, draw):
        if draw:
            for angle in range(-20,20+10,10):     
                pt=[
                    MarsRoverNavigation.rover.get_center()[0] + (Kobuki.Radius)*U*np.cos((angle+Kobuki.current_angle)*DEGREES),
                    MarsRoverNavigation.rover.get_center()[1] + (Kobuki.Radius)*U*np.sin((angle+Kobuki.current_angle)*DEGREES),
                    0
                ]
                i=int(abs(-20-angle)/10)
                MarsRoverNavigation.d[i].move_to(pt)


    # The actual algorithm
    def testAlgorithm(self, layout_num):     
        state=None
        state=MarsRoverNavigation.updateState(state,State.SEARCH)

        WHILE_ESCAPE_COUNTER=600
        while (MarsRoverNavigation.mission != [True, True]) and WHILE_ESCAPE_COUNTER>0:
            WHILE_ESCAPE_COUNTER-=1

            # Update sensors
            detected, dist  = Kobuki.UpdateDetection(layout_num, self)
            bumper          = Kobuki.UpdateBumper   (layout_num, self)
            cliff           = Kobuki.UpdateCliff    (layout_num, self)

            # FSM
            match state:
                case State.SEARCH:
                    pass
                      
                case State.OBJECT:
                    pass

                case State.OBSTACLE:
                    pass

    # What is called when you run "manim MCP_A3.py MarsRoverNavigation"
    def construct(self):
        # VISUALS FOR SENSORS
        # Bumper Sensor Triggered Visual
        MarsRoverNavigation.bumper=Dot(UP*3+LEFT*6, color=WHITE)
        self.add(MarsRoverNavigation.bumper)

        # Cliff Sensor Triggered Visual
        MarsRoverNavigation.cliff=Dot(UP*2+LEFT*6, color=WHITE)
        self.add(MarsRoverNavigation.cliff)

        if CLIFF_SHOW: self.add(*MarsRoverNavigation.d)

        # ==== CHOOSE LAYOUT ====
        layout, layout_num=MarsRoverNavigation.SetTest1(self)
        # ==== CHOOSE LAYOUT ====

        MarsRoverNavigation.testAlgorithm(self, layout_num)
        
        if (MarsRoverNavigation.mission == [True, True]): 
            MarsRoverNavigation.MissionCompleted(self,layout)
            output.write(Green+"Mission Successful\n"+Color_Off)
        else: 
            output.write(Red+"ESCAPED WHILE LOOP\n"+Color_Off)
        
        output.close()

# ==== ALGORITHM AND FSM ====