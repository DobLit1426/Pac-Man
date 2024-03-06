# -*- coding: utf-8 -*-

"""

Created on Wed May  17 17:53:04 2020



@author: Klaus Reinold
It is time to write somethnig completely uninteresting while I am waiting for my Kurzarbeit to arrive. It's a very long text and I am typing using Blind Typing System, which helps me use 90% of my possibilites of typing with 10 fingers. I do it cause I have to waste time to survive another Informatik lesson (no offences here). As I write, nothing interesting happens, so I just type more LOL.

"""





from graphics_and_games_klassen import *
from time import sleep






class HausbauTurtle(Turtle):

    """

    'Bessere' Turtle, die ein Haus zeichnen kann.

    """




    def QuadratZeichnen(self):

        """

        Zeichnet ein Quadrat mit Seitenlänge 50

        """     

        self.Gehen(100)

        self.Drehen(90)

        self.Gehen(50)

        self.Drehen(90)

        self.Gehen(100)

        self.Drehen(90)

        self.Gehen(50)

        self.Drehen(90)

    





    def DreieckZeichnen(self, s):

        """

        Zeichnet ein gleichseitiges Dreieck mit beliebiger Größe

        -- Parameter s Seitenlänge

        """

        self.FarbeSetzen("rot")

        self.Gehen(s)

        self.Drehen(120)

        self.Gehen(s)

        self.Drehen(120)

        self.Gehen(s)

        self.Drehen(120)

    

    

    def HausZeichnen(self):

        """

        Baut ein Haus aus einem Quadrat und einem Dreieck

        """ 

        self.FarbeSetzen("schwarz")

        self.QuadratZeichnen()

        self.Drehen(90)

        self.Gehen(50)

        self.Drehen(-90)

        self.DreieckZeichnen(100)

        

#turtle = HausbauTurtle()

#turtle.HausZeichnen()

m = Figur(groesse=100)
m.FigurteilFestlegenEllipse(x=-50, y=-50, breite=100, hoehe=100, farbe="gelb")

