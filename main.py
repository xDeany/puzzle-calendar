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
MONTH="Jan"
DATE="8"

# Default behaviour is to only return the first solution the program finds
# Setting FIND_ALL_SOLUTIONS to True will make the algorithm perform an exhaustive search for all possible solutions
FIND_ALL_SOLUTIONS=False

def dfs(board: Board, pieces: List[Piece], states: Set[Board] = set(), solutions: Set[Board] = set()) -> Set[Board]:
    logging.debug(board)
    
    if len(pieces) == 0:
        # We placed all the pieces! Success!
        logging.info(str(datetime.datetime.now()))
        logging.info(board)
        solutions.add(board)
        return solutions
    
    targetTile = board.getTopLeft()
    logging.debug(f"top left tile: {targetTile}")
    
    # Scan over all tiles in the board
    for y, row in enumerate(board.tiles):
        for x, _ in enumerate(row):
            # Try and place each piece there
            for piece in pieces:
                # Try every rotation/reflection of the piece
                for perm in getPerms(piece):
                    if board.place(perm, Coord(x, y)):
                        # Ayyy we managed to fit it in
                        logging.debug(f"placed {perm.name}")
                        
                        # Check if this placement covered the top left most available tile
                        # This saves the program arbitrarily placing pieces in the middle of the board 
                        # with no way of them ever fitting together
                        if targetTile.piece is None:
                            logging.debug(f"failed to cover {targetTile}")
                            board.remove(perm)
                            continue
                        
                        # check if this created a dead region (e.g. a space too small to fit any pieces in)
                        if board.hasDeadSpace():
                            logging.debug(f"created deadspace")
                            board.remove(perm)
                            continue
                        
                        # check if we've seen this partial solution before
                        if board in states:
                            logging.debug(f"visited this state already")
                            board.remove(perm)
                            continue
                        
                        # this is a new, and valid partial soltuion
                        # track the new state for future reference
                        states.add(board)
                        
                        # make a copy of the pieces so we don't edit the original list
                        remainingPieces = pieces.copy() 
                        remainingPieces.remove(piece)
                        
                        # try to add the rest of the pieces
                        # keeping track of any solutions we find diving down this branch
                        solutions = dfs(board, remainingPieces, states, solutions)
                        
                        # if we only want the first solution, we can stop here
                        if len(solutions) == 1 and not FIND_ALL_SOLUTIONS:
                            return solutions
                        
                        # we've exhausted this option, remove the piece and continue on to the next
                        board.remove(perm)
                    
    # Return any solutions we found
    return solutions

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
    logging.info(f"Found {len(result)} solutions")
    
    # Record finish time & total time taken
    finish = datetime.datetime.now()
    logging.info(f"Finish time: {str(finish)}")
    logging.info(f"Time taken - {str(finish - start)}")
        

if __name__ == "__main__":
    main()
