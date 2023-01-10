#!/usr/bin/python3

from typing import List, Tuple
import numpy as np

Coord = Tuple[int, int]

class Piece:
    def __init__(self, name: str = "", coords: List[Coord] = [], matrix: np.ndarray = None):
        """Initialises the piece. If coords provided, a matrix will be auto generated and vice versa"""
        self.name = name
        self.coords = coords if coords != [] else toCoords(matrix)
        self.matrix = matrix if matrix is not None else toMatrix(coords)

    def __repr__(self) -> str:
        """Printing the piece's matrix so it's easier to see its shape"""
        return repr(self.matrix)


def toCoords(matrix: np.ndarray) -> List[Coord]:
    """Helper function. Generates a list of coordinates from a matrix."""
    result = []

    # Get the indexes of all non-zero values in the matrix
    mIndices = np.argwhere(matrix)

    # Create a Coord object from each index
    for idx in mIndices:
        coord = (idx[0], idx[1])
        result.append(coord)

    return result


def toMatrix(coords: List[Coord]) -> np.ndarray:
    """Helper function. Generates a matrix from a list of coordinates."""
    # Set the matrix size to the largest x & y values
    # This ensures the piece will fit in the resulting matrix
    maxX = 0
    maxY = 0
    for coord in coords:
        maxY = coord[0] if coord[0] > maxY else maxY
        maxX = coord[1] if coord[1] > maxX else maxX
    max = maxX if maxX > maxY else maxY

    # Initialise a zero matrix of that size
    result = np.zeros((max + 1, max + 1))

    # Set each coordinate to a '1' in the matrix
    for coord in coords:
        result[coord[0], coord[1]] = 1

    return result


def getPerms(p: Piece) -> List[Piece]:
    """Generates all rotations & reflection permutations of a piece as new pieces"""

    matrices = []

    for i in range(4):
        # Rotate the piece
        rotated = np.rot90(p.matrix, i)
        matrices.append(rotated)

        # Flip the rotated piece
        flipped = np.fliplr(rotated)
        matrices.append(flipped)

    # The way the matrices are rotated sometimes leaves empty space
    # This trims those spaces out
    # i.e. the '0' columns and rows are removed
    # [['0', '0'],
    #  ['0', '1'],         [['1'],
    #  ['0', '1']] becomes  ['1']]
    trimmedMatrices = []
    for matrix in matrices:
        matrix = matrix[~np.all(matrix == 0, axis=1)]  # Remove empty rows
        matrix = np.delete(matrix, np.where(~matrix.any(axis=0))[
                           0], axis=1)  # Remove empty colls
        trimmedMatrices.append(matrix)

    # Remove duplicate results (happens if the piece has rotational symmetry)
    uniqueMatrices = removeDuplicates(trimmedMatrices)

    # Convert matrices to pieces
    result = []
    for matrix in uniqueMatrices:
        result.append(Piece(p.name, [], matrix))

    return result


def removeDuplicates(matrices: List[np.ndarray]) -> List[np.ndarray]:
    """Helper function. Removes duplicate matrices from a list"""
    result = []
    for matrixA in matrices:
        unique = True
        for matrixB in result:
            # If a matrix of the same elements and size is already in result, skip
            if np.array_equal(matrixA, matrixB):
                unique = False
        if unique:
            result.append(matrixA)

    return result
