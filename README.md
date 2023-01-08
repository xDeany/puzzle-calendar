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

Run `$ python3 main.py` and follow the command line prompts.

Results are saved to `.solutions/{MONTH}/{DATE}.csv` and, from there, can be loaded into a spreadsheet.
Conditional formatting can then be used to better display the solutions.

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
L   S   S   Oct P   P
L   2   S   T   T   T   T
C   C   S   S   T   O   O
C   J   J   J   J   O   O
C   C   Z   Z   J   O   O
Z   Z   Z
```

In the example above, the date left uncovered is October 2nd.

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
