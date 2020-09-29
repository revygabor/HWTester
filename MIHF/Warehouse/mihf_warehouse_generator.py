#!/usr/bin/python/
import sys
import random
import json
import math
#usage: python mihf_search_generator.py [startsize] [endsize] [stepsize]"
#psarkozy@mit.bme.hu

total_width = None
total_height = None

class Piece:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        

    def split(self):
        if self.width == 1 and self.height == 1:
            return None, None
        elif self.width == 1:
            return self.splitHorizontal()
        elif self.height == 1:
            return self.splitVertical()
        else:
            if random.random() > 0.5:
                return self.splitVertical()
            else:
                return self.splitHorizontal()

    def splitVertical(self):
        splitat = random.randint(1, self.width - 1)
        split_width_coordinate = self.x+self.width-splitat
        newpiece = Piece(splitat, self.height,split_width_coordinate,self.y)
        self.width -= splitat
        
        lower_bound = 0
        if self.y ==0:
            lower_bound = 1
        upper_bound = self.height
        if self.y + self.height == total_height:
            upper_bound = self.height -1
        pillar = (split_width_coordinate,self.y + random.randint(lower_bound, upper_bound))
        
        return newpiece, pillar

    def splitHorizontal(self):
        splitat = random.randint(1, self.height - 1)
        split_height_coordinate =  self.y+self.height-splitat
        newpiece = Piece(self.width, splitat, self.x,split_height_coordinate)
        self.height -= splitat
        
        #tricky
        lower_bound = 0
        if self.x ==0:
            lower_bound = 1
        upper_bound = self.width
        if self.x + self.width == total_width:
            upper_bound = self.width -1
        pillar = (self.x + random.randint(lower_bound, upper_bound),split_height_coordinate)
        
        return newpiece, pillar

    def rotate(self):
        temp   = self.width
        self.width = self.height
        self.height = temp




def createInput(width, height, desired_splits, desired_pillars):
    global total_width
    total_width = width
    global total_height
    total_height = height
    pieces = [Piece(width, height,0,0)]
    pillars = []
    current_splits = 0
    current_pillars = 0
    while current_splits < desired_splits:
        newpiece, pillar = random.choice(pieces).split()
        if newpiece is not None:
            pieces.append(newpiece)
            if current_pillars < desired_pillars:
                pillars.append(pillar)
                current_pillars +=1
            current_splits += 1
    for piece in pieces:
        if random.random > 0.5:
            piece.rotate()
    
    if width * height != sum([piece.width * piece.height for piece in pieces]):  #sanity check
        raise ValueError('Sanity check failed, sum of pieces not equal to total area!'+str(pieces))
    for pillar in pillars:
        if pillar[0] < 1 or pillar[0] >= total_width or pillar[1] < 1 or pillar[1] >= total_height:
            raise ValueError('Sanity check failed, a pillar is not on the inside of the warehouse!'+str(pillar) + 'with map ' + str((total_width,total_height)))
    combined = [(pillar[0], pillar[1]) for pillar in pillars] + [(piece.width, piece.height) for piece in pieces]
    return '%d\t%d\n%d\n%d\n%s\n' % (width, height,len(pillars), len(pieces), '\n'.join(['%d\t%d' % (piece[0], piece[1]) for piece in combined]))


if __name__ == "__main__":
    random.seed(1)
    startSize = 3
    stepSize = 3
    if len(sys.argv) >= 4:
        startSize, endSize, stepSize = map(int, tuple(sys.argv[1:4]))
    json_output = []
    
    
    for i in range(startSize, startSize + stepSize*12 +1, stepSize):
        inputstring = createInput(i, i, i*2,i)
        #print inputstring
        json_output.append({"input": inputstring, "target": ""})

    print json.dumps(json_output, separators=(',\n', ': '))
