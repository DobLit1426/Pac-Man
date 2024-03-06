"""
Author: Dobromir Litvinov
"""

from time import sleep
from graphics_and_games_klassen import *
from intern.zeichenfenster import Zeichenfenster
import keyboard
from random import randint
from labytinth import Labyrinth
from intern.zeichenfenster import Zeichenfenster
from pacman import PacMan
from foodpiece import FoodPiece

# Define some constraints
#  - Pac-Man start position
# pac_start_x = 100
# pac_start_y = 100
#  - Pac-Man color
pac_start_color = "gelb"
#  - Pac-Man radius
pac_radius = 15
#  - Pac-Man waiting time
waiting_time = 0.005
#  - Pac-Man step size
pac_step = 1
#  - Walls and scene
ratio_between_cell_length_and_pac_radius = 0.15
wall_length = pac_radius * (2 + ratio_between_cell_length_and_pac_radius)
walls_number_vertical = 16 # Must be higher than 10!!!
walls_number_horizontal = 23 # Must be higher than 10!!!
wall_color = "schwarz"
scene_width = wall_length * walls_number_horizontal
scene_height = wall_length * walls_number_vertical
#  - Walls - Logic: First, the whole labyrinth is filled with wall "Einheiten" (squares with side wall_length). Then a "tractor" will clean the labyrinth unless all even blocks () are clear
#  - Scene
scene_x = 20
scene_y = 20
scene_color = "weiss"
# Others
game_running = True
points_for_eating_dot = 10

# Function to convert matrix (of walls_map) coordinates to regular ones
def get_wall_middle_in_regular_coordinates(wall_x: int, wall_y: int) -> list:
    """Takes matrix cordinates (e.g. x=3, y=7) of a wall and converts them to the normal coordinates that are at the walls middle

    Args:
        wall_x (int): matrix x coordinate
        wall_y (int): matrix y coordinate

    Returns:
        list: coordinates in format [x, y]
    """
    global wall_length, scene_x, scene_y
    
    regular_x = scene_x + (wall_x + 0.5) * wall_length
    regular_y = scene_y + (wall_y + 0.5) * wall_length
    
    return [regular_x, regular_y]

# Define functions to change moving vector
def left_arrow_pressed():
    global game_running, pac, wall_length, ratio_between_cell_length_and_pac_radius, walls_obj
    
    if game_running: # Change the vector only if the game is running
        # Move left only if there's a free cell directly left
        
        next_left_cell_found = False
        
        # Count this only once -> Optimization
        pac_rightest_point_x = pac.x + pac.radius
        pac_highest_point_y = pac.y - pac.radius
        pac_lowest_point_y = pac.y + pac.radius
        pac_leftest_point_x = pac.x - pac_radius
        
        control_factor = ratio_between_cell_length_and_pac_radius / 2 * pac.radius
        
        for x in range(walls_number_horizontal):
            cells_rightest_point_x = scene_x + wall_length * (x + 1)
            pac_left_enough = (pac_leftest_point_x - cells_rightest_point_x) < control_factor
            
            # Only scan further for a cell directly left if the cell's x coordinate is right -> Optimization
            if pac_left_enough:
                pac_right_enough = (pac_leftest_point_x - cells_rightest_point_x) > 0
                if pac_right_enough:
                    for y in range(walls_number_vertical):
                        if not walls_obj.cell_filled(x=x, y=y): # Spare any calculations if the wall is filled                             
                            cells_highest_point_y = scene_y + wall_length * y
                            cells_lowest_point_y = scene_y + wall_length * (y + 1)
                            
                            pac_lower_than_cells_highest_point = (pac_highest_point_y - cells_highest_point_y) < control_factor
                            if pac_lower_than_cells_highest_point:
                                pac_higher_than_cells_lowest_point = cells_lowest_point_y - pac_highest_point_y
                                if pac_higher_than_cells_lowest_point: # All requieremnts are satisfied, there is a free cell directly on the left
                                    pac.change_movement_vector_to_left()
                                    next_left_cell_found = True
                                    print("Can move left -> Changing movement vector to left.")
                                    break
                    if next_left_cell_found: break
            
    if not next_left_cell_found:
        print("Can't move left -> Can't change the movement vector to left.")
    
def right_arrow_pressed():
    global game_running, pac, wall_length, ratio_between_cell_length_and_pac_radius, walls_obj
    
    # Count this only once -> Optimization
    pac_rightest_point_x = pac.x + pac.radius
    pac_highest_point_y = pac.y - pac.radius
    pac_lowest_point_y = pac.y + pac.radius
    pac_leftest_point_x = pac.x - pac_radius
    
    control_factor = ratio_between_cell_length_and_pac_radius / 2 * pac.radius
    
    if game_running: # Change the vector only if the game is running
        next_right_cell_found = False
        for x in range(walls_number_horizontal):
            cells_leftest_point_x = scene_x + wall_length * x
            pac_right_enough = (cells_leftest_point_x - pac_rightest_point_x) < control_factor

            # Only scan further for a cell directly left if the cell's x coordinate is right -> Optimization
            if pac_right_enough:
                del pac_right_enough
                pac_left_enough = (cells_leftest_point_x - pac_rightest_point_x) > 0
                if pac_left_enough:
                    for y in range(walls_number_vertical):
                        if not walls_obj.cell_filled(x=x, y=y): # Spare any calculations if the wall is filled 
                            cells_highest_point_y = scene_y + wall_length * y
                            cells_lowest_point_y = scene_y + wall_length * (y + 1)
                            cells_rightest_point_x = scene_x + wall_length * (x + 1)
                            
                            pac_lower_than_cells_highest_point = (pac_highest_point_y - cells_highest_point_y) < control_factor
                            if pac_lower_than_cells_highest_point:
                                pac_higher_than_cells_lowest_point = (cells_lowest_point_y - pac_lowest_point_y) < control_factor
                                if pac_higher_than_cells_lowest_point: # All requieremnts are satisfied, there is a free cell directly on the left
                                    pac.change_movement_vector_to_right()
                                    next_right_cell_found = True
                                    print("Can move right -> Changing movement vector to right.")
                                    break
                    if next_right_cell_found: break
        if not next_right_cell_found:
            print("Can't move right -> Can't change the movement vector to right.")
                        
def down_arrow_pressed():
    global game_running, pac
    
    control_factor = ratio_between_cell_length_and_pac_radius / 2 * pac.radius
    
    if game_running: pac.change_movement_vector_to_down()
    
def up_arrow_pressed():
    global game_running, pac
    
    control_factor = ratio_between_cell_length_and_pac_radius / 2 * pac.radius
    
    if game_running: pac.change_movement_vector_to_up()
    
def toggle_game_running():
    global game_running
    game_running = not game_running

# def change_direction_if_will_escape_scene():
#     global vector_x, vector_y, scene_x, scene_y, pac_radius, pac
    
#     if ((pac.x + vector_x + pac_radius) > (scene_x + scene_width)) or ((pac.x + vector_x - pac_radius) < scene_x):
#         vector_x = -vector_x
        
#     if ((pac.y - vector_y + pac_radius) > (scene_y + scene_height)) or ((pac.y - vector_y - pac_radius) < scene_y):
#         vector_y = -vector_y

# Create scene
background = Rechteck(x=scene_x, y=scene_y, winkel=0, breite=scene_width, hoehe=scene_height, farbe=scene_color)
background.GanzNachHintenBringen() # Place the background on the smallest z-index
background.FarbeSetzen((30,18,237)) # Make the background retro blue

# Create a labyrinth
walls_obj = Labyrinth(wall_map_width=walls_number_horizontal, wall_map_height=walls_number_vertical)
walls_obj.print_in_console()

walls_map = walls_obj.walls_map # Define walls_map for easier access to walls_obj.walls_map

# Fill the field with walls according to walls_map
for y in range(walls_obj.walls_n_vertical):
    for x in range(walls_obj.walls_n_horizontal):
        if walls_obj.cell_filled(x=x, y=y):
            wall_x = scene_x + x * wall_length
            wall_y = scene_y + y * wall_length
            wall = Rechteck(x=wall_x, y=wall_y, breite=wall_length, hoehe=wall_length, farbe="schwarz")
            wall.GanzNachVornBringen()

# Make everything out of labyrinth appear black by setting 4 rectangles
background_color_rectangles_length = 10000

background_color_rectangle_1 = Rechteck(x=scene_x-background_color_rectangles_length, y=scene_y - background_color_rectangles_length/4, breite=background_color_rectangles_length, hoehe=background_color_rectangles_length, farbe="schwarz")
background_color_rectangle_2 = Rechteck(x=scene_x+wall_length*walls_number_horizontal, y=scene_y - background_color_rectangles_length/4, breite=background_color_rectangles_length, hoehe=background_color_rectangles_length, farbe="schwarz")
background_color_rectangle_3 = Rechteck(x=scene_x - background_color_rectangles_length/4, y=scene_y + wall_length*walls_number_vertical, breite=background_color_rectangles_length, hoehe=background_color_rectangles_length, farbe="schwarz")
background_color_rectangle_4 = Rechteck(x=scene_x, y=scene_y - background_color_rectangles_length, breite=background_color_rectangles_length, hoehe=background_color_rectangles_length, farbe="schwarz")

for rect in [background_color_rectangle_1, background_color_rectangle_2, background_color_rectangle_3, background_color_rectangle_4]:
    rect.GanzNachVornBringen()

# Create Pac-Man and place him in the middle of the free cell
free_cell_matrix_x, free_cell_matrix_y = walls_obj.random_free_cell()
pac_start_x, pac_start_y = get_wall_middle_in_regular_coordinates(wall_x=free_cell_matrix_x, wall_y=free_cell_matrix_y)

pac = PacMan(x=pac_start_x, y=pac_start_y, angle=0, size=pac_radius*2, step=pac_step)
print(f"Pac-Man starts at matrix_x={free_cell_matrix_x} matrix_y={free_cell_matrix_y}")

# Randomly decide Pac-Man's angle at start
exits = walls_obj.get_exits(x=free_cell_matrix_x, y=free_cell_matrix_y)
attempts_counter = 0
while attempts_counter < 30:
    salt = randint(1, 500) # Python's randint module may prefer 0 over 1, 2, or 3, which causes the Pac-Man to almost always look left, but to prevent that there will be some "salt" added (-> word from cryptography)
    random_exit_index = randint(salt, len(exits) - 1 + salt) - salt
    if exits[random_exit_index] == True: # Found open exit
        if random_exit_index == 0: 
            pac.change_movement_vector_to_left()
        elif random_exit_index == 1: 
            pac.change_movement_vector_to_right
        elif random_exit_index == 2: 
            pac.change_movement_vector_to_up()
        elif random_exit_index == 3: 
            pac.change_movement_vector_to_down()
        else: 
            print("Fatal error! The exit index for the Pac-Man is unknown!!!")
            exit()
        break
    attempts_counter += 1
if attempts_counter > 30:
    print("Fatal error! The exit index for the Pac-Man wasn't found!!! Probably all exits closed!!!")
    exit()
del exits, random_exit_index, salt


# Link functions changing moving vector to the key presses
keyboard.on_press_key("left arrow", lambda _: left_arrow_pressed())
keyboard.on_press_key("right arrow", lambda _: right_arrow_pressed())
keyboard.on_press_key("up arrow", lambda _: up_arrow_pressed())
keyboard.on_press_key("down arrow", lambda _: down_arrow_pressed())
keyboard.on_press_key("space", lambda _: toggle_game_running())

points: int = 0 # Points counter

# Draw food pieces in all the free cells except the one with Pac-Man
free_cells = walls_obj.get_all_free_cells()
food_pieces = [] # The array with the food pieces

for cell in free_cells:
    regular_x, regular_y = get_wall_middle_in_regular_coordinates(cell[0], cell[1])
    if regular_x != pac_start_x or regular_y != pac_start_y:
        food = FoodPiece(x=regular_x, y=regular_y, radius=2)
        food_pieces.append(food)
        
def check_whether_pac_just_ate_food():
    global food_pieces, pac, points, points_for_eating_dot
    
    for piece in food_pieces:
        piece_x = piece.x
        piece_y = piece.y
        
        if abs(piece_x - pac.x) < pac.radius and abs(piece_y - pac.y) < pac.radius: # We found the piece pac just ate (= the piece the pac is now in front of)
            # Make the piece invisible and add points
            piece.aten()
            points += points_for_eating_dot
            
            

background.GanzNachHintenBringen()
pac.GanzNachVornBringen() # Place Pac-Man in front of all the other objects

# ghost_a = Ghost(farbe="rot")
                
# Indefinite loop of game
#while True:
#     Check whether the move will make Pac-Man escape the scene and change the vector accordingly
#     change_direction_if_will_escape_scene()
    
#     Move Pac-Man
#     pac.move_according_to_vector()
    
#    # Check whether Pac-Man just ate a food-dot
#    check_whether_pac_just_ate_food()
#     Stop for a predefined time
#     sleep(waiting_time)

# Only for use on MacOS
# left_arrow_pressed()
# right_arrow_pressed()
# pac.close_mouth()
print(f"You scored {points} points!")
Zeichenfenster().run()