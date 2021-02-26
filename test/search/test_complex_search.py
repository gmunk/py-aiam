from unittest import TestCase
from unittest.mock import patch, Mock, DEFAULT

from problem.problem import create_n_queens_states, calculate_non_attacking_pairs
from search.complex_search import weight_by, reproduce, mutate, genetic_algorithm


class GeneticAlgorithm(TestCase):
    def test_weight_by(self):
        population = ["1", "2"]
        expected_weights = [1, 2]
        mock_fitness_function = Mock(side_effect=expected_weights)

        weights = weight_by(population, mock_fitness_function)

        self.assertEqual(weights, expected_weights)

    def test_reproduce(self):
        fp, sp = "112233", "445566"
        e = ["112266", "445533"]
        c = 4

        with self.subTest(fp=fp, sp=sp, e=e, c=c):
            with patch("search.complex_search.random.randrange", return_value=c):
                self.assertEqual(reproduce(fp, sp), e)

    def test_mutate(self):
        individual = "0" * 8
        genes = [str(i) for i in range(8)]
        probability_mutation = 0.1

        test_data = [(0.09, 1, genes[1], "01000000"), (0.2, 1, genes[1], individual)]

        with patch.multiple("search.complex_search.random", uniform=DEFAULT, randrange=DEFAULT, choice=DEFAULT) as mocks:
            for pm, c, g, e in test_data:
                with self.subTest(pm=pm, c=c, g=g, e=e):
                    mock_rand_uniform, mock_rand_randrange, mock_rand_choice = \
                        mocks["uniform"], mocks["randrange"], mocks["choice"]
                    mock_rand_uniform.return_value = pm
                    mock_rand_randrange.return_value = c
                    mock_rand_choice.return_value = g

                    self.assertEqual(mutate(individual, genes, probability_mutation), e)

    def test_genetic_algorithm(self):
        n, p, ct, ft = 8, 100, 21, 28
        population = create_n_queens_states(n, p)

        state = genetic_algorithm(population,
                                  calculate_non_attacking_pairs,
                                  [str(i) for i in range(1, n + 1)],
                                  culling_threshold=ct,
                                  fitness_threshold=ft)

        self.assertEqual(calculate_non_attacking_pairs(state), ft)
