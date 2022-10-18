from manim import *

class KobukiMovement(Scene):
    def construct(self):
        plane = NumberPlane()
        #self.add(plane)

        # Height of layout. Use 6 for animation
        # Actual height is 2180 mm
        # Therefore unit to convert from mm to munit is U
        H=1800
        U=6/H

        # LAYOUTS
        # L1 W:1810 mm, H:2180 mm
        # W=H*(W/H)
        W=1600
        layout=[
            Rectangle(width=W*U,height=H*U,color=WHITE).set_fill(GOLD_A, opacity=1)
        ]
        self.add(layout[0])
        self.add(Line([U*(-W/2),U*(-H/2+600),0],[U*(W/2),U*(-H/2+600),0]), Line([0,U*(H/2),0],[0,U*(-H/2),0]))

        # ROCKS
        R1Pos=[[U*(-W/2+80),U*(-H/2+680),0],[0,0,0],[0,0,0]]
        R2Pos=[[0,0,0],[0,0,0],[0,0,0]]
            # Assumed radius in mm
        R1Rad=40
        R1=Circle(radius=R1Rad*U, color=GREY_D).set_fill(GREY_C, opacity=1)
        R1.move_to(R1Pos[0])
        self.add(R1)

        # R:175 mm
        R=350/2
        kobuki=Circle(radius=R*U,color=GREY_E)
        kobuki.set_fill(GREY_C, opacity=1)
        kobuki.move_to([U*(-W/2+225+R),U*(-H/2+R),0])
        self.add(kobuki)
        kobuki_startPos=kobuki.get_center()

        # Move up to R1
        self.play(kobuki.animate.move_to([kobuki.get_center()[0],R1Pos[0][1],0]),run_time=2)
        # Move across to R1
        self.play(kobuki.animate.move_to([R1Pos[0][0]+R1Rad*U+R*U,kobuki.get_center()[1],0]),run_time=2)
        self.play(kobuki.animate.move_to(kobuki_startPos))
        self.play(kobuki.animate.move_to(R1Pos[0]), run_time=2)
