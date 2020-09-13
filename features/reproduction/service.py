import random
import pprint
import datetime
from features.penalty.hard_constraints_def import get_total_hard_constraints_value, __get_difference,has_duplicates
from features.exam.service.__init__ import (get_exam_id_from_name,
                                            get_exam_max_room, 
                                            get_exam_enrollment 
                                            )
from features.penalty.penalty_def import get_total_penalty_value
from features.penalty.cost_function import get_fitness_value
from features.periods.service import get_period_date

from features.rooms.service import get_rooms

def find_gene_index_in_chromosome(exam_id, chromosome_interest):
        for ind,  elem in enumerate(chromosome_interest['data']):
            if elem['exam_id'] == exam_id:
                return ind, elem



# def calculate_chromosome_penalties(chromosome_interest, params):
    
#     chromosome_interest['soft_constraint'] = get_total_penalty_value(chromosome_interest, params['threshold'],
#                                                        params['reserved_periods'])
#     chromosome_interest['hard_constraint'] = get_total_hard_constraints_value(chromosome_interest,
#                                                                 params['closed_periods'], params['reserved_rooms'],
#                                                                 params['previous_chromosome'])  

#     return chromosome_interest
        

def chromosomes_cross_over(chromosome_interest1, chromosome_interest2):
    # pprint.pprint(chromosome_interest2)
    chromosome_size = len(chromosome_interest1['data']) 
    generated_rand_check = []
    # print('chromosome size:', chromosome_size)
    ran1 = 0
    i = 0
    for i in range(len(chromosome_interest1['data'])):
        ran1 = random.randint(0, (chromosome_size - 1))
        generated_rand_check.append(ran1)
        # print(ran1,'rand1')
        for id in range(len(chromosome_interest1['data'])):
            if id == ran1:
                gene = chromosome_interest1['data'][id]
                search_id = gene['exam_id']
                # print(search_id)
                swap_data = gene
                ind, fig = find_gene_index_in_chromosome(search_id, chromosome_interest2)
                # temp_period = swap_data['period_id']
                # swap_data['period_id'] = fig['period_id']
                # fig['period_id'] = temp_period
                chromosome_interest1['data'][id] = fig
                chromosome_interest2['data'][ind] = swap_data
        i += 1

    # if chromosome_interest1['data'] is None:
    #         print("Child1 doesnt have flesh")
    # if chromosome_interest2['data'] is None:
    #         print("Child2 doesnt have flesh")
            # pprint.pprint(chromosome_interest1)
    # chromosome_interest1 = get_fitness_value(chromosome_interest1['data'], params)
    # chromosome_interest2 = calculate_chromosome_penalties(chromosome_interest2['data'], params)
    return chromosome_interest1['data'], chromosome_interest2['data']


def get_all_children(parents):
    children = []
    for ind, parent in enumerate(parents):
        for other_ind, other_parent in enumerate(parents[(ind):]):
            child1, child2 = chromosomes_cross_over(parent, other_parent)
            if order_chromosome_by_period(child1) == order_chromosome_by_period(child2): 
                # children.append(child1)
                continue

            if order_chromosome_by_period(child1) not in order_all(children):
                children.append(child1)
            if order_chromosome_by_period(child2) not in order_all(children):
                children.append(child2)
            # if (order_chromosome_by_period(child1) == order_chromosome_by_period(parent['data'])) or (order_chromosome_by_period(child1) == order_chromosome_by_period(other_parent['data'])): continue
            # pprint.pprint(child1)
            # pprint.pprint(child2)
            
    return children

def get_occupied_rooms_for_periods(period_id, chromosome):
    occupied_rooms = []
    for gene in chromosome:
        if gene['period_id'] == period_id:
            occupied_rooms.append(gene['rooms'])

    occupied_rooms = [item for sublist in occupied_rooms for item in sublist]
    return occupied_rooms

def order_chromosome_by_period(chromosome):
    newlist = sorted(chromosome, key=lambda k: k['period_id']) 
    return newlist

def order_all(chromosomes):
    
    new_chromosomes = []
    for ind, chromosome in enumerate(chromosomes):
      
        arranged_chromosome = order_chromosome_by_period(chromosome)
        new_chromosomes.append(arranged_chromosome)

    return new_chromosomes

def check_uniqueness(generation):
    unique_gen = []
    for item in generation:
        for other_item in generation:
            if item == other_item: continue
            if generation[item] == generation[other_item]:
                continue
            else: 
                unique_gen.append(generation[item])
    return  unique_gen


def my_custom_random(all_period_max, exclude):
    print(exclude)
    randInt = random.randint(1,all_period_max)
    return my_custom_random(all_period_max, exclude) if randInt in exclude else randInt 


def refined_get_rooms():
    all_rooms = []
    for room in get_rooms():
        room = {
            'name': room['roomName'],
            'size': room['size']
        }
        all_rooms.append(room)
    return all_rooms


def get_avaliable_rooms_for_period(period_id, chromosome):
    all_rooms = refined_get_rooms()
    occupied_rooms = get_occupied_rooms_for_periods(period_id, chromosome)

    available_rooms = [x for x in a if x not in [2, 3, 7]]
    return available_rooms


if __name__ == "__main__":

    data = [
    {
    "data": [
    {
        "period_id": 2,
        "exam_id": "B",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },
        {
        "name": "EHC_102",
        "no_of_stds": 200
        },
        {
        "name": "NB_T3",
        "no_of_stds": 200
        },
        {
        "name": "NB_T5",
        "no_of_stds": 50
        }
        ],
        "std_with_seats": 850
    },
    {
        "period_id": 2,
        "exam_id": "D",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 1,
        "exam_id": "A",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 3,
        "exam_id": "C",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    }
    ],
    "soft_constraint": 50,
    "hard_constraint": 58
    },

   {
    "data": [
    {
        "period_id": 100,
        "exam_id": "A",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },
        {
        "name": "EHC_102",
        "no_of_stds": 200
        },
        {
        "name": "NB_T3",
        "no_of_stds": 200
        },
        {
        "name": "NB_T5",
        "no_of_stds": 50
        }
        ],
        "std_with_seats": 850
    },
    {
        "period_id": 200,
        "exam_id": "B",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 300,
        "exam_id": "C",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 400,
        "exam_id": "D",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    }
    ],
    "soft_constraint": 20,
    "hard_constraint": 10
    },

   {
    "data": [
    {
        "period_id": 1000,
        "exam_id": "A",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },
        {
        "name": "EHC_102",
        "no_of_stds": 200
        },
        {
        "name": "NB_T3",
        "no_of_stds": 200
        },
        {
        "name": "NB_T5",
        "no_of_stds": 50
        }
        ],
        "std_with_seats": 850
    },
    {
        "period_id": 2000,
        "exam_id": "B",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 3000,
        "exam_id": "C",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 4000,
        "exam_id": "D",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    }
    ],
    "soft_constraint": 20,
    "hard_constraint": 10
    },

 {
    "data": [
    {
        "period_id": 10000,
        "exam_id": "A",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },
        {
        "name": "EHC_102",
        "no_of_stds": 200
        },
        {
        "name": "NB_T3",
        "no_of_stds": 200
        },
        {
        "name": "NB_T5",
        "no_of_stds": 50
        }
        ],
        "std_with_seats": 850
    },
    {
        "period_id": 20000,
        "exam_id": "B",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 30000,
        "exam_id": "C",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 40000,
        "exam_id": "D",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    }
    ],
    "soft_constraint": 20,
    "hard_constraint": 10
    },


   

    ]
   
            
    # nls = []
    # nls.append(data[0])   
    # print(len(nls)) 
    # nls.append(a)
    # print(len(nls))
    params = {
            'threshold': 1000,
            'closed_periods': [],
            'reserved_rooms': [],
            'reserved_periods': [],
            'previous_chromosome': [],
            'prefered_rooms': [],  # get prefered rooms,r
            'prefered_periods':  []
        }
           
    children = []
    # print(type(data))
    # res = order_all(data)
    # for item in res:
    #     pprint.pprint(item)

    # print(len(data))
    # res = get_all_children(data)
    # print(len(res))
    # for item in res:
    #     pprint.pprint(item)
    print(get_occupied_rooms_for_periods(2, data[0]['data']))
    # roms = get_rooms()
    # print(roms)
    
