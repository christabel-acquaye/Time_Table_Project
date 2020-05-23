def non_dorminating_sort(chromosomes):
    domination_count = [0 for _ in range(chromosomes)]
    dominated_elements = [[] for _ in range(chromosomes)]

    dorminating_chromosomes = []
    non_dorminating_chromosomes = []

    """
        [A, B, C]
        A -> B, C
        B -> A, C
        C -> A, B
    """
    for reference_position, reference_chromosome in enumerate(chromosomes):
        for other_position, other_chromosome in enumerate(chromosomes):
            x1 = reference_chromosome['hard_constraint']
            x2 = other_chromosome['hard_constraint']

            y1 = reference_chromosome['soft_constraint']
            y2 = other_chromosome['soft_constraint']
            # (x1 <= x2 and y1 <= y2) and (x1 < x2 or y1 < y2)
            if ((x1 <= x2 and y1 <= y2) and (x1 < x2 or y1 < y2)):
                domination_count[reference_position] += 1
                dominated_elements[reference_position].append(other_position)
                dominated_elements[other_position] -= 1
            """
            if reference is dominant than other then
            domination_count[reference_position] += 1
            dominated_elements[reference_position].append(other_position)
            """

    return dorminating_chromosomes, non_dorminating_chromosomes


def over_crowding(non_dorminating_chromosomes):
    selected_chromosome = []
    return selected_chromosome


def get_first_generation_parents(dorminating_chromosomes, selected_chromosome):
    return dorminating_chromosomes, selected_chromosome


def natural_selection(population):
    """
    population = [
        {
            data: [{},{}],
            hard_contrainst: int,
            soft_constraint: int
        }
    ]
    """

    non_dominated_chromosomes = non_dominated_chromosomes(population)
