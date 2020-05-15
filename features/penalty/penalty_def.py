# def room_size_penalty(original, new):
#     percentage = round((new/original) * 100)

#     penalty = 0
#     if percentage in range(1,10):
#         penalty = 1
#     elif percentage in range(10,30):
#         penalty = 0
#     elif percentage in range(30,60):
#         penalty = -1
#     elif percentage in range(60,100):
#         penalty = -2
#     else:
#         print('Percentage out of range')
#     return penalty

# def large_exam_penalty(exam_threshold, exam_size):
#     percentage = round(((exam_size-exam_threshold)/exam_threshold) * 100)
#     print(percentage)
#     penalty = 0
#     if percentage in range(1,10):
#         penalty = 1
#     elif percentage in range(10,30):
#         penalty = 5
#     elif percentage in range(30,60):
#         penalty = 10
#     elif percentage in range(60,101):
#         penalty = 20
#     else:
#         penalty = 0
#     return penalty


def get_period_penalty(chromosome, period):
    return period_penalty


def get_room_penalty(chromosome, room):
    return room_penalty


def get_exam_penalty(chromosome, exam):
    return exam_penalty


def get_total_penalty_value():
    penalty = []
    penalty.append(get_exam_penalty)
    penalty.append(get_period_penalty)
    penalty.append(get_room_penalty)

    return sum(penalty)
