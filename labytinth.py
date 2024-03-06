from random import randint
from random import choice
from colorama import init, Fore
from time import sleep

# Class Labyrinth creates the labyrinth matrix
class Labyrinth:
    walls_map = [] # Map of the walls and unfilled spaces inside the labirynth
    
    walls_n_vertical = 0 # Number of vertical cells
    walls_n_horizontal = 0 # Number of horizontal cells
    
    debug_mode = False
    
    def __init__(self, wall_map_width: int, wall_map_height: int, debug_mode: bool = False):
        # Check that the width and height is big enough
        if wall_map_width < 10 or wall_map_height < 10:
            print("Fatal Error: When creating an instance of Labyrinth class, the width and height must be 10 or higher!")
            exit(0)
        
        # Set the inner constraints to the arguments
        self.walls_n_horizontal = wall_map_width
        self.walls_n_vertical = wall_map_height
        self.debug_mode = debug_mode
        
        # Create a filled basic matrix
        self.walls_map = self._initialise_basic_walls_map()
        
        # # Add random walls to the walls map
        self._add_random_walls()
        
        # # Place all walls
        self._go_through_each_cell_and_add_walls()
        
        # Search for "walls of walls" (= rows/columns that consist only of walls) and make exits through them
        self._make_ways_through_walls_of_walls()
        
        # Fill the cells with one or zero way out
        self._fill_cells_with_one_or_zero_ways_out()
        
        # Make the side cells free as a universal way
        #if randint(1, 2) == 2: 
        self.make_side_cells_free()
        
        # Fill the cells with one or zero way out
        self._fill_cells_with_one_or_zero_ways_out()
    
    def _initialise_basic_walls_map(self) -> list:
        map = []
        
        for raw_index in range(self.walls_n_vertical):
            is_first_or_last_row = (raw_index == self.walls_n_vertical - 1) or (raw_index == 0)
            
            array_for_raw = []
            for column_index in range(self.walls_n_horizontal):
                if is_first_or_last_row: array_for_raw.append(True) # If first or last row, add a wall
                else: array_for_raw.append(False) # Otherwise fill with empty space
            
            if not is_first_or_last_row: 
                array_for_raw[0] = True
                array_for_raw[1] = False
                
                array_for_raw[-1] = True
                array_for_raw[-2] = False
                
                if raw_index == 2 or raw_index + 3 == self.walls_n_vertical:
                    array_for_raw[2] = True
                    array_for_raw[-3] = True
            
            map.append(array_for_raw)
            
        return map
    
    def _add_random_walls(self):
        number_of_attempts = randint(5, round(self.walls_n_horizontal * self.walls_n_vertical / 4))
        
        for i in range(round(number_of_attempts * 2/3)): # Place the walls at uneven spaces
            while True:
                # Don't take the first and last column as well row (because they should be already filled)
                x = randint(1, self.walls_n_horizontal - 2)
                y = randint(1, self.walls_n_vertical - 2)

#                if x % 2 != 0 and y % 2 != 0 and not self.cell_filled(x=x, y=y):       
                if not self.cell_filled(x=x, y=y):
                    self._close_cell(x=x, y=y)
                    break
        
        for i in range(round(number_of_attempts / 3)): # Place the walls at even spaces
            # Don't take the first and last column as well row (because they should be already filled)
            x = randint(1, self.walls_n_horizontal - 2)
            y = randint(1, self.walls_n_vertical - 2)
                            
            if not self.cell_filled(x=x, y=y):
                self._close_cell(x=x, y=y)
    
    def _is_there_diagonally_wall(self, index_vertical: int, index_horizontal: int) -> bool:
        # Logic: if there's block diagonally and not directly to the side, return True, but if there's a block directly to the side (like there's a wall diagonally right-up but there's a block directly right -> return False)
        
        diagonally_to_right_up = False
        try: diagonally_to_right_up = self.walls_map[index_vertical - 1][index_horizontal + 1]
        except: pass
        
        diagonally_to_left_up = False
        try: diagonally_to_left_up = self.walls_map[index_vertical - 1][index_horizontal - 1]
        except: pass
        
        diagonally_to_right_down = False
        try: diagonally_to_right_down = self.walls_map[index_vertical + 1][index_horizontal + 1]
        except: pass
        
        diagonally_to_left_down = False
        try: diagonally_to_left_down = self.walls_map[index_vertical + 1][index_horizontal - 1]
        except: pass
        
        # Find out whether there are blocks directly left/right/up/down
        wall_directly_up = False
        try: wall_directly_up = self.walls_map[index_vertical - 1][index_horizontal]
        except: pass
        
        wall_directly_left = False
        try: wall_directly_left = self.walls_map[index_vertical][index_horizontal - 1]
        except: pass
        
        wall_directly_down = False
        try: wall_directly_down = self.walls_map[index_vertical + 1][index_horizontal]
        except: pass
        
        wall_directly_right = False
        try: wall_directly_right = self.walls_map[index_vertical][index_horizontal + 1]
        except: pass
        
        if randint(1, 100) > 90: 
            return not ((diagonally_to_left_up == wall_directly_left or diagonally_to_left_up == wall_directly_up) or (diagonally_to_left_down == wall_directly_left or diagonally_to_left_down == wall_directly_down) and (diagonally_to_right_up == wall_directly_right or diagonally_to_right_up == wall_directly_up) and (diagonally_to_right_down == wall_directly_right or diagonally_to_right_down == wall_directly_down))
        else: 
            return (diagonally_to_left_up or diagonally_to_right_up or diagonally_to_right_down or diagonally_to_left_down)
        # place_block = (diagonally_to_left_up or diagonally_to_right_up or diagonally_to_right_down or diagonally_to_left_down)
        # return not place_block
    
    def cell_filled(self, x: int, y: int) -> bool:
        try: return self.walls_map[y][x]
        except:
            if self.debug_mode: print(f"Error: the cell with coordinates x={x} y={y} doesn't exist! Rerturning True (that cell is filled)...")
            return True
    
    def cell_exists(self, x: int, y: int) -> bool:
        try: 
            a = self.walls_map[y][x]
            return True
        except:
            return False
        
    def get_exits(self, x: int, y: int) -> list:
        """Finds and returns array of exits for the cell

        Args:
            x (int): x-coordinate of the cell
            y (int): y-coordinate of the cell

        Returns:
            list: List of True(open) and False(closed) exits for the position in format [there_is_exit_left, there_is_exit_right, there_is_exit_up, there_is_exit_down]
        """
        
        if not self.cell_exists(x=x, y=y):
            if self.debug_mode: print(f"Error: the cell with coordinates x={x} y={y} doesn't exist! Returning False for all the exits...")
        
        there_is_exit_left = False
        try: there_is_exit_left = not self.walls_map[y][x - 1]
        except: pass
        
        there_is_exit_right = False
        try: there_is_exit_right = not self.walls_map[y][x + 1]
        except: pass
        
        there_is_exit_up = False
        try: there_is_exit_up = not self.walls_map[y - 1][x]
        except: pass
        
        there_is_exit_down = False
        try: there_is_exit_down = not self.walls_map[y + 1][x]
        except: pass
        
        return [there_is_exit_left, there_is_exit_right, there_is_exit_up, there_is_exit_down]
    
    # By using a randomness determines whether make 2 exits out of 3
    def _make_2_exits_out_of_3(self) -> bool:
        # if randint(1, 20) > randint(17, 20):
        #     return randint(1, 10) == randint(1, 10)
        # else: 
            return randint(1, 10) == randint(1, 10)
    
    def _close_cell(self, x: int, y: int):
        if self.debug_mode: print(f"Closing the cell x={x} y={y}")
        try: self.walls_map[y][x] = True
        except: 
            if self.debug_mode: print(f"Error: the cell with coordinates x={x} y={y} doesn't exist => Can't close it")
        
    def _open_cell(self, x: int, y: int):
        if self.debug_mode: print(f"Closing the cell x={x} y={y}")
        try: self.walls_map[y][x] = False
        except: 
            if self.debug_mode: print(f"Error: the cell with coordinates x={x} y={y} doesn't exist => Can't open it")
        
    # Returns position of the exit in format y, x
    def _get_position_of_exit(self, exit_index: int, origin_x: int, origin_y: int) -> list:
        vertical_index_in_walls_map = 0
        horizontal_index_in_walls_map = 0
        
        if exit_index == 0: # Exit left
            vertical_index_in_walls_map = origin_y
            horizontal_index_in_walls_map = origin_x - 1
        elif exit_index == 1: # Exit right
            vertical_index_in_walls_map = origin_y
            horizontal_index_in_walls_map = origin_x + 1
        elif exit_index == 2: # Exit up
            vertical_index_in_walls_map = origin_y - 1
            horizontal_index_in_walls_map = origin_x
        elif exit_index == 0: # Exit down
            vertical_index_in_walls_map = origin_y + 1
            horizontal_index_in_walls_map = origin_x
        
        return [vertical_index_in_walls_map, horizontal_index_in_walls_map]
    
    def _number_of_exits_based_on(self, there_is_exit_left: bool, there_is_exit_right: bool, there_is_exit_up: bool, there_is_exit_down: bool) -> int:
        number_of_exits = 0
        
        if there_is_exit_left: number_of_exits += 1
        if there_is_exit_right: number_of_exits += 1
        if there_is_exit_up: number_of_exits += 1
        if there_is_exit_down: number_of_exits += 1
        
        return number_of_exits
    
    def _fill_cells_with_one_or_zero_ways_out(self):
        for i in range(randint(1, 3)): # Repeat the filling process a few times to surely fill all cells with or one exits
            for index_n_vertical in range(self.walls_n_vertical):
                for index_n_horizontal in range(self.walls_n_horizontal):
                    if self.walls_map[index_n_vertical][index_n_horizontal] == False: # If the cell isn't filled, check where are the exits (free cells to different sides of the origin cell)
                        there_is_exit_left, there_is_exit_right, there_is_exit_up, there_is_exit_down = self.get_exits(x=index_n_horizontal, y=index_n_vertical)
                        num_exits = self._number_of_exits_based_on(there_is_exit_left=there_is_exit_left, there_is_exit_down=there_is_exit_down, there_is_exit_right=there_is_exit_right, there_is_exit_up=there_is_exit_up)
                        
                            
                        if num_exits <= 1: # Only one or even no exit, that's not enough to play -> place a wall here
                            self._close_cell(x=index_n_horizontal, y=index_n_vertical)
                            continue
                        

                    # if num_exits == 0:
                    #     self.walls_map[index_n_vertical][index_n_horizontal] = True
                    # elif number_of_exits == 0:
                    #     self._close_cell(x=index_n_horizontal, y=index_n_vertical)
                    #     continue
    
    def _go_through_each_cell_and_add_walls(self):
        for n_vertical in range(self.walls_n_vertical):
            for n_horizontal in range(self.walls_n_horizontal):
                if self.walls_map[n_vertical][n_horizontal] == False: # If the cell isn't filled, check where are the exits (free cells to different sides of the origin cell)
                    there_is_exit_left, there_is_exit_right, there_is_exit_up, there_is_exit_down = self.get_exits(x=n_horizontal, y=n_vertical)
                    number_of_exits = self._number_of_exits_based_on(there_is_exit_left, there_is_exit_down, there_is_exit_right, there_is_exit_up)
                    
                    exits_map = [there_is_exit_left, there_is_exit_right, there_is_exit_up, there_is_exit_down]
                    
                    if number_of_exits == 1: # Only one or even no exit, that's not enough to play -> place a wall here
                       self._close_cell(x=n_horizontal, y=n_vertical)
                       pass
                    elif number_of_exits == 2: # Only 2 exits (the minimum), continue
                        continue
                    elif number_of_exits == 3: # There're 3 exists, which can randomly become 2
                        if self._make_2_exits_out_of_3(): # The 3 exits will randomly become 2
                            attempt = 1
                            max_number_of_attempts = randint(1, 5)
                            while attempt < max_number_of_attempts: # Break out if too many atttempts (meaning it's probably impossible that it's impossible to find such an exit) or the exit is closed
                                random_exit_index = randint(0, 3) # Randomly choose an exit
                                
                                # Figure out the position of the exit in walls_map
                                indexes = self._get_position_of_exit(exit_index=random_exit_index, origin_x=n_horizontal, origin_y=n_vertical)
                                vertical_index_in_walls_map = indexes[0]
                                horizontal_index_in_walls_map = indexes[1]
                                
                                # Print debugging message
                                if self.debug_mode: print(f"Attempting x={horizontal_index_in_walls_map} y={vertical_index_in_walls_map}")
                                
                                if exits_map[random_exit_index] == False: # If the exit is already closed, continue trying till the open exit isn't randomly found
                                    continue
                                elif not self._is_there_diagonally_wall(index_vertical=vertical_index_in_walls_map, index_horizontal=horizontal_index_in_walls_map): # The exit is open, nut there's extra condition: the exit can be only closed (= the wall will be placed there), if there's no diagonally wall                                    
                                    self._close_cell(x=horizontal_index_in_walls_map, y=vertical_index_in_walls_map) # Closing the open cell
                                    break # Break out of the loop because the exit is closed

                                attempt += 1 # Add 1 to the attempt counter
                            
                            if self.debug_mode: print("Got out") # Print debug message that the program is done with that loop got out                            
                            
                    elif number_of_exits == 4: # All directions are free, 1 to 2 walls can be created
                        attempt = 1
                        closed_exits = 0
                        while (not closed_exits == 2) and (attempt < randint(4,5)): # Break out if too many atttempts (meaning it's probably impossible that it's impossible to find such an exit) or all exits are closed
                            random_exit_index = randint(0, 3)
                            
                            # Figure out the position of the exit in walls_map
                            indexes = self._get_position_of_exit(exit_index=random_exit_index, origin_x=n_horizontal, origin_y=n_vertical)
                            vertical_index_in_walls_map = indexes[0]
                            horizontal_index_in_walls_map = indexes[1]
                            
                            if self.debug_mode: print(f"Attempting x={horizontal_index_in_walls_map} y={vertical_index_in_walls_map}") # Print debug message
                            
                            # Extra condition: the exit can be only closed (= the wall will be placed there), if there's no diagonally wall
                            if not self._is_there_diagonally_wall(index_vertical=vertical_index_in_walls_map, index_horizontal=horizontal_index_in_walls_map): 
                                self._close_cell(x=horizontal_index_in_walls_map, y=vertical_index_in_walls_map) # Closing the open exit
                                closed_exits += 1 # Add the closed exit to the counter

                            attempt += 1  # Add 1 to the attempt counter
                            if self.debug_mode: print("Got out") # Print debug message that the program is done with that loop got out
        
    def _make_ways_through_wall_columns(self):
        x_coordinates_of_wall_columns = [] # Array for storing the x coordinate of wall columns
        
        # 1st step: Locate all columns that only consist of walls (except for the side ones) and save their x coordinate into an array
        for x in range(1, self.walls_n_horizontal - 2):
            completely_out_of_walls = True # Shows after the examination whether at the x coordinate there're only walls
            
            for y in range(1, self.walls_n_vertical - 2):
                if not self.cell_filled(x=x, y=y): # If there's at least one cell free break out from the loop and look at the next row
                    completely_out_of_walls = False
                    break
            
            if completely_out_of_walls: # Add the x-coordinate to the array if the column is completely out of walls
                x_coordinates_of_wall_columns.append(x)
                continue
        if self.debug_mode: (f"x-coordinates of wall columns: {x_coordinates_of_wall_columns}")
        
        # 2nd step: Go through all the coordinates and make some ways if there are free cells left and right
        for x in x_coordinates_of_wall_columns:
            if self.debug_mode: print(f"Cleaning wall column at x={x}")
            y_coordinates_with_horizontal_exits_free = [] # Array for storing the y-coordinates for the current column which have left and right exits free
            
            # Go through the column and add those with left and right exits to the array
            for y in range(1, self.walls_n_vertical - 2):
                exits = self.get_exits(x=x, y=y) # Get list of exits
                left_and_right_exits_free = exits[0] and exits[1] # Shows whether left AND right exits are free
                if left_and_right_exits_free: 
                    y_coordinates_with_horizontal_exits_free.append(y)

            # Based on the number of the cells with 2 exits decide how many should be opened
            number_of_cells_with_horizontal_exits_free = len(y_coordinates_with_horizontal_exits_free)
            if self.debug_mode: print(number_of_cells_with_horizontal_exits_free)
            if number_of_cells_with_horizontal_exits_free == 0: # No cells with horizontal exits free
                continue
            elif 0 < number_of_cells_with_horizontal_exits_free < round(self.walls_n_vertical / 2): # Number of such cells is between one and half of the labytinth
                for y in y_coordinates_with_horizontal_exits_free:
                    self._open_cell(x=x, y=y)
                    if self.debug_mode: print(f"Opening cell with coordinates x={x} y={y}")
            else:
                # Open randomly some exits
                max_number_of_open_exits = round(len(y_coordinates_with_horizontal_exits_free) / 2)
                for i in range(randint(1, max_number_of_open_exits)):
                    while True: # Loop to ensure we search until we find an open cell
                        y = choice(y_coordinates_with_horizontal_exits_free)
                        if self.cell_filled(x=x, y=y):
                            self._open_cell(x=x, y=y)
                            break # Break because found a closed exit and opened it
                
    def _make_ways_through_wall_rows(self):
        y_coordinates_of_wall_columns = [] # Array for storing the y coordinate of wall columns
        
        # 1st step: Locate all rows that only consist of walls (except for the side ones) and save their y coordinate into an array
        for y in range(1, self.walls_n_vertical - 2):
            completely_out_of_walls = True # Shows after the examination whether at the x coordinate there're only walls
            
            for x in range(1, self.walls_n_horizontal - 2):
                if not self.cell_filled(x=x, y=y): # If there's at least one cell free break out from the loop and look at the next row
                    completely_out_of_walls = False
                    break
            
            if completely_out_of_walls: # Add the x-coordinate to the array if the column is completely out of walls
                y_coordinates_of_wall_columns.append(y)
                continue
        if self.debug_mode: print(f"y-coordinates of wall columns: {y_coordinates_of_wall_columns}")
        
        # 2nd step: Go through all the coordinates and make some ways if there are free cells up and down
        for y in y_coordinates_of_wall_columns:
            if self.debug_mode: print(f"Cleaning wall row at y={y}")
            x_coordinates_with_horizontal_exits_free = [] # Array for storing the y-coordinates for the current column which have up and down exits free
            
            # Go through the column and add those with left and right exits to the array
            for x in range(1, self.walls_n_horizontal - 2):
                exits = self.get_exits(x=x, y=y) # Get list of exits
                up_and_down_exits_free = exits[2] and exits[3] # Shows whether up AND down exits are free
                
                if up_and_down_exits_free: 
                    x_coordinates_with_horizontal_exits_free.append(x)

            # Based on the number of the cells with 2 exits decide how many should be opened
            number_of_cells_with_vertical_exits_free = len(x_coordinates_with_horizontal_exits_free)
            if number_of_cells_with_vertical_exits_free == 0: # No cells with vertical exits free
                continue
            elif 0 < number_of_cells_with_vertical_exits_free < round(self.walls_n_horizontal / 2): # Number of such cells is between one and half of the labytinth width
                for x in x_coordinates_with_horizontal_exits_free:
                    self._open_cell(x=x, y=y)
                    if self.debug_mode: print(f"Opening cell with coordinates x={x} y={y}")       
            else:
                # Open randomly some exits
                max_number_of_open_exits = round(len(x_coordinates_with_horizontal_exits_free) / 2)
                for i in range(randint(1, max_number_of_open_exits)):
                    while True: # Loop to ensure we search until we find an open cell
                        x = choice(x_coordinates_with_horizontal_exits_free)
                        if self.cell_filled(x=x, y=y):
                            self._open_cell(x=x, y=y)
                            break # Break because found a closed exit and opened it
    
    def _make_ways_through_walls_of_walls(self):
        for i in range(randint(2, 7)):
            self._make_ways_through_wall_columns()
            self._make_ways_through_wall_rows()
      
    def print_in_console(self):
        from colorama import init, Fore
        init()
        
        print("----------------- Labyrinth -----------------")
        
        for n_vertic in range(self.walls_n_vertical):
            for n_horizon in range(self.walls_n_horizontal):
                if self.walls_map[n_vertic][n_horizon]:
                    print(Fore.RED, "B", end="")
                else:
                    print(Fore.GREEN, "o", end="")
            print(Fore.WHITE, f" {n_vertic}\n") # Print the row index on the right side of the labyrinth
        
        # Print the column index under the labyrinth
        for i in range(self.walls_n_horizontal):
            if i >= 10:
                print(Fore.WHITE, str(i)[-1], end="")
            else: print(Fore.WHITE, f"{i}", end="")
        print("\n")
        
        print("---------------------------------------------")

    def random_free_cell(self) -> list:
        """Finds a random free cell and gives its coordinates

        Returns:
            list: Coordinates in format [x: int, y: int]
        """
        
        while True:
            choice(choice(self.walls_map))
            x = randint(1, self.walls_n_horizontal - 2)
            y = randint(1, self.walls_n_vertical - 2)
            
            if not self.cell_filled(x=x, y=y):
                return [x, y]
                break
    
    def get_all_free_cells(self) -> list:
        free_cells = []
        
        for n_vertic in range(self.walls_n_vertical):
            for n_horizon in range(self.walls_n_horizontal):
                if not self.cell_filled(x=n_horizon, y=n_vertic):
                    free_cells.append([n_horizon, n_vertic])
        return free_cells

    def make_side_cells_free(self):
        new_map = []
        for raw_index in range(self.walls_n_vertical):
            is_first_or_last_row = (raw_index == self.walls_n_vertical - 1) or (raw_index == 0)
            
            array_for_raw = []
            for column_index in range(self.walls_n_horizontal):
                if (raw_index == 1 or raw_index == self.walls_n_vertical - 2) or (column_index == 0 or column_index == self.walls_n_horizontal - 2) and not is_first_or_last_row: array_for_raw.append(False) # Make side cells free
                else: array_for_raw.append(self.walls_map[raw_index][column_index]) # Otherwise add to the new map the cells that are already there (= not change anything)
            
            if not is_first_or_last_row: 
                array_for_raw[0] = True
                array_for_raw[1] = False
                
                array_for_raw[-1] = True
                array_for_raw[-2] = False
            
            new_map.append(array_for_raw)

        self.walls_map = new_map

# Usage
obj = Labyrinth(wall_map_width=23, wall_map_height=16)
walls_map = obj.walls_map

obj.print_in_console()