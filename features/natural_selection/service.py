import math
import pprint
import operator


def get_chromosome_fitness(chromosomes, chromosome_id):
    return chromosomes[chromosome_id]['hard_constraint'],chromosomes[chromosome_id]['soft_constraint']


def get_distance_average(ls1, ls2):
    c = list(map(operator.add, ls1,ls2))
    c = [x/2 for x in c]
    return c
    
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

           
            if ((x1 <= x2 and y1 <= y2) and (x1 < x2 or y1 < y2)):
    
                # domination_count[other_position] += 1
                dominated_elements[reference_position].append(other_position)
        
    for id in range(0,(len(chromosomes))+1):
        for sublist in dominated_elements:
            if id in sublist:
                domination_count[id] += 1
      
    chromosomes_rank = sorted(range(len(domination_count)), reverse=False, key=lambda k: domination_count[k])
   
    domination_count = sorted(domination_count, reverse=False)
   
    print(domination_count)
    print(chromosomes_rank)
    res = {key+1 : [chromosomes_rank[idx]  
        for idx in range(len(chromosomes_rank)) if domination_count[idx]== i] 
        for key, i in enumerate(set(domination_count))} 

    
    # for i in range(len(domination_count)):
    #     if domination_count[i] >= 0:
    #         non_dorminating_chromosomes.append(chromosomes_rank[i])
    #     else:
    #         dorminating_chromosomes.append(chromosomes_rank[i])

    # return dorminating_chromosomes, non_dorminating_chromosomes
    return res
def calc_crowding_distance(front_ls, fitness):
    """

    Arguments:
        
    Returns:
       
    """
    
   
    distance  = [0] * len(front_ls)
    den = fitness[len(fitness)-1] - fitness[0]

    for i, item in enumerate(front_ls):
        if i == 0 or i == (len(front_ls)-1):
            distance[0] = math.inf
            distance[len(front_ls)-1] = math.inf
        else:
            distance[i] = abs(0 + ((fitness[(i+1)] - fitness[(i-1)])/abs(den)))
    return distance
    
def get_crowding_dis_ordered_ls(chromosomes, front_ls):
    """

    Arguments:
        
    Returns:
       
    """
    hard = []
    soft = []
    # if len(front_ls) == 2:
    #     return front_ls
    for id, item in enumerate(front_ls):
        fitness1, fitness2 = get_chromosome_fitness(chromosomes, item)
        
        hard.append(fitness1)
        soft.append(fitness2)

    crowding_distance_on_hard = calc_crowding_distance(front_ls, hard)
    crowding_distance_on_soft = calc_crowding_distance(front_ls, soft)
    
    averge_distance = get_distance_average(crowding_distance_on_hard, crowding_distance_on_soft)
    zipped_lists = zip(averge_distance, front_ls)
    sorted_zipped_lists = sorted(zipped_lists, reverse=True)
    sorted_list1 = [element for _, element in sorted_zipped_lists]
    
    return sorted_list1

def complete_nsga(keep,chromosomes):
    """

    Arguments:
        
    Returns:
       
    """

    result = non_dorminating_sort(chromosomes)
    ls = list(result.values())
    print("ls", ls)
    res = []

    for sublist in ls:
     

        if len(sublist) <= keep:
            for item in sublist:
                res.append(item)
            keep = keep - len(sublist)

        else:
          
            new_ls = get_crowding_dis_ordered_ls(chromosomes,sublist)
            
            l = new_ls[0:keep]
            
            for i in l:
                res.append(i)
            break
        
          
            
    return res
    
            

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
    chromosomes = [
        {
            "hard_constraint": 65,
            "soft_constraint": 51
        },
        {
            "hard_constraint": 56,
            "soft_constraint": 52
        },     
       
        {
            "hard_constraint": 62,
            "soft_constraint": 49
        },  
        {
            "hard_constraint": 57,
            "soft_constraint": 52
        },  
        {
            "hard_constraint": 59,
            "soft_constraint": 47
        },  
      
        {
            "hard_constraint": 56,
            "soft_constraint": 61
        },  

        {
            "hard_constraint": 56,
            "soft_constraint": 49
        },  

        {
            "hard_constraint": 58,
            "soft_constraint": 54
        },  

        {
            "hard_constraint": 60,
            "soft_constraint": 46
        },  

        {
            "hard_constraint": 59,
            "soft_constraint": 51
        },  

    ]
    keep =  5
    print(non_dorminating_sort(chromosomes))
    # print(complete_nsga(keep,chromosomes))
