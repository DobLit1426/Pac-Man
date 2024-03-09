from graphics_and_games_klassen import *
from intern.zeichenfenster import Zeichenfenster

class Ghost(Figur):
    def __init__(self, farbe: str = "rot", x=0, y=0, angle=0, size=50, visible=True):
        super().__init__(x=x, y=y, winkel=angle, groesse=size, sichtbar=visible)
        
        self.FigurteilFestlegenEllipse(x=-size,y=-size, breite=size * 2, hoehe=size * 2, farbe=farbe) # Skin (circle base)
        self.FigurteilFestlegenRechteck(x=-size, y=0, breite=size*2, hoehe=size, farbe=farbe) # Skin 2 (rectangle)
        
        # 3 rectangles to show legs
        # self.FigurteilFestlegenEllipse(x=-size, y=2/3 * size, breite=8/15 * size, hoehe=2/3 * size, farbe=WEISS)
        # self.FigurteilFestlegenRechteck(x=-7/9 * size, y=2/3 * size, breite=2/9 * size, hoehe=1/3 * size, farbe=farbe)
        
        # Eyes
        eyes_d = 8/15 * size
        left_eye_x = -9/15 * size
        right_eye_x = 1/15 * size
        eyes_y = -2/3 * size # = -10/15 * size
        
        self.FigurteilFestlegenEllipse(x=left_eye_x, y=eyes_y, breite=eyes_d, hoehe=eyes_d, farbe=WEISS)
        self.FigurteilFestlegenEllipse(x=right_eye_x, y=eyes_y, breite=eyes_d, hoehe=eyes_d, farbe=WEISS)
        
        # Eyes' pupils (looks to left)
        pupils_d = eyes_d / 2
        pupils_y = -7/15 * size
        self.FigurteilFestlegenEllipse(x=left_eye_x, y=pupils_y, breite=pupils_d, hoehe=pupils_d, farbe=SCHWARZ)
        self.FigurteilFestlegenEllipse(x=right_eye_x, y=pupils_y, breite=pupils_d, hoehe=pupils_d, farbe=SCHWARZ)
        
        # self.FigurteilFestlegenDreieck(x1=size*15/50, y1=0, x2=size, y2=-0.1*size, x3=size, y3=0.1*size, farbe="schwarz")

    def move(self, x: int, y: int):
        new_x = self.x + x
        new_y = self.y + y
        
        self.PositionSetzen(new_x, new_y)
    
    def place(self, x: int, y: int):
        self.PositionSetzen(x=x, y=y)
        
        
# ghost = Ghost(farbe="rot", x=100, y=100, angle=0, size=50, visible=True)

# Zeichenfenster().run()