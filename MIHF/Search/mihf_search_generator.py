#!/usr/bin/python/
import sys
import random
import json
#usage: python mihf_search_generator.py [startsize] [endsize] [stepsize]"
#psarkozy@mit.bme.hu



class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def split(self):
        if self.x == 1 and self.y == 1:
            return None
        elif self.x == 1:
            return self.splitY()
        elif self.y == 1:
            return self.splitX()
        else:
            if random.random() > 0.5:
                return self.splitX()
            else:
                return self.splitY()

    def splitX(self):
        splitat = random.randint(1, self.x - 1)
        newpiece = Piece(splitat, self.y)
        self.x -= splitat
        return newpiece

    def splitY(self):
        splitat = random.randint(1, self.y - 1)
        newpiece = Piece(self.x, splitat)
        self.y -= splitat
        return newpiece

    def rotate(self):
        temp   = self.x
        self.x = self.y
        self.y = temp


def createInput(x, y, desired_splits):
    pieces = [Piece(x, y)]
    current_splits = 0
    while current_splits < desired_splits:
        newpiece = random.choice(pieces).split()
        if newpiece is not None:
            pieces.append(newpiece)
            current_splits += 1
    for piece in pieces:
        if random.random > 0.5:
            piece.rotate()
    if x * y != sum([piece.x * piece.y for piece in pieces]):  #sanity check
        raise ValueError('Sanity check failed, sum of pieces not equal to total area!'+str(pieces))
    return '%d\t%d\n%d\n%s\n' % (x, y, len(pieces), '\n'.join(['%d\t%d' % (piece.x, piece.y) for piece in pieces]))

if __name__ == "__main__":
	random.seed(1)
	startSize = 3
	endSize = 31
	stepSize = 3
	if len(sys.argv) >= 4:
		startSize, endSize, stepSize = map(int, tuple(sys.argv[1:4]))
	json_output = []

	for i in range(startSize, endSize, stepSize):
		inputstring = createInput(i, i, i*2)
		#print inputstring
		json_output.append({"input": inputstring, "target": ""})

	print json.dumps(json_output, separators=(',\n', ': '))
