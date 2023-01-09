#!/usr/bin/python3

from enum import Enum
import logging
from typing import Dict, List, Set, Tuple


logging.basicConfig(level=logging.DEBUG)

class Dir(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
class Rot(Enum):
    ZERO = 0
    NINETY = 1
    ONE_EIGHTY = 2
    TWO_SEVENTY = 3

class Piece:
    def __init__(self, name: str, path: List[Dir]):
        self.name = name
        self.path = path


class Tile:
    def __init__(self, date: str, piece: Piece = None, neigh: Dict = {}):
        self.date = date
        self.piece = piece
        self.neigh = neigh

    def __repr__(self) -> str:
        """If uncovered, returns the date of the tile, else returns the name of the piece covering it."""
        return self.piece.name if self.piece is not None and self.piece.name != "" else self.date

class Board:
    placed: Set[str] = set()
    
    def __init__(self, tiles: List[List[Tile]]) -> None:
        self.tiles = tiles

    # def place(self, p: Piece, dest: Coord) -> bool:
    #     """Tries to place the piece at the destination
    #     The top left coordinate of the piece will be on top of the destination coordinate
    #     Returns true if successful
    #     """
    #     if not self.canPlace(p, dest):
    #         return False
    #     for coord in p.coords:
    #         self.tiles[dest.y + coord.y][dest.x + coord.x].piece = p
    #     return True

    # def canPlace(self, p: Piece, dest: Coord) -> bool:
    #     """Checks if a piece can be placed at the corresponding coordinate"""
    #     for coord in p.coords:
    #         try:
    #             target = self.tiles[dest.y + coord.y][dest.x + coord.x]
    #             if target.piece != None:
    #                 # There's already a piece there
    #                 return False
    #         except IndexError:
    #             # Out of bounds
    #             return False
    #     return True
    
    
    def place(self, tile: Tile, piece: Piece, rotation: Rot, flipped: bool) -> bool:
        if piece.name in self.placed:
            logging.debug(f"already placed {piece.name}")
            return False # Each piece can only be placed once
        toCover = []
        toCover.append(tile)
        try:
            for step in piece.path:
                dir = (step.value + rotation.value) % 4
                if flipped:  # If flipped, swap left and right
                    if dir == Dir.LEFT.value or dir == Dir.RIGHT.value:
                        dir = (dir + 2) % 4

                logging.debug(f"next direction: {dir}")
                tile = tile.neigh[dir]
                toCover.append(tile)
        except KeyError:  # Out of bounds
            logging.debug("out of bounds")
            return False
        
        
        logging.debug(f"planning to cover: {toCover}")

        for tile in toCover:
            if tile.piece != None and tile.piece != piece:
                # At least one of the target tiles has a piece on it already
                # Also, for the 'T' piece, the path loops back over itself, hence the extra check
                # Pieces can also only be placed once, so allowing a piece to "overlap" itself is fine
                return False

        for tile in toCover:
            tile.piece = piece
        self.placed.add(piece.name)

    def remove(self, piece: Piece):
        """Removes a piece from all the tiles that it covers"""
        logging.debug(f"removing {piece.name}...")
        for row in self.tiles:
            for tile in row:
                if tile.piece is not None and tile.piece.name == piece.name:
                    tile.piece = None
        self.placed.discard(piece.name)

    def updateNeighbours(self):
        """Updates all tiles with pointers to their neighbours"""
        for rowIdx, row in enumerate(self.tiles):
            for colIdx, tile in enumerate(row):
                tile.neigh = self.getNeighbours(rowIdx, colIdx)

    def getNeighbours(self, tileRow: int, tileCol: int) -> List[Tile]:
        """Gets the immediate neighbours of a tile"""
        result = {}
        dirs = {
            Dir.UP: (-1, 0),
            Dir.RIGHT: (0, 1),
            Dir.DOWN: (1, 0),
            Dir.LEFT: (0, -1),
        }
        for direction, adjustment in dirs.items():
            try:
                newRow = tileRow + adjustment[0]
                newCol = tileCol + adjustment[1]
                if newRow == -1 or newCol == -1:
                    continue  # Otherwise it wraps around to the other end of the array
                result[direction.value] = self.tiles[newRow][newCol]
            except IndexError:
                continue
        return result

    def __repr__(self) -> str:
        """A nice print out version of the board"""
        result = "\n"
        for row in self.tiles:
            for tile in row:
                # Add a bit of padding for neatness
                result += repr(tile).ljust(4)
            result += "\n"
        return result



    # def region(self, tile: Tile, path: set = set()) -> set:
    #     """Creates a set of all uncovered tiles adjacent to the provided tile (similar to minesweeper when you click an empty region)"""
    #     # Add current tile to the path
    #     path.add(tile)

    #     for t in tile.neigh:
    #         if t not in path:
    #             # Continue finding the region from here, merging the rest of the path
    #             path.union(self.region(t, path))

    #     return path

    # def hasDeadSpace(self, pieces: List[Piece]) -> bool:
    #     """True if there's a region of the board too small for a piece to be placed there (e.g. a single tile)"""
    #     self.updateNeighbours()
    #     regions = []

    #     # The O piece is the only one that has an area of 6
    #     # If that's been placed already, we can be smarter with the maths
    #     # Likewise, if that's the only piece left, the area remaining must be 6
    #     hasOPiece = False
    #     for p in pieces:
    #         hasOPiece = hasOPiece or p.name == "O"

    #     for row in self.tiles:
    #         for tile in row:
    #             if tile.piece is not None:
    #                 continue  # Covered by a piece, continue

    #             alreadyChecked = False
    #             for coveredRegion in regions:
    #                 alreadyChecked = alreadyChecked or tile in coveredRegion

    #             if alreadyChecked:
    #                 continue

    #             region = self.region(tile, set())
    #             regions.append(region)

    #             if not hasOPiece:
    #                 # All the pieces left are of size 5
    #                 # So each region has to be a multiple of 5
    #                 if len(region) % 5 != 0:
    #                     return True
    #             elif len(pieces) == 1:
    #                 # Only the O piece is remaining, so the remaining area has to be 6
    #                 if len(region) != 6:
    #                     return True

    #             # Else we have a mix of pieces and can't prune as well
    #             validAreas = [5, 6, 10, 11, 12, 15, 16, 17, 18] # all perms of 5 or 6 up to 20 (after that all areas are okay)
    #             if len(region) < 20 and len(region) not in validAreas:
    #                 return True
    #     return False

    # def getTopLeft(self) -> Tile:
    #     """Gets the top left most tile that isn't covered by a piece"""
    #     for i in range(7):  # Max board index + 1
    #         for j in range(i):
    #             try:
    #                 t1 = self.tiles[j][i-1]  # Scans down the ith column
    #                 if t1.piece is None:
    #                     return t1
    #             except IndexError: # Out of bounds
    #                 pass

    #             try:
    #                 t2 = self.tiles[i-1][j]  # Scans across the ith row
    #                 if t2.piece is None:
    #                     return t2
    #             except IndexError: # Out of bounds
    #                 pass
    #     return None  # The board is full

    # def find(self, date: str) -> Tuple[Tile, Coord]:
    #     """Returns a Tile, and its Coord, based on the provided date"""
    #     for y, row in enumerate(self.tiles):
    #         for x, tile in enumerate(row):
    #             if tile.date == date:
    #                 return tile, Coord(x, y)

    #     raise KeyError(f"{date} not found")

    # def toString(self) -> str:
    #     """Flattens the board into a string"""
    #     boardAsList = []
    #     for row in self.tiles:
    #         for tile in row:
    #             boardAsList.append(
    #                 tile.piece.name if tile.piece is not None and tile.piece.name != "" else tile.date)
    #     result = ','.join(boardAsList)
    #     return result

    # def __hash__(self) -> int:
    #     """Flattens the board into a string and returns the hash of that string"""
    #     return hash(self.toString())

# def toCsv(board: str) -> List[str]:
#     """Converts a string version of a board into a csv representation"""
#     boardAsList = board.split(",")
#     # Annoyingly, the board is of a weird shape
#     # rowLens = [6,6,7,7,7,7,3]
#     result = []
#     boardAsListList = [
#         boardAsList[0:6],
#         boardAsList[6:12],
#         boardAsList[12:19],
#         boardAsList[19:26],
#         boardAsList[26:33],
#         boardAsList[33:40],
#         boardAsList[40:]
#     ]
#     for row in boardAsListList:
#         csvLine = ",".join(row)
#         csvLine += "\n"
#         result.append(csvLine)
#     result.append("\n")
#     return result
