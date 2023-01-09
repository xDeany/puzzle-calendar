#!/usr/bin/python3

import logging

from board import *


# Changing the logging level changes what information goes to the console
logging.basicConfig(level=logging.DEBUG)

# The default puzzle board
BOARD = Board([[Tile("Jan"), Tile("Feb"), Tile("Mar"), Tile("Apr"), Tile("May"), Tile("Jun")],
               [Tile("Jul"), Tile("Aug"), Tile("Sep"), Tile("Oct"), Tile("Nov"), Tile("Dec")],
               [Tile("1"),   Tile("2"),   Tile("3"),   Tile("4"),   Tile("5"),   Tile("6"),  Tile("7")],
               [Tile("8"),   Tile("9"),   Tile("10"),  Tile("11"),  Tile("12"),  Tile("13"), Tile("14")],
               [Tile("15"),  Tile("16"),  Tile("17"),  Tile("18"),  Tile("19"),  Tile("20"), Tile("21")],
               [Tile("22"),  Tile("23"),  Tile("24"),  Tile("25"),  Tile("26"),  Tile("27"), Tile("28")],
               [Tile("29"),  Tile("30"),  Tile("31")]])

# The default pieces we need to place in the board
PIECES: List[Piece] = [
    Piece("L", [Dir.DOWN, Dir.DOWN, Dir.RIGHT, Dir.RIGHT]),
    Piece("C", [Dir.LEFT, Dir.DOWN, Dir.DOWN, Dir.RIGHT]),
    Piece("S", [Dir.LEFT, Dir.DOWN, Dir.DOWN, Dir.LEFT]),
    Piece("Z", [Dir.RIGHT, Dir.RIGHT, Dir.DOWN, Dir.RIGHT]),
    Piece("J", [Dir.DOWN, Dir.DOWN, Dir.DOWN, Dir.LEFT]),
    Piece("P", [Dir.RIGHT, Dir.DOWN, Dir.LEFT, Dir.DOWN]),
    Piece("T", [Dir.DOWN, Dir.RIGHT, Dir.LEFT, Dir.DOWN, Dir.DOWN]),
    Piece("O", [Dir.RIGHT, Dir.DOWN, Dir.DOWN, Dir.LEFT, Dir.UP]),
]

# PIECES: List[Piece] = [
#     Piece("L", [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(0, 1), Coord(0, 2)]),
#     Piece("C", [Coord(0, 0), Coord(1, 0), Coord(0, 1), Coord(0, 2), Coord(1, 2)]),
#     Piece("S", [Coord(1, 0), Coord(2, 0), Coord(1, 1), Coord(0, 2), Coord(1, 2)]),
#     Piece("Z", [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(2, 1), Coord(3, 1)]),
#     Piece("J", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3), Coord(1, 3)]),
#     Piece("T", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3), Coord(1, 1)]),
#     Piece("P", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 0), Coord(1, 1)]),
#     Piece("O", [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 0), Coord(1, 1), Coord(1, 2)])
# ]

# def dfs(board: Board, pieces: List[Piece], numSolutions: int=1, states: Set[str] = set(), solutions: Set[str] = set()) -> Set[str]:
#     logging.debug(board)

#     if len(pieces) == 0:
#         # We placed all the pieces! Success!
#         logging.info(str(datetime.datetime.now()))
#         logging.info(board)
#         solutions.add(board.toString())
#         return solutions

#     targetTile = board.getTopLeft()
#     logging.debug(f"top left tile: {targetTile}")

#     # Scan over all tiles in the board
#     for y, row in enumerate(board.tiles):
#         for x, _ in enumerate(row):
#             # Try and place each piece there
#             for piece in pieces:
#                 # Try every rotation/reflection of the piece
#                 for perm in getPerms(piece):
#                     if board.place(perm, Coord(x, y)):
#                         # Ayyy we managed to fit it in
#                         logging.debug(f"placed {perm.name}")

#                         # make a copy of the pieces so we don't edit the original list
#                         remainingPieces = pieces.copy()
#                         remainingPieces.remove(piece)

#                         # Check if this placement covered the top left most available tile
#                         # This saves the program arbitrarily placing pieces in the middle of the board
#                         # with no way of them ever fitting together
#                         if targetTile.piece is None:
#                             logging.debug(f"failed to cover {targetTile}")
#                             board.remove(perm)
#                             continue

#                         # check if this created a dead region (e.g. a space too small to fit any pieces in)
#                         if board.hasDeadSpace(remainingPieces):
#                             logging.debug(f"created deadspace")
#                             board.remove(perm)
#                             continue

#                         # check if we've seen this partial solution before
#                         if board.toString() in states:
#                             logging.debug(f"visited this state already")
#                             board.remove(perm)
#                             continue

#                         # this is a new, and valid partial soltuion
#                         # track the new state for future reference
#                         states.add(board.toString())

#                         # try to add the rest of the pieces
#                         # keeping track of any solutions we find diving down this branch
#                         solutions = dfs(board, remainingPieces, numSolutions, states, solutions)

#                         # Stop when we reach the desired number of solutions
#                         # -1 will get the program to find _all_ solutions
#                         if len(solutions) == numSolutions:
#                             return solutions

#                         # we've exhausted this option, remove the piece and continue on to the next
#                         board.remove(perm)

#     # Return any solutions we found
#     return solutions

# def main(month: str="Jan", date: str="1", numSolutions: int=1):
#     # Place a * piece over the month/date to leave showing
#     BOARD.find(month)[0].piece = Piece("", [Coord(0,0)])
#     BOARD.find(date)[0].piece = Piece("", [Coord(0,0)])

#     # Record start time
#     logging.info(BOARD)
#     start = datetime.datetime.now()
#     logging.info(f"Start time: {str(start)}")

#     # GO GO GO
#     result = dfs(BOARD, PIECES, numSolutions)

#     # Print the result
#     logging.info(f"Found {len(result)} solutions")

#     # Record finish time & total time taken
#     finish = datetime.datetime.now()
#     logging.info(f"Finish time: {str(finish)}")
#     logging.info(f"Time taken - {str(finish - start)}")

#     # Store the solutions in csv file
#     solutionsDir = f".solutions/{month}"
#     solutionsFile = f"{solutionsDir}/{date}.csv"

#     if not os.path.exists(solutionsDir):
#         os.makedirs(solutionsDir)

#     with open(solutionsFile, "w") as fp:
#         fp.write(f"{len(result)},{str(finish - start)}\n")
#         for solution in result:
#             fp.writelines(toCsv(solution))

#     logging.info(f"Solutions saved to {solutionsFile}")


def main():
    print(BOARD)
    BOARD.updateNeighbours()
    print(BOARD.tiles[0][0].neigh)
    BOARD.place(BOARD.tiles[2][3], PIECES[0], Rot.NINETY, False)
    print(BOARD)
    # BOARD.remove(piece)
    
    # for piece in PIECES:
    #     for dir in Dir:
    #         for flipped in [True, False]:
    #             BOARD.place(BOARD.tiles[2][3], piece, dir, flipped)
    #             print(BOARD)
    #             BOARD.remove(piece)


if __name__ == "__main__":
    main()
