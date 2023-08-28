#!/usr/bin/env python3

puzzle_types = {
    'basic': 'basic.py',
    'quad marks': 'quadmarks.py',
    'odd-even': 'oddeven.py',
    'wraparound': 'jigsaw.py',
    'blackout': 'blackout.py',
    'touchy': None,
    'jigsaw': 'jigsaw.py',
    'outsider': None,
    'consecutive': 'consecutive.py',
    'kropki': None,
    'inequality': None,
    'slashed': None,
    'trio': None,
    'xv': None,
    'arrows': None,
    'thermometer': 'lines.py',
    'frame': None,
    'cornered': None,
    'little killer': None
}

print()
print(f'{len(puzzle_types)} different types of puzzles with some overlap')

for k,v in puzzle_types.items():
    if v is not None:
        print(f' {k:20s} {v}')
    else:
        print(f' {k:20s} ...')
print()

