# -*- coding: utf-8 -*-
"""
Beispiel zur Nutzung von Graphics and Games for Python am Mac
"""

from graphics_and_games_klassen import Turtle
from intern.zeichenfenster import Zeichenfenster

schnecke = Turtle()
schnecke.Gehen(100)
schnecke.Drehen(90) 
schnecke.Gehen(100)
schnecke.Drehen(90) 
schnecke.Gehen(100)
schnecke.Drehen(90) 
schnecke.Gehen(100)
schnecke.Drehen(90) 
Zeichenfenster().run()