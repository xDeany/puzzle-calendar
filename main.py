#!/usr/bin/python3

import numpy as np
from board import Board
from pieces import Coord, Piece, permutations
from tile import Tile



def main():
    b = Board([[Tile("Jan"), Tile("Feb"), Tile("Mar"), Tile("Apr"), Tile("May"), Tile("Jun")],
               [Tile("Jul"), Tile("Aug"), Tile("Sep"), Tile("Oct"), Tile("Nov"), Tile("Dec")],
               [Tile("1"),   Tile("2"),   Tile("3"),   Tile("4"),   Tile("5"),   Tile("6"),  Tile("7")],
               [Tile("8"),   Tile("9"),   Tile("10"),  Tile("11"),  Tile("12"),  Tile("13"), Tile("14")],
               [Tile("15"),  Tile("16"),  Tile("17"),  Tile("18"),  Tile("19"),  Tile("20"), Tile("21")],
               [Tile("22"),  Tile("23"),  Tile("24"),  Tile("25"),  Tile("26"),  Tile("27"), Tile("28")],
               [Tile("29"),  Tile("30"),  Tile("31")]])
    
    initialPieces = [
        Piece("L", [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(0, 1), Coord(0, 2)]),
        Piece("C", [Coord(0, 0), Coord(1, 0), Coord(0, 1), Coord(0, 2), Coord(1, 2)]),
        Piece("S", [Coord(1, 0), Coord(2, 0), Coord(1, 1), Coord(0, 2), Coord(1, 2)]),
        Piece("Z", [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(2, 1), Coord(3, 1)]),
        Piece("J", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3), Coord(1, 3)]),
        Piece("T", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3), Coord(1, 1)]),
        Piece("P", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 0), Coord(1, 1)]),
        Piece("O", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 0), Coord(1, 1), Coord(1, 2)])
    ]
    
    allPieces = dict()
    
    for piece in initialPieces:
        allPieces[piece.name] = permutations(piece)
        
    for letter, perms in allPieces.items():
        print(letter)
        for perm in perms:
            print(perm)
            print()
        print()
    

if __name__ == "__main__":
    main()
