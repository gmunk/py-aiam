import random
from typing import Sequence, Callable


def weight_by(population: Sequence[str], fitness_function: Callable[[str], float]) -> list[float]:
    """Calculates weights for the individuals of an evolutionary algorithms population.

    Parameters
    ----------
    population : Sequence[str]
        Strings over a finite alphabet, representing a population of individuals.
    fitness_function : Callable[[str], float]
        Called for each individual, provides the weight or how fit this individual is.

    Returns
    -------
    list[float]
        The calculated weights of the population's members.
    """
    return [fitness_function(i) for i in population]


def choose_parents(population: Sequence[str], weights: Sequence[float]) -> list[str, str]:
    """Chooses two parents, based on their fitness score, which are going to create offspring for the next generation.

    Parameters
    ----------
    population : Sequence[str]
        Strings over a finite alphabet, representing a population of individuals.
    weights : Sequence[float]
        Numeric values, representing how fit each individual in population is.

    Returns
    -------
    list[str, str]
        Two individuals, selected based on probabilities derived from their weights.
    """
    return random.choices(population, weights, k=2)


def reproduce(first_parent: str, second_parent: str) -> list[str]:
    """Creates the offspring of the two parents passed as function arguments.

    This function achieves reproduction by using the common crossover method, where a
    crossover point is selected and the children are recombined based on that point.

    Parameters
    ----------
    first_parent : str
        First individual who is going to be a parent.
    second_parent : str
        Second individual who is going to be a parent.

    Returns
    -------
    list[str]
        The children of the two parents passed as function arguments.
    """
    c = random.randrange(0, len(first_parent))

    return [first_parent[:c] + second_parent[c:], second_parent[:c] + first_parent[c:]]


def mutate(individual: str, genes: Sequence[str], mutation_rate: float) -> str:
    """Mutates an individual according to a predetermined mutation rate.

    Mutation is based on the mutation rate, the larger it is, the more frequently it happens.
    Mutation works by randomly changing one of the genes of an individual.

    Parameters
    ----------
    individual : str
        An individual to be mutated.
    genes : Sequence[str]
        The gene pool from which all individuals are derived.
    mutation_rate : float
        Rate of mutation, determines how often a random gene is going to be mutated.

    Returns
    -------
    str
        An individual, either the same one that was passed or a mutated one.
    """
    if random.uniform(0, 1) >= mutation_rate:
        return individual

    c = random.randrange(0, len(individual))
    g = random.choice(genes)

    return individual[:c] + g + individual[c + 1:]


def genetic_algorithm(population: Sequence[str],
                      fitness_function: Callable[[str], float],
                      genes: Sequence[str],
                      culling_threshold: float = None,
                      fitness_threshold: float = None,
                      mutation_rate: float = 0.1,
                      number_generations: int = 100,
                      generation_size: int = 1000) -> str:
    """Implementation of a genetic algorithm.

    It relies on a fixed generation size and number of generations, the recombination procedure assumes
    a mixing number of 2 (which is actually hardcoded) and for best results it is recommended to use culling.

    Parameters
    ----------
    population : Sequence[str]
        Strings over a finite alphabet, representing a population of individuals.
    fitness_function : Callable[[str], float]
        Function which calculated the weight or how fit this individual is.
    genes : Sequence[str]
        The gene pool from which all individuals are derived.
    culling_threshold : float
        A threshold which determines whether an individual is going to be included in the next generation (if provided).
    fitness_threshold : float
        A threshold which determines when an individual is fit enough and is considered to be a solution (if provided).
    mutation_rate : float
        Rate of mutation, determines how often a random gene is going to be mutated.
    number_generations : int
        The number of generations for which the algorithm is going to run.
    generation_size : int
        The population size of each generation.

    Returns
    -------

    """
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
