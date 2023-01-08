# puzzle-calendar

Program to solve the [DragonFjord puzzle-a-day](https://www.dragonfjord.com/product/a-puzzle-a-day/)

## Installation

Requires `python3` installed.
All dependencies listed in `requirements.txt`.

On linux/WSL, to setup in a virtualenv:

```bash
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Execution

1. Edit the `MONTH` and `DATE` in `main.py` to whatever spaces should be left uncovered
2. Run `$ python3 main.py`

### Exhaustive Search

Change `FIND_ALL_SOLUTIONS` to `True` to have the program perform an exhaustive search for all the possible solutions.

**warning:** may take minutes or even hours to complete

## Understanding the solution

The empty board looks like this

```
Jan Feb Mar Apr May Jun
Jul Aug Sep Oct Nov Dec
1   2   3   4   5   6   7
8   9   10  11  12  13  14
15  16  17  18  19  20  21
22  23  24  25  26  27  28
29  30  31
```

The output will look similar to the following

```
L   L   L   P   P   P
L   S   S   *   P   P
L   *   S   T   T   T   T
C   C   S   S   T   O   O
C   J   J   J   J   O   O
C   C   Z   Z   J   O   O
Z   Z   Z
```

`*` represents the squares left "uncovered". In the example above, that would be October 2nd

Each of the letters represents the spaces covered by different pieces. Each piece _sort of_ looks like a different letter. e.g. the `L` piece has the shape of an L, but may be oriented differently

So:
```
L
L
L   L   L
```

can also be rotated to
```
L   L   L
L
L
```
