from maze import Maze
import sys

class MazeManager(object):
    """A manager that abstracts the interaction with the library's components. The graphs, animations, maze creation,
    and solutions are all handled through the manager.

    Attributes:
        mazes (list): It is possible to have more than one maze. They are stored inside this variable.
        media_name (string): The filename for animations and images
        quiet_mode (bool): When true, information is not shown on the console
    """

    def __init__(self):
        self.mazes = []
        self.media_name = ""
        self.quiet_mode = True

    def add_maze(self, row, col, objects, id):
        """Add a maze to the manager. We give the maze an index of
        the total number of mazes in the manager. As long as we don't
        add functionality to delete mazes from the manager, the ids will
        always be unique. Note that the id will always be greater than 0 because
        we add 1 to the length of self.mazes, which is set after the id assignment

        Args:
            row (int): The height of the maze
            col (int): The width of the maze
            id (int):  The optional unique id of the maze.
        """
        self.mazes.append(Maze(row, col, objects, id))
        return self.mazes[-1]

    def get_maze(self, id):
        """Get a maze by its id.

            Args:
                id (int): The id of the desired maze

            Return:
                    Maze: Returns the maze if it was found.
                    None: If no maze was found
        """

        for maze in self.mazes:
            if maze.id == id:
                return maze
        #print("Unable to locate maze")
        return None

    def get_mazes(self):
        """Get all of the mazes that the manager is holding"""
        return self.mazes

    def get_maze_count(self):
        """Gets the number of mazes that the manager is holding"""
        return self.mazes.__len__()

    def check_matching_id(self, id):
        """Check if the id already belongs to an existing maze

        Args:
            id (int): The id to be checked

        Returns:

        """
        return next((maze for maze in self.mazes if maze .id == id), None)

    def set_filename(self, filename):
        """
        Sets the filename for saving animations and images
        Args:
            filename (string): The name of the file without an extension
        """

        self.media_name = filename

    def set_quiet_mode(self, enabled):
        """
        Enables/Disables the quiet mode
        Args:
            enabled (bool): True when quiet mode is on, False when it is off
        """
        self.quiet_mode=enabled
 
    def print_maze_to_console(self, id):
    
        maze_in_numbers = self.mazes[id-1].generate_maze_with_numbers()
        name = "lab"+str(id)+".txt"
        for i in range(len(maze_in_numbers)):
            line = []
            for j in range(len(maze_in_numbers[i])):
                #print(str(maze_in_numbers[i][j]), end=' ') #py3!!
                line.append( str(maze_in_numbers[i][j])) #py2.7
            print ' '.join(line)
        print str(id)
    
    def print_maze_to_str(self, id):
        mazestr = []
        maze_in_numbers = self.mazes[id-1].generate_maze_with_numbers()
        name = "lab"+str(id)+".txt"
        for i in range(len(maze_in_numbers)):
            line = []
            for j in range(len(maze_in_numbers[i])):
                line.append(str(maze_in_numbers[i][j]))
            mazestr.append(' '.join(line)+'\n')
        return ''.join(mazestr)+str(self.mazes[id-1].num_objects)+'\n'
        
    def gather_solution_from_console(self, id):
        solution = []
        
        for line in sys.stdin:
            if(line == "\n"):
                break
            solution.append(line)
            
        return solution
    
    def check_solution(self, solution, id):
        
        return self.mazes[id-1].check_solution(solution)
        
