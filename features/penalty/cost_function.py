def get_fitness_value(hard_constraints, penalties):
    fitness_value1 = sum(hard_constraints)
    fitness_value2 = sum(penalties)
    print(fitness_value1, fitness_value2)


if __name__ == "__main__":
    hard_constraints = [2,4,5,6]
    penalties = [1,1,1,1,1]
    get_fitness_value(hard_constraints, penalties)