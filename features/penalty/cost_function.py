import pprint

from .hard_constraints_def import get_total_hard_constraints_value
from .penalty_def import get_total_penalty_value


def get_fitness_value(chromosomes, params):
    """get the fitness value 1 and fitness value 2 or every chromosome in the
     population.

    Arguments:
        chromosome {List[dict]} -- chromosomes in a population
        params {dict} -- parameters data

    Returns:
        updated_chromosome {List[dict]}  -- chromosome with hard_constraints
        fitness value and soft_contraints fitness value attached.
    """
    restructured_chromosomes = []
    for chromosome in chromosomes:
        restructured_chromosome = {
            'data': chromosome,
            'soft_constraint': get_total_penalty_value(chromosome, params['threshold'],
                                                       params['reserved_periods']),
            'hard_constraint': get_total_hard_constraints_value(chromosome,
                                                                params['closed_periods'], params['reserved_periods'],
                                                                params['previous_chromosome'])
        }
        restructured_chromosomes.append(restructured_chromosome)

    return restructured_chromosomes


if __name__ == "__main__":
    chromosomes = []
    params = []
    print(get_fitness_value(chromosomes, params))
