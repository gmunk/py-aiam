import random


def weight_by(population, fitness_function):
    return [fitness_function(i) for i in population]


def choose_parents(population, weights):
    return random.choices(population, weights, k=2)


def reproduce(first_parent, second_parent):
    c = random.randrange(0, len(first_parent))

    return [first_parent[:c] + second_parent[c:], second_parent[:c] + first_parent[c:]]


def mutate(individual, genes, mutation_rate):
    if random.uniform(0, 1) >= mutation_rate:
        return individual

    c = random.randrange(0, len(individual))
    g = random.choice(genes)

    return individual[:c] + g + individual[c + 1:]


def genetic_algorithm(population,
                      fitness_function,
                      genes,
                      culling_threshold=None,
                      fitness_threshold=None,
                      mutation_rate=0.1,
                      number_generations=100,
                      generation_size=1000):
    for _ in range(number_generations):
        weights = weight_by(population, fitness_function)
        next_generation = []

        while len(next_generation) < generation_size:
            children = [mutate(c, genes, mutation_rate) for c in reproduce(*choose_parents(population, weights))]

            if fitness_threshold:
                for c in children:
                    if fitness_function(c) >= fitness_threshold:
                        return c

            if culling_threshold:
                children = [c for c in children if fitness_function(c) >= culling_threshold]

            next_generation.extend(children)

        population = next_generation

    return max(population, key=fitness_function)
