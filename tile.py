#!/usr/bin/python3

from pieces import Piece


class Tile:
    def __init__(self, date: str, piece: Piece=None):
        self.date = date
        self.piece = piece

    def __repr__(self) -> str:
        return self.piece.name.ljust(4) if self.piece is not None else self.date.ljust(4)
