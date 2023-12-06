import random
from deap import base, creator, tools, algorithms
from datetime import datetime

tstart = datetime.now()
print(f"Start:{tstart}")

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
            'A': (8, 18),
            'B': (10, 16)
        },
        'restrictions': {
            'blue': [8, 9, 10],
            'red': [10, 11, 12]
        }
    },
    'Board 2': {
        'slots': {
            'A': (10, 18),
            'B': (10, 18)
        },
        'restrictions': {
            'green': [14, 15],
            'red': [12, 13, 14],
            'yellow': [8, 9, 10, 11]
        }
    },
    'Board 3': {
        'slots': {
            'A': (10, 18),
            'B': (10, 18),
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


def generate_individual():
    individual = []

    available_colors_by_board = {board_key: set(BLOCK_SIZES.keys()) for board_key in BOARDS.keys()}

    for board_key, board_info in BOARDS.items():
        board_colors = available_colors_by_board[board_key]
        for slot_key, slot_range in board_info['slots'].items():
            if not board_colors:
                return generate_individual()

            color = random.choice(list(board_colors))
            size = random.randint(BLOCK_SIZES[color].start, BLOCK_SIZES[color].stop - 1)

            individual.append((color, size))
            board_colors.remove(color)

    return individual



def evaluate(individual):
    total_score = 0
    index = 0

    for board_key, board_info in BOARDS.items():
        used_colors = set()
        empty_slots = 0  # Licznik pustych slotów na planszy
        for slot_key, slot_range in board_info['slots'].items():
            block_color, block_size = individual[index]

            if slot_range[1] - slot_range[0] >= block_size:
                total_score += 10  # Zwiększona nagroda za zapełnienie slotu

                # Kara za naruszenie ograniczeń kolorów
                if block_color in board_info['restrictions'] and any(
                    pos in board_info['restrictions'][block_color] for pos in range(slot_range[0], slot_range[1] + 1)):
                    total_score -= 10000

                # Kara za powtórzenie koloru na planszy
                if block_color in used_colors:
                    total_score -= 10000
                else:
                    used_colors.add(block_color)
            else:
                total_score -= 1000  # Kara za niezapełnienie slotu
                empty_slots += 1

            index += 1

        # Nagroda za wypełnienie wszystkich slotów na planszy
        if empty_slots == 0:
            total_score += 10000

    return total_score,




# Parametry algorytmu
NGEN = 5000
CX_PROB = 0.8
MUT_PROB = 0.3

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_block", lambda: random.choice(
    [(color, size) for color in BLOCK_SIZES for size in BLOCK_SIZES[color]]))

toolbox.register("individual", tools.initIterate, creator.Individual, generate_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def print_boards(solution):
    index = 0
    for board_key, board_info in BOARDS.items():
        print(f"{board_key}:")
        for slot_key, slot_range in board_info['slots'].items():
            print(f"\tSlot {slot_key}:")
            block_color, block_size = solution[index]

            for i in range(slot_range[0], slot_range[1] + 1):
                if i >= slot_range[0] and i < slot_range[0] + block_size:
                    print(f"\t\t{i}: {block_color.capitalize()}")
                else:
                    print(f"\t\t{i}: Empty")
            index += 1
        print("\n")


def main():
    random.seed(64)
    population = toolbox.population(n=300)

    NGEN = 50
    best_solutions = []

    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))

        top_individual = tools.selBest(population, k=1)[0]
        best_solutions.append(top_individual)

    return best_solutions


if __name__ == "__main__":
    best_solutions = main()
    best_score = float("-inf")
    best_solution = None

    for solution in best_solutions:
        score = evaluate(solution)[0]
        if score > best_score:
            best_solution = solution
            best_score = score

    if best_solution is not None:
        print("Best Solution:")
        print_boards(best_solution)

tsend = datetime.now()
print(f"Start:{tsend}")

time_diff = tsend - tstart
print(f"Total time: {time_diff}")