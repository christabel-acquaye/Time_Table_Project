from .hard_constraints_def import get_total_hard_constraints_value
from .penalty_def import get_total_penalty_value


def get_fitness_value(chromosomes, params):
    restructured_chromosomes = []
    for chromosome in chromosomes:
        restructured_chromosome = {
            'data': chromosome,
            'soft_constraint': get_total_penalty_value(chromosome, params['threshold']),
            'hard_constraint': get_total_hard_constraints_value(chromosome)
        }
        restructured_chromosomes.append(restructured_chromosome)
    return restructured_chromosomes


if __name__ == "__main__":
    chromosomes = []
    params = []
    print(get_fitness_value(chromosomes, params))
