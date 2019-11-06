import Evaluator
from io import StringIO
import numpy as np
import sys

class SearchEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input, target_output, output, log):
        try:
            # read test case
            dims = (0,0)
            objects = []
            lines = input.split("\n")
            line = lines[0].split("\t")
            dims = (int(line[0]),int(line[1]))
            for i in range(2,len(lines)):
                o = lines[i].split("\t")
                if len(o) == 2:
                    objects.append((int(o[0]),int(o[1])))   
            # read data
           
			
            M = np.genfromtxt(StringIO(unicode(output, "utf-8")),int,delimiter='\t')
            
            # check size
            if M.shape != dims:
                return (0, "Size mismatch: should be ({0},{1}), found {2}, for input:\n\n {3} \nYour truncated output[:500] was: {4}".format(dims[0],dims[1],M.shape,input,output[:500]))
 
            # check objects
            for o in enumerate(objects):
                id = o[0]+1
                dx,dy = o[1]
                pos = np.argwhere(M==id)
                
                if dx*dy != len(pos):
            	    return (0,"Object {0} should occupy exactly {1} fields, found {2}, for input:\n\n {3}".format(id,dx*dy,len(pos),input))
                
                px0 = min(pos,key=lambda x: x[0])[0]-1
                px1 = max(pos,key=lambda x: x[0])[0]
                py0 = min(pos,key=lambda x: x[1])[1]-1
                py1 = max(pos,key=lambda x: x[1])[1]
                
                if (px1-px0 != dx or py1-py0 != dy) and (px1-px0 != dy or py1-py0 != dx):
            	    return (0,"Object size mismatch for object {0}: ({1},{2}) given, ({3},{4}) found, for input:\n\n {5}".format(id,dx,dy,px1-px0,py1-py0,input))

            return (1, "")

        except (ValueError, OverflowError) as err:
            return (0, "{0}\nfor input:\n\n {1}".format(err.message, input))
        except:
            print sys.exc_info()[0]
            return (0, "Unknown error:\n {0} \nfor input:\n\n {1}".format(sys.exc_info()[0], input))

