from __future__ import absolute_import
from maze_manager import MazeManager


if __name__ == "__main__":

    # Create the manager
    manager = MazeManager()
    
    #sorszám,oszlopszám,id=tárgy szám
    # manager.add_maze(10,10,1)
    # manager.add_maze(20,20,2)
    # manager.add_maze(30,30,3)
    # manager.add_maze(40,40,4)
    # manager.add_maze(50,50,5)
    # manager.add_maze(100,5,6)
    # manager.add_maze(100,5,7)
    # manager.add_maze(100,5,8)
    # manager.add_maze(100,5,9)
    # manager.add_maze(100,5,10)
    # manager.add_maze(100,5,11)
    # manager.add_maze(100,5,12)
    # manager.add_maze(100,5,13)
    # manager.add_maze(100,5,14)
    # manager.add_maze(100,5,15)
    
    for i in range(1, 16):
        manager.add_maze(10*i,10*i,i)
    
    point = 0
    for i in range(1,16):
        manager.print_maze_to_console(i)
        solution = manager.gather_solution_from_console(i)
        okay = True
        
        okay = manager.check_solution(solution,i)
        if okay:
            point += 1
        else:
            #print(str(i)+". labirintusban elakadtál!\n\n")
            break
        
    #print(str(point)+" pontot szereztél!\n")
            
            
