#!/usr/bin/python3

import datetime
from typing import List, Set
from board import Board
from piece import Coord, Piece, getPerms
from tile import Tile
import logging

# Changing the logging level changes what information goes to the console vs stdout
logging.basicConfig(level=logging.INFO)

# These could be user input, but then I can't do 'python3 main.py > out.txt' without extra work
MONTH="Oct"
DATE="2"

def dfs(board: Board, pieces: List[Piece], states: Set[Board] = set()) -> Board:
    logging.debug(board)
    
    if len(pieces) == 0:
        # We placed all the pieces! Success!
        return board
    
    targetTile = board.getTopLeft()
    logging.debug(f"top left tile: {targetTile}")
    
    for y, row in enumerate(board.tiles):
        for x, _ in enumerate(row):
            # Try and place each piece there
            for piece in pieces:
                for perm in getPerms(piece):
                    if board.place(perm, Coord(x, y)):
                        # Ayyy we managed to fit it in
                        logging.debug(f"placed {perm.name}")
                        
                        # Check if this placement covered the top left most available tile
                        if targetTile.piece is None:
                            logging.debug(f"failed to cover {targetTile}")
                            board.remove(perm)
                            continue
                        
                        # check if this created a dead region
                        if board.hasDeadSpace():
                            logging.debug(f"created deadspace")
                            board.remove(perm)
                            continue
                        
                        # check if we've seen this before
                        if board in states:
                            logging.debug(f"visited this state already")
                            board.remove(perm)
                            continue
                        
                        # track the new state
                        states.add(board)
                        
                        # make a copy of the pieces so we don't edit the original list
                        remainingPieces = pieces.copy() 
                        remainingPieces.remove(piece)
                        
                        # try to add the rest of the pieces
                        result = dfs(board, remainingPieces, states)
                        
                        # if that worked, return the solution up the chain
                        if result is not None:
                            return result
                        
                        # Else, we couldn't solve the rest from here so remove whatever we just placed
                        # and try another permuation/piece
                        board.remove(perm)
                    
    # We failed to place any more pieces, go back a step!
    return None

def main():
    # The puzzle board
    b = Board([[Tile("Jan"), Tile("Feb"), Tile("Mar"), Tile("Apr"), Tile("May"), Tile("Jun")],
               [Tile("Jul"), Tile("Aug"), Tile("Sep"), Tile("Oct"), Tile("Nov"), Tile("Dec")],
               [Tile("1"),   Tile("2"),   Tile("3"),   Tile("4"),   Tile("5"),   Tile("6"),  Tile("7")],
               [Tile("8"),   Tile("9"),   Tile("10"),  Tile("11"),  Tile("12"),  Tile("13"), Tile("14")],
               [Tile("15"),  Tile("16"),  Tile("17"),  Tile("18"),  Tile("19"),  Tile("20"), Tile("21")],
               [Tile("22"),  Tile("23"),  Tile("24"),  Tile("25"),  Tile("26"),  Tile("27"), Tile("28")],
               [Tile("29"),  Tile("30"),  Tile("31")]])
    
    # The pieces we need to place in the board
    pieces = [
        Piece("L", [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(0, 1), Coord(0, 2)]),
        Piece("C", [Coord(0, 0), Coord(1, 0), Coord(0, 1), Coord(0, 2), Coord(1, 2)]),
        Piece("S", [Coord(1, 0), Coord(2, 0), Coord(1, 1), Coord(0, 2), Coord(1, 2)]),
        Piece("Z", [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(2, 1), Coord(3, 1)]),
        Piece("J", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3), Coord(1, 3)]),
        Piece("T", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3), Coord(1, 1)]),
        Piece("P", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 0), Coord(1, 1)]),
        Piece("O", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 0), Coord(1, 1), Coord(1, 2)])
    ]
    
    # Place a * piece over the month/date to leave showing
    b.find(MONTH)[0].piece = Piece("*", [Coord(0,0)])
    b.find(DATE)[0].piece = Piece("*", [Coord(0,0)])
    
    # Record start time
    logging.info(b)
    start = datetime.datetime.now()
    logging.info(f"Start time: {str(start)}")
    
    # GO GO GO
    result = dfs(b, pieces)
    
    # Print the result
    logging.info(result)
    
    # Record finish time & total time taken
    finish = datetime.datetime.now()
    logging.info(f"Finish time: {str(finish)}")
    logging.info(f"Time taken - {str(finish - start)}")
        

if __name__ == "__main__":
    main()
