BLOCK_SIZES = {
    'yellow': range(4, 9),
    'green': range(2, 9),
    'blue': range(4, 8),
    'red': range(3, 10),
    'grey': range(5, 10)
}

BOARDS = {
    'Board 1': {
        'slots': {
            'A': (8, 17),
            'B': (10, 15)
        },
        'restrictions': {
            'blue': [8, 9, 10],
            'red': [10, 11, 12]
        }
    },
    'Board 2': {
        'slots': {
            'A': (10, 17),
            'B': (10, 17)
        },
        'restrictions': {
            'green': [14, 15],
            'red': [12, 13, 14],
            'yellow': [8, 9, 10, 11]
        }
    },
    'Board 3': {
        'slots': {
            'A': (10, 17),
            'B': (10, 17),
            'C': (12, 17)
        },
        'restrictions': {
            'grey': [12, 13],
            'red': [17, 18, 19],
            'yellow': [14, 15, 16]
        }
    },
}

NUM_BOARDS = len(BOARDS)
MAX_SLOTS = 5