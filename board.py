#!/usr/bin/python3

from pieces import Coord, Piece
from typing import List, Dict

from tile import Tile

# Board = List[List[Tile]]

class Board:
    def __init__(self, tiles: List[List[Tile]]) -> None:
        self.tiles = tiles
        
    def place(self, p: Piece, dest: Coord) -> bool:
        """Places a piece with the yIdx & xIdx matching the upper left coord
        Returns false if the piece falls out of bounds
        """
        if not self.canPlace(p, dest):
            return False
        for coord in p.coords:
            self.tiles[dest.y + coord.y][dest.x + coord.x].piece = p
        
    def canPlace(self, p: Piece, dest: Coord) -> bool:
        """Checks if a piece can be places at the corresponding coordinate
        """
        # Bounds checking
        for coord in p.coords:
            try:
                self.tiles[dest.y + coord.y][dest.x + coord.x]
            except IndexError:
                return False
        return True

    def __repr__(self) -> str:
        result = "\n"
        for row in self.tiles:
            for tile in row:
                result += repr(tile)
            result += "\n"
        return result
