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

    def hasDeadSpace(self) -> bool:
        """True if there's a region of the board too small for a piece to be placed there (e.g. a single tile)"""
        self.updateNeighbours()
        regions = []
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
                if len(region) < 5:
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
                except IndexError:
                    pass

                try:
                    t2 = self.tiles[i-1][j]  # Scans across the ith row
                    if t2.piece is None:
                        return t2
                except IndexError:
                    pass
        return None  # The board is full

    def find(self, date: str) -> Tuple[Tile, Coord]:
        """Returns a Tile, and its Coord, based on the provided date"""
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile.date == date:
                    return tile, Coord(x, y)

        raise KeyError(f"{date} not found")

    def __hash__(self) -> int:
        """Flattens the board into a string and returns the hash of that string"""
        boardAsList = []
        for row in self.tiles:
            for tile in row:
                boardAsList.append(
                    tile.piece.name if tile.piece is not None and tile.piece.name != "" else tile.date)
        result = ','.join(boardAsList)
        return hash(result)

    def __repr__(self) -> str:
        """A nice print out version of the board"""
        result = "\n"
        for row in self.tiles:
            for tile in row:
                # Add a bit of padding for neatness
                result += repr(tile).ljust(4)
            result += "\n"
        return result
