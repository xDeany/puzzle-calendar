#!/usr/bin/python3

from typing import List, Set
import numpy as np

class Coord:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class Piece:
    def __init__(self, name: str, coords: List[Coord]):
        self.name = name
        self.coords = coords
        self.matrix = self.toMatrix()
        self.matrices = self.toMatrices()

    def toMatrix(self) -> np.ndarray:
        maxX = 0
        maxY = 0
        for coord in self.coords:
            maxX = coord.x if coord.x > maxX else maxX
            maxY = coord.y if coord.y > maxY else maxY
        max = maxX if maxX > maxY else maxY
        
        result = np.zeros((max + 1, max + 1))
        for coord in self.coords:
            result[coord.y, coord.x] = 1
            
        return result
    
    def toMatrices(self) -> Set[str]:
        setM = {self.matrix.tostring()}
        ref = np.fliplr(self.matrix)
        setM.add(ref.tostring())
        
        for i in range(4):
                setM.add(np.rot90(self.matrix, i).tostring())
                setM.add(np.rot90(ref, i).tostring())
                
        result = []
        for m in setM:
            m: np.ndarray = np.fromstring(m)
            result.append(m.reshape(self.matrix.shape))
            
        return result
    
    def __repr__(self) -> str:
        return repr(self.matrix)

def permutations(p: Piece) -> List[Piece]:
    result = []
    for m in p.matrices:
        result.append(Piece(p.name, convert(m)))
    
    return result

def convert(m: np.ndarray) -> List[Coord]:
    result: List[Coord] = []
    mIndices = np.argwhere(m)
    for idx in mIndices:
        coord = Coord(y=idx[0], x=idx[1])
        result.append(coord)
    
    return result
