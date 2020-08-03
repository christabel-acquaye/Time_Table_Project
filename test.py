# my_list = [{'Chromosome': 0, 'Domination_Count':1 }, 
#     {'Chromosome': 1, 'Domination_Count':0 },
#     {'Chromosome': 2, 'Domination_Count':3 },
#     {'Chromosome': 3, 'Domination_Count':3 },
#     {'Chromosome': 4, 'Domination_Count':1 }]


# res = dict((key, tuple(val)) for key, val in temp.items()) 

# test_list1 = [5, 5, 4, 2, 2, 2, 2, 2, 2, 1]
# test_list2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  

  

# res = {key+1 : [test_list2[idx]  
#       for idx in range(len(test_list2)) if test_list1[idx]== i] 
#       for key, i in enumerate(set(test_list1))} 

# print(res)



# dict = {1: [7, 8, 9], 2: [2, 3, 4, 5, 6], 3: [0, 1]}
# ls = list(dict.values())
# print(ls)
# keep = 5
# res = []
# for sublist in ls:
#     for item in sublist:
#         if len(res) < keep:
#             if len(sublist) < keep:
#                 res.append(item)
#             else:
#                 new_ls = [4,2,3,5,6]
#                 l = new_ls[0:]
#                 for i in l:
#                     res.append(i)
            
# print(res)

# import math
# test_list1 = [9,8,3,2,1]
# test_list2 = [5,1,4,3,2]
# distance  = [0] * len(test_list2)
# den = test_list1[len(test_list1)-1] - test_list1[0]

# for i, item in enumerate(test_list2):
#     if i == 0 or i == (len(test_list2)-1):
#         distance[0] = math.inf
#         distance[len(test_list2)-1] = math.inf
#     else:
#         distance[i] = abs(0 + ((test_list1[(i+1)] - test_list1[(i-1)])/abs(den)))
# print(distance)
# import math

# a = [math.inf, 0, 1,6, math.inf]
# b = [5,1,4,3,2]
# chromosomes_rank = sorted(range(len(a)), reverse=True, key=lambda k: a[k])
# print(chromosomes_rank)

# data = [[2], [0, 2, 3, 4, 5], [], [], [3], [0, 2, 3]]
# dormination_count = [0 for i in range(len(data))]
# search = [0,1,2,3,4,5]
# for id in range(0,6):
#     for sublist in data:
#         if id in sublist:
#             dormination_count[id] += 1
            
# print(dormination_count)
# import math
# list1 = [4, 5, 6]
# list2 = [math.inf, 1.0, math.inf]
#     zipped_lists = zip(list2, list1)
#     sorted_zipped_lists = sorted(zipped_lists, reverse=True)
#     sorted_list1 = [element for _, element in sorted_zipped_lists]
# print(sorted_list1)

import random
import pprint


# for item in data:
#     chromosome_size = len(item['data'])
#     ran = random.randint(1,(chromosome_size-1))
#     # print(item['data'][ran])
#     print(ran)
#     print(item['data'][ran])
#     for gene in item['data']:
#         if item['data'].index(gene) == ran:
#             swap_data = {'period_id': 2, 'exam_id': '16', 'rooms': [{'name': 'OLD', 'no_of_stds': 60}], 'std_with_seats': 60}
#             temp = swap_data
#             swap_data = gene
#             print()
#             item['data'][(item['data'].index(gene))]= temp
#     print(item['data'][ran])
# print(' ')
# pprint.pprint(data[0]['data'])



    
    