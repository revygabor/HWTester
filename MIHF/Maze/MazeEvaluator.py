import Evaluator
from io import StringIO
import numpy as np
from MIHF.Maze.maze_manager import MazeManager

class MazeEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input, target_output, output, log):
        try:
            result =  input['mazemanager'].check_solution(output.split('\n'),input['mazeID'])
            if result[0] == True:
                return (1,result[1])
            else:
                return (0, result[1])
        except ValueError as err:
            return (0, err.message)
        except Exception as e:
            print "Exception:", e.message
            return (0, "Unknown error"+e.message)

