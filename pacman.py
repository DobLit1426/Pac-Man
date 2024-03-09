from graphics_and_games_klassen import *

class PacMan(Figur):
    movement_vector_x = 0
    movement_vector_y = 0
    movement_step = 0
    radius = 0
    distance_since_toggling_mouth = 0
    _max_distance_since_toggling_mouth = 15
    is_mouth_open: bool = True
    
    def __init__(self, x: int = 0, y: int = 0, angle: int = 0, size: int = 50, step: int = 1):
        super().__init__(x=x, y=y, winkel=angle, groesse=size, sichtbar=True)
        self.movement_step = step
        self.radius = size / 2
        
        if self.is_mouth_open:
            self._draw_pac_with_open_mouth()
        else:
            self._draw_pac_with_closed_mouth()
            
    def _draw_pac_with_open_mouth(self):
        size = self.radius * 2
        
        self.FigurteilFestlegenEllipse(x=-size,y=-size, breite=size * 2, hoehe=size * 2, farbe="gelb") # Skin
        self.FigurteilFestlegenDreieck(x1=0, y1=0, x2=size * 0.95, y2=-0.2*size, x3=size * 0.95, y3=0.3*size, farbe="schwarz") # Mouth
        
    def _draw_pac_with_closed_mouth(self):
        size = self.radius * 2
        
        self.FigurteilFestlegenEllipse(x=-size,y=-size, breite=size * 2, hoehe=size * 2, farbe="gelb") # Skin
        self.FigurteilFestlegenDreieck(x1=0, y1=0, x2=size * 0.99, y2=-0.05*size, x3=size * 0.99, y3=0.05*size, farbe="schwarz") # Mouth
    
    def open_mouth(self):
        if not self.is_mouth_open:
            angle = self.winkel
            
            self.EigeneFigurLoeschen()
            self._draw_pac_with_open_mouth()
            self.WinkelSetzen(winkel=angle)
        else: print("Warning: Mouth is already open, no need to open it again!")
        
    def close_mouth(self):
        if self.is_mouth_open:
            angle = self.winkel
            
            self.EigeneFigurLoeschen()
            self._draw_pac_with_closed_mouth()
            self.WinkelSetzen(winkel=angle)
        else: print("Warning: Mouth is already closed, no need to close it again!")
    
    def toggle_mouth_if_needed_or_update_counter(self, distance: int):
        if self.distance_since_toggling_mouth > self._max_distance_since_toggling_mouth:
            self.distance_since_toggling_mouth = 0
            self.is_mouth_open = not self.is_mouth_open
            if self.is_mouth_open:
                self.close_mouth() # Open mouth if it's closed
            else:
                self.open_mouth() # Close mouth if it's open
        else:
            self.distance_since_toggling_mouth += distance
    
    def moveUp(self, length: int = 10):
        self.WinkelSetzen(90)
        self.move(length)
        self.toggle_mouth_if_needed_or_update_counter(distance=length)
        
    def moveDown(self, length: int = 10):
        self.WinkelSetzen(270)
        self.move(length)
        self.toggle_mouth_if_needed_or_update_counter(distance=length)
        
    def moveRight(self, length: int = 10):
        self.WinkelSetzen(0)
        self.move(length)
        self.toggle_mouth_if_needed_or_update_counter(distance=length)
        
    def moveLeft(self, length: int = 10):
        self.WinkelSetzen(180)
        self.move(length)
        self.toggle_mouth_if_needed_or_update_counter(distance=length)
        
    def stop(self):
        self.movement_vector_x = 0
        self.movement_vector_y = 0
        
    def move(self, x: int, y: int):
        new_x = self.x + x
        new_y = self.y + y
        
        self.PositionSetzen(new_x, new_y)
    
    def place(self, x: int, y: int):
        self.PositionSetzen(x=x, y=y)
        
    def move_according_to_vector(self):
        self.move(x=self.movement_vector_x, y=self.movement_vector_y)
        self.toggle_mouth_if_needed_or_update_counter(distance=abs(self.movement_vector_x) + abs(self.movement_vector_y))
#         self.move(abs(self.movement_vector_x) + abs(self.movement_vector_y))
        
    def change_movement_vector_to_left(self):
        self.movement_vector_x = -self.movement_step
        self.movement_vector_y = 0
        
        self.WinkelSetzen(180) # Turn to the left
    
    def change_movement_vector_to_right(self):
        self.movement_vector_x = self.movement_step
        self.movement_vector_y = 0
        
        self.WinkelSetzen(0) # Turn to the right
        
    def change_movement_vector_to_up(self):
        self.movement_vector_x = 0
        self.movement_vector_y = -self.movement_step
        
        self.WinkelSetzen(90) # Turn upwards
        
    def change_movement_vector_to_down(self):
        self.movement_vector_x = 0
        self.movement_vector_y = self.movement_step
        
        self.WinkelSetzen(270) # Turn downwards
        
    def is_static(self):
        return self.movement_vector_x and self.movement_vector_y