import random
import pprint
from features.penalty.hard_constraints_def import get_total_hard_constraints_value
from features.penalty.penalty_def import get_total_penalty_value
from features.penalty.cost_function import get_fitness_value

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
        

def chromosomes_cross_over(chromosome_interest1, chromosome_interest2, params):
    # pprint.pprint(chromosome_interest2)
    chromosome_size = len(chromosome_interest1['data']) 
    generated_rand_check = []
    print('chromosome size:', chromosome_size)
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
                print(search_id)
                swap_data = gene
                ind, fig = find_gene_index_in_chromosome(search_id, chromosome_interest2)
                # temp_period = swap_data['period_id']
                # swap_data['period_id'] = fig['period_id']
                # fig['period_id'] = temp_period
                chromosome_interest1['data'][id] = fig
                chromosome_interest2['data'][ind] = swap_data
        i += 1
            # pprint.pprint(chromosome_interest1)
    # chromosome_interest1 = get_fitness_value(chromosome_interest1['data'], params)
    # chromosome_interest2 = calculate_chromosome_penalties(chromosome_interest2['data'], params)
    return chromosome_interest1['data'], chromosome_interest2['data']

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
        "period_id": 4,
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
        "period_id": 10,
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
        "period_id": 20,
        "exam_id": "B",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 30,
        "exam_id": "C",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 40,
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
    
    a =  {
    "data": [
    {
        "period_id": 20,
        "exam_id": "20",
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
        "period_id": 20,
        "exam_id": "30",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 30,
        "exam_id": "40",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    },
    {
        "period_id": 40,
        "exam_id": "10",
        "rooms": [
        {
        "name": "OLD",
        "no_of_stds": 400
        },]
    }
    ],
    "soft_constraint": 40,
    "hard_constraint": 48
    },
            
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
           

    child1, child2 = chromosomes_cross_over(data[0], data[1], params)
    # print(child1 == child2)
    # print(child1 == data[0])
    # print(child1 == data[1])
    # pprint.pprint(data[0])
    pprint.pprint(child1)
    pprint.pprint(child2)
    # print(chromosomes_cross_over(data[0], data[1], params))