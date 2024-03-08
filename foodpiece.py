from graphics_and_games_klassen import *

class FoodPiece(Kreis):
    position_x = 0
    position_y = 0
    is_super = False
    
    def __init__(self, x=60, y=60, is_super=False, visible=True):
        self.is_super = is_super
        
        if is_super:
            radius = 4
        else:
            radius = 2
        
        super().__init__(x=x, y=y, radius=radius, winkel=0, farbe="schwarz", sichtbar=visible)
    
    def aten(self):
        """Makes the food piece disappear
        """
        self.SichtbarkeitSetzen(False)
    
    def is_aten(self) -> bool:
        return not self.sichtbar