import random
from deap import base, creator, tools, algorithms
from datetime import datetime
import data as d

tstart = datetime.now()
print(f"Start:{tstart}")

# Parametry algorytmu
TOTAL_POPULATION = 5000
NGEN = 500
CX_PROB = 0.5
MUT_PROB = 0.01
TOURNSIZE = 8


def generate_individual():
    individual = []

    available_colors_by_board = {board_key: set(d.BLOCK_SIZES.keys()) for board_key in d.BOARDS.keys()}

    for board_key, board_info in d.BOARDS.items():
        board_colors = available_colors_by_board[board_key]
        for slot_key, slot_range in board_info['slots'].items():
            if not board_colors:
                return generate_individual()

            color = random.choice(list(board_colors))
            size = random.randint(d.BLOCK_SIZES[color].start, d.BLOCK_SIZES[color].stop - 1)

            individual.append((color, size))
            board_colors.remove(color)

    return individual


def evaluate(individual):
    total_score = 0
    index = 0

    for board_key, board_info in d.BOARDS.items():
        used_colors = set()
        empty_slots = 0  # Licznik pustych slotów na planszy
        for slot_key, slot_range in board_info['slots'].items():
            block_color, block_size = individual[index]

            if slot_range[1] - slot_range[0] >= block_size:
                total_score += 10  # Zwiększona nagroda za zapełnienie slotu

                # Kara za naruszenie ograniczeń kolorów
                if block_color in board_info['restrictions'] and any(
                        pos in board_info['restrictions'][block_color] for pos in
                        range(slot_range[0], slot_range[1] + 1)):
                    total_score -= 100000

                # Kara za powtórzenie koloru na planszy
                if block_color in used_colors:
                    total_score -= 10000000
                else:
                    used_colors.add(block_color)
            else:
                total_score -= 10000000  # Kara za niezapełnienie slotu
                empty_slots += 1

            index += 1

        # Nagroda za wypełnienie wszystkich slotów na planszy
        if empty_slots == 0:
            total_score += 10000

    return total_score,


def mutate_individual(individual):
    mutation_idx = random.randrange(len(individual))
    mutation_choice = random.choice(["color", "size", "both"])

    if mutation_choice == "color":
        new_color = random.choice(list(d.BLOCK_SIZES.keys()))
        individual[mutation_idx] = (new_color, individual[mutation_idx][1])
    elif mutation_choice == "size":
        color = individual[mutation_idx][0]
        new_size = random.randint(d.BLOCK_SIZES[color].start, d.BLOCK_SIZES[color].stop - 1)
        individual[mutation_idx] = (color, new_size)
    elif mutation_choice == "both":
        new_color = random.choice(list(d.BLOCK_SIZES.keys()))
        new_size = random.randint(d.BLOCK_SIZES[new_color].start, d.BLOCK_SIZES[new_color].stop - 1)
        individual[mutation_idx] = (new_color, new_size)

    return individual,


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_block", lambda: random.choice(
    [(color, size) for color in d.BLOCK_SIZES for size in d.BLOCK_SIZES[color]]))

toolbox.register("individual", tools.initIterate, creator.Individual, generate_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate_individual)
toolbox.register("select", tools.selTournament, tournsize=TOURNSIZE)


def print_boards(solution):
    index = 0
    for board_key, board_info in d.BOARDS.items():
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
    population = toolbox.population(n=TOTAL_POPULATION)

    best_solutions = []

    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=CX_PROB, mutpb=MUT_PROB)
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
