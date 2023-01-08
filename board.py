#!/usr/bin/python3

from piece import Coord, Piece
from typing import List, Tuple

from tile import Tile
import logging


class Board:
    def __init__(self, tiles: List[List[Tile]]) -> None:
        self.tiles = tiles

    def place(self, p: Piece, dest: Coord) -> bool:
        """Tries to place the piece at the destination
        The top left coordinate of the piece will be on top of the destination coordinate
        Returns true if successful
        """
        if not self.canPlace(p, dest):
            return False
        for coord in p.coords:
            self.tiles[dest.y + coord.y][dest.x + coord.x].piece = p
        return True

    def canPlace(self, p: Piece, dest: Coord) -> bool:
        """Checks if a piece can be placed at the corresponding coordinate"""
        for coord in p.coords:
            try:
                target = self.tiles[dest.y + coord.y][dest.x + coord.x]
                if target.piece != None:
                    # There's already a piece there
                    return False
            except IndexError:
                # Out of bounds
                return False
        return True

    def updateNeighbours(self):
        """Updates all tiles with pointers to their uncovered neighbours"""
        for row in self.tiles:
            for tile in row:
                if tile.piece != None:
                    # Tile has a piece on it, so it has no neighbours
                    tile.neigh = []
                    continue
                tile.neigh = self.getNeighbours(tile)

    def getNeighbours(self, tile: Tile) -> List[Tile]:
        """Gets the immediate uncovered neighbours of a tile"""
        result = []
        diffs = [1, -1]
        _, coord = self.find(tile.date)
        for diffY in diffs:
            newY = coord.y + diffY
            if newY == -1:
                continue
            try:
                neigh = self.tiles[newY][coord.x]
                if neigh.piece == None:
                    result.append(neigh)
            except IndexError:
                continue

        for diffX in diffs:
            newX = coord.x + diffX
            if newX == -1:
                continue
            try:
                neigh = self.tiles[coord.y][newX]
                if neigh.piece == None:
                    result.append(neigh)
            except IndexError:
                continue
        return result

    def region(self, tile: Tile, path: set = set()) -> set:
        """Creates a set of all uncovered tiles adjacent to the provided tile (similar to minesweeper when you click an empty region)"""
        # Add current tile to the path
        path.add(tile)

        for t in tile.neigh:
            if t not in path:
                # Continue finding the region from here, merging the rest of the path
                path.union(self.region(t, path))

        return path

    def remove(self, piece: Piece):
        """Removes a piece from all the tiles that it covers"""
        logging.debug(f"removing {piece.name}...")
        for row in self.tiles:
            for tile in row:
                if tile.piece is not None and tile.piece.name == piece.name:
                    tile.piece = None

    def hasDeadSpace(self, pieces: List[Piece]) -> bool:
        """True if there's a region of the board too small for a piece to be placed there (e.g. a single tile)"""
        self.updateNeighbours()
        regions = []
        
        # The O piece is the only one that has an area of 6
        # If that's been placed already, we can be smarter with the maths
        # Likewise, if that's the only piece left, the area remaining must be 6
        hasOPiece = False
        for p in pieces:
            hasOPiece = hasOPiece or p.name == "O"
        
        for row in self.tiles:
            for tile in row:
                if tile.piece is not None:
                    continue  # Covered by a piece, continue

                alreadyChecked = False
                for coveredRegion in regions:
                    alreadyChecked = alreadyChecked or tile in coveredRegion

                if alreadyChecked:
                    continue

                region = self.region(tile, set())
                regions.append(region)
                
                if not hasOPiece:
                    # All the pieces left are of size 5
                    # So each region has to be a multiple of 5
                    if len(region) % 5 != 0:
                        return True
                elif len(pieces) == 1:
                    # Only the O piece is remaining, so the remaining area has to be 6
                    if len(region) != 6:
                        return True
                    
                # Else we have a mix of pieces and can't prune as well
                validAreas = [5, 6, 10, 11, 12, 15, 16, 17, 18] # all perms of 5 or 6 up to 20 (after that all areas are okay)
                if len(region) < 20 and len(region) not in validAreas:
                    return True
        return False

    def getTopLeft(self) -> Tile:
        """Gets the top left most tile that isn't covered by a piece"""
        for i in range(7):  # Max board index + 1
            for j in range(i):
                try:
                    t1 = self.tiles[j][i-1]  # Scans down the ith column
                    if t1.piece is None:
                        return t1
                except IndexError: # Out of bounds
                    pass

                try:
                    t2 = self.tiles[i-1][j]  # Scans across the ith row
                    if t2.piece is None:
                        return t2
                except IndexError: # Out of bounds
                    pass
        return None  # The board is full

    def find(self, date: str) -> Tuple[Tile, Coord]:
        """Returns a Tile, and its Coord, based on the provided date"""
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile.date == date:
                    return tile, Coord(x, y)

        raise KeyError(f"{date} not found")
    
    def toString(self) -> str:
        """Flattens the board into a string"""
        boardAsList = []
        for row in self.tiles:
            for tile in row:
                boardAsList.append(
                    tile.piece.name if tile.piece is not None and tile.piece.name != "" else tile.date)
        result = ','.join(boardAsList)
        return result
        

    def __hash__(self) -> int:
        """Flattens the board into a string and returns the hash of that string"""
        return hash(self.toString())

    def __repr__(self) -> str:
        """A nice print out version of the board"""
        result = "\n"
        for row in self.tiles:
            for tile in row:
                # Add a bit of padding for neatness
                result += repr(tile).ljust(4)
            result += "\n"
        return result
    
def toCsv(board: str) -> List[str]:
    """Converts a string version of a board into a csv representation"""
    boardAsList = board.split(",")
    # Annoyingly, the board is of a weird shape
    # rowLens = [6,6,7,7,7,7,3]
    result = []
    boardAsListList = [
        boardAsList[0:6],
        boardAsList[6:12],
        boardAsList[12:19],
        boardAsList[19:26],
        boardAsList[26:33],
        boardAsList[33:40],
        boardAsList[40:]
    ]
    for row in boardAsListList:
        csvLine = ",".join(row)
        csvLine += "\n"
        result.append(csvLine)
    result.append("\n")
    return result
