import random
import math
import time
from cell import Cell

class Maze(object):
    """Class representing a maze; a 2D grid of Cell objects. Contains functions
    for generating randomly generating the maze as well as for solving the maze.

    Attributes:
        num_cols (int): The height of the maze, in Cells
        num_rows (int): The width of the maze, in Cells
        id (int): A unique identifier for the maze
        grid_size (int): The area of the maze, also the total number of Cells in the maze
        entry_coor Entry location cell of maze
        exit_coor Exit location cell of maze
        generation_path : The path that was taken when generating the maze
        solution_path : The path that was taken by a solver when solving the maze
        initial_grid (list):
        grid (list): A copy of initial_grid (possible this is un-needed)
        """

    def __init__(self, num_rows, num_cols, id, randomseed = 1):
        """Creates a gird of Cell objects that are neighbors to each other.

            Args:
                    num_rows (int): The width of the maze, in cells
                    num_cols (int): The height of the maze in cells
                    id (id): An unique identifier

        """
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.id = id
        self.grid_size = num_rows*num_cols
        self.entry_coor = (0,0)
        self.exit_coor = (num_rows-1,num_cols-1)
        self.generation_path = []
        self.solution_path = None
        self.initial_grid = self.generate_grid()
        self.grid = self.initial_grid
        self.generate_maze((0, 0),randomseed)

    def generate_grid(self):
        """Function that creates a 2D grid of Cell objects. This can be thought of as a
        maze without any paths carved out

        Return:
            A list with Cell objects at each position

        """

        # Create an empty list

        grid = list()

        # Place a Cell object at each location in the grid
        for i in range(self.num_rows):
            grid.append(list())

            for j in range(self.num_cols):
                grid[i].append(Cell(i, j))

        return grid

    def find_neighbours(self, cell_row, cell_col):
        """Finds all existing and unvisited neighbours of a cell in the
        grid. Return a list of tuples containing indices for the unvisited neighbours.

        Args:
            cell_row (int):
            cell_col (int):

        Return:
            None: If there are no unvisited neighbors
            list: A list of neighbors that have not been visited
        """
        neighbours = list()

        def check_neighbour(row, col):
            # Check that a neighbour exists and that it's not visited before.
            if row >= 0 and row < self.num_rows and col >= 0 and col < self.num_cols:
                neighbours.append((row, col))

        check_neighbour(cell_row-1, cell_col)     # Top neighbour
        check_neighbour(cell_row, cell_col+1)     # Right neighbour
        check_neighbour(cell_row+1, cell_col)     # Bottom neighbour
        check_neighbour(cell_row, cell_col-1)     # Left neighbour

        if len(neighbours) > 0:
            return neighbours

        else:
            return None     # None if no unvisited neighbours found

    def _validate_neighbours_generate(self, neighbour_indices):
        """Function that validates whether a neighbour is unvisited or not. When generating
        the maze, we only want to move to move to unvisited cells (unless we are backtracking).

        Args:
            neighbour_indices:

        Return:
            True: If the neighbor has been visited
            False: If the neighbor has not been visited

        """

        neigh_list = [n for n in neighbour_indices if not self.grid[n[0]][n[1]].visited]

        if len(neigh_list) > 0:
            return neigh_list
        else:
            return None

    def validate_neighbours_solve(self, neighbour_indices, k, l, k_end, l_end, method = "fancy"):
        """Function that validates whether a neighbour is unvisited or not and discards the
        neighbours that are inaccessible due to walls between them and the current cell. The
        function implements two methods for choosing next cell; one is 'brute-force' where one
        of the neighbours are chosen randomly. The other is 'fancy' where the next cell is chosen
        based on which neighbour that gives the shortest distance to the final destination.

        Args:
            neighbour_indices
            k
            l
            k_end
            l_end
            method

        Return:


        """
        if method == "fancy":
            neigh_list = list()
            min_dist_to_target = 100000

            for k_n, l_n in neighbour_indices:
                if (not self.grid[k_n][l_n].visited
                        and not self.grid[k][l].is_walls_between(self.grid[k_n][l_n])):
                    dist_to_target = math.sqrt((k_n - k_end) ** 2 + (l_n - l_end) ** 2)

                    if (dist_to_target < min_dist_to_target):
                        min_dist_to_target = dist_to_target
                        min_neigh = (k_n, l_n)

            if "min_neigh" in locals():
                neigh_list.append(min_neigh)

        elif method == "brute-force":
            neigh_list = [n for n in neighbour_indices if not self.grid[n[0]][n[1]].visited
                          and not self.grid[k][l].is_walls_between(self.grid[n[0]][n[1]])]

        if len(neigh_list) > 0:
            return neigh_list
        else:
            return None

    def _pick_random_entry_exit(self, used_entry_exit=None):
        """Function that picks random coordinates along the maze boundary to represent either
        the entry or exit point of the maze. Makes sure they are not at the same place.

        Args:
            used_entry_exit

        Return:

        """
        rng_entry_exit = used_entry_exit    # Initialize with used value

        # Try until unused location along boundary is found.
        while rng_entry_exit == used_entry_exit:
            rng_side = random.randint(0, 3)

            if (rng_side == 0):     # Top side
                rng_entry_exit = (0, random.randint(0, self.num_cols-1))

            elif (rng_side == 2):   # Right side
                rng_entry_exit = (self.num_rows-1, random.randint(0, self.num_cols-1))

            elif (rng_side == 1):   # Bottom side
                rng_entry_exit = (random.randint(0, self.num_rows-1), self.num_cols-1)

            elif (rng_side == 3):   # Left side
                rng_entry_exit = (random.randint(0, self.num_rows-1), 0)

        return rng_entry_exit       # Return entry/exit that is different from exit/entry
   
    def generate_maze(self, start_coor = (0, 0), randomseed = 1):
        """This takes the internal grid object and removes walls between cells using the
        depth-first recursive backtracker algorithm.

        Args:
            start_coor: The starting point for the algorithm

        """
        #random.seed(randomseed) #only use if deterministic maze generation is needed!

        k_curr, l_curr = start_coor             # Where to start generating
        path = [(k_curr, l_curr)]               # To track path of solution
        self.grid[k_curr][l_curr].visited = True     # Set initial cell to visited
        visit_counter = 1                       # To count number of visited cells
        visited_cells = list()                  # Stack of visited cells for backtracking

        #print("\nGenerating the maze with depth-first search...")
        time_start = time.clock()

        while visit_counter < self.grid_size:     # While there are unvisited cells
            neighbour_indices = self.find_neighbours(k_curr, l_curr)    # Find neighbour indicies
            neighbour_indices = self._validate_neighbours_generate(neighbour_indices)

            if neighbour_indices is not None:   # If there are unvisited neighbour cells
                visited_cells.append((k_curr, l_curr))              # Add current cell to stack
                k_next, l_next = random.choice(neighbour_indices)     # Choose random neighbour
                self.grid[k_curr][l_curr].remove_walls(k_next, l_next)   # Remove walls between neighbours
                self.grid[k_next][l_next].remove_walls(k_curr, l_curr)   # Remove walls between neighbours
                self.grid[k_next][l_next].visited = True                 # Move to that neighbour
                k_curr = k_next
                l_curr = l_next
                path.append((k_curr, l_curr))   # Add coordinates to part of generation path
                visit_counter += 1

            elif len(visited_cells) > 0:  # If there are no unvisited neighbour cells
                k_curr, l_curr = visited_cells.pop()      # Pop previous visited cell (backtracking)
                path.append((k_curr, l_curr))   # Add coordinates to part of generation path

        #print("Number of moves performed: {}".format(len(path)))
        #print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))


        self.grid[self.entry_coor[0]][self.entry_coor[1]].set_as_entry_exit("entry", self.num_rows-1, self.num_cols-1)
        self.grid[self.exit_coor[0]][self.exit_coor[1]].set_as_entry_exit("exit", self.num_rows-1, self.num_cols-1)
        
        
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.grid[i][j].visited = False      # Set all cells to unvisited before returning grid
        self.generation_path = path
        
        
        #targyak elhelyezese
        i = 0
        while i < self.id:
            x = random.randint(0,self.num_rows-1)
            y = random.randint(0,self.num_cols-1)
            if(self.grid[x][y].have_obj == False):
                self.grid[x][y].set_obj()
                i += 1
        
        #falak kitorese
        i = int(self.num_cols*self.num_rows/100)*2 + 1 # 1% +1 fal kitorese
        while i > 0:
            x = random.randint(1,self.num_rows-2)
            y = random.randint(1,self.num_cols-2)
            self.remove_wall(x, y)
            i -= 1
    
    def remove_wall(self, i, j):
        if self.grid[i][j].walls["top"]:
            self.grid[i][j].remove_wall("top")
            self.grid[i-1][j].remove_wall("bottom")
        if self.grid[i][j].walls["right"]:
            self.grid[i][j].remove_wall("right")
            self.grid[i][j+1].remove_wall("left")
        if self.grid[i][j].walls["bottom"]:
            self.grid[i][j].remove_wall("bottom")
            self.grid[i+1][j].remove_wall("top")
        if self.grid[i][j].walls["left"]:
            self.grid[i][j].remove_wall("left")
            self.grid[i][j-1].remove_wall("right")
        
    def generate_maze_with_numbers(self):
        """ kiirja egy listaba az osszes cellara az alabbiak osszeget
            csak a labirintus megoldasa utan hivhato!
            TODO ATIRNI
            fent: 1
            jobb: 2
            lent: 4
            bal : 8
            targy: 16
        """
        maze_in_numbers = []
        counter = 0
        object_placed = 0
        for i in range(self.num_rows):
            maze_rows_in_numbers = []
            for j in range(0, self.num_cols):
                counter += 1
                cell_value = 0
                if self.grid[i][j].walls["top"]:
                    cell_value += 1
                if self.grid[i][j].walls["right"]:
                    cell_value += 2
                if self.grid[i][j].walls["bottom"]:
                    cell_value += 4
                if self.grid[i][j].walls["left"]:
                    cell_value += 8
                if self.grid[i][j].have_obj == True:
                    cell_value += 16
                
                maze_rows_in_numbers.append(cell_value)
            maze_in_numbers.append(maze_rows_in_numbers)
            
        return maze_in_numbers
        
    
    def check_solution(self, solution):
        curr_poz = self.grid[0][0]
        isok = True
        message = 'Maze Correctly Solved'
        gathered = 0

        try:
            for line in solution:
                if 'felvesz' in line:
                    if curr_poz.have_obj == True:
                        curr_poz.get_obj()
                        gathered += 1
                    else:
                        isok = False
                        message = 'Tried to pick up non-existing object at %d;%d '%(curr_poz.row, curr_poz.col)+str(line)
                        break
                else:
                    x = int(line.split(" ")[0])
                    y = int(line.split(" ")[1])
                    if x >= 0 and x <= self.num_rows and y >= 0 and y <= self.num_cols:
                        if (abs(x - curr_poz.row) + abs(y - curr_poz.col))>1:
                            isok = False
                            message = 'Tried to move more than 1 space with '+ str(line)
                            break
                        #ide eljut ha szabalyos a lepes
                        elif x == curr_poz.row -1 and y == curr_poz.col:      #fel
                            if curr_poz.walls["top"] == True:
                                isok = False
                                message = 'Collided with top wall at move '+ str(line)
                                break
                            else:
                                curr_poz = self.grid[x][y]
                                
                        elif x == curr_poz.row and y == curr_poz.col +1:    #jobbra
                            if curr_poz.walls["right"] == True:
                                isok = False
                                message = 'Collided with right wall at move '+ str(line)
                                break
                            else:
                                curr_poz = self.grid[x][y]
                                
                        elif x == curr_poz.row +1 and y == curr_poz.col:    #le
                            if curr_poz.walls["bottom"] == True:
                                isok = False
                                message = 'Collided with bottom wall at move '+ str(line)
                                break
                            else:
                                curr_poz = self.grid[x][y]
                                
                        elif x == curr_poz.row and y == curr_poz.col -1:    #balra
                            if curr_poz.walls["left"] == True:
                                isok = False
                                message = 'Collided with left wall at move '+ str(line)
                                break
                            else:
                                curr_poz = self.grid[x][y]
                                
                        else:
                            isok = False
                            message = 'Unable to parse command at '+ str(line)
                            break
                    else:
                        isok = False
                        message = 'Moved out of bounds at move '+ str(line)
                        break
                    
            if(gathered != self.id):
                message = 'Only gathered %d of %d items!'%(gathered,self.id)
                isok = False
        except:
            message = 'Failed to parse command at: '+str(line)
            isok = False
            pass
        return (isok,message)
 