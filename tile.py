#!/usr/bin/python3

from typing import List
from piece import Piece


class Tile:
    def __init__(self, date: str, piece: Piece = None, neigh: List = []):
        self.date = date
        self.piece = piece
        self.neigh = neigh

    def __repr__(self) -> str:
        """If uncovered, returns the date of the tile, else returns the name of the piece covering it."""
        return self.piece.name if self.piece is not None and self.piece.name != "" else self.date
