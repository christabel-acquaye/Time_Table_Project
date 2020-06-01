import math


def non_dorminating_sort(chromosomes):
    """
        [A, B, C]
        A -> B, C
        B -> A, C
        C -> A, B
    """

    domination_count = [0 for i in range(len(chromosomes))]
    dominated_elements = [[] for i in range(len(chromosomes))]

    dorminating_chromosomes = []
    non_dorminating_chromosomes = []

    for reference_position, reference_chromosome in enumerate(chromosomes):
        for other_position, other_chromosome in enumerate(chromosomes):
            x1 = reference_chromosome['hard_constraint']
            x2 = other_chromosome['hard_constraint']
            y1 = reference_chromosome['soft_constraint']
            y2 = other_chromosome['soft_constraint']
            print((x1, x2), (y1, y2))

            # (x1 <= x2 and y1 <= y2) and (x1 < x2 or y1 < y2)
            if ((x1 <= x2 and y1 <= y2) and (x1 < x2 or y1 < y2)):
                domination_count[reference_position] += 1
                print(domination_count[reference_chromosome])
                dominated_elements[reference_position].append(other_position)
            """
            if reference is dominant than other then
            domination_count[reference_position] += 1
            dominated_elements[reference_position].append(other_position)
            """

    return dorminating_chromosomes, non_dorminating_chromosomes

# Function to find index of list


def index_of(a, list):
    for i in range(0, len(list)):
        if list[i] == a:
            return i
    return -1


def sort_by_values(list1, values):
    sorted_list = []
    while(len(sorted_list) != len(list1)):
        if index_of(min(values), values) in list1:
            sorted_list.append(index_of(min(values), values))
        values[index_of(min(values), values)] = math.inf
    return sorted_list


def over_crowding(non_dorminating_chromosomes, dorminating_chromosomes):
    crowding_distance = [0 for i in range(0, len(dorminating_chromosomes))]
    fitness_value1 = [chromosome['hard_constraint'] for chromosome in non_dorminating_chromosomes]
    fitness_value2 = [chromosome['soft_constraint'] for chromosome in non_dorminating_chromosomes]
    fitness_value1_sorted = sort_by_values(dorminating_chromosomes, fitness_value1)
    fitness_value2_sorted = sort_by_values(dorminating_chromosomes, fitness_value2)
    crowding_distance[0] = 4444444444444444
    crowding_distance[len(dorminating_chromosomes) - 1] = 4444444444444444
    for i in range((1, len(dorminating_chromosomes)-1)):
        crowding_distance[i] = crowding_distance[i] + (fitness_value1[fitness_value1_sorted[i+1]] -
                                                       fitness_value2[fitness_value1_sorted[i-1]])/(max(fitness_value1)-min(fitness_value1))
    for i in range((1, len(dorminating_chromosomes)-1)):
        crowding_distance[i] = crowding_distance[i] + (fitness_value1[fitness_value2_sorted[i+1]] -
                                                       fitness_value2[fitness_value2_sorted[i-1]])/(max(fitness_value2)-min(fitness_value2))
    return crowding_distance


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

    non_dominated_chromosomes = non_dorminating_sort(population)
    return non_dominated_chromosomes


if __name__ == "__main__":
    pass
