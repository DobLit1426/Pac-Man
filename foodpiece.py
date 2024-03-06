from graphics_and_games_klassen import *

class FoodPiece(Kreis):
    position_x = 0
    position_y = 0
    
    def __init__(self, x=60, y=60, radius=2, visible=True):
        super().__init__(x=x, y=y, radius=radius, winkel=0, farbe="schwarz", sichtbar=visible)
    
    def aten(self):
        """Makes the food piece disappear
        """
        self.SichtbarkeitSetzen(False)