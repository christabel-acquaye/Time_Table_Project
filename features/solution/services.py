import random
import pprint
from features.migration import read_student
from features.exam.services import get_exam_bound
from features.exam.services import get_exam
from features.exam.services import get_exam_column

def rand_gen(start, finish):
    finish +=1
    rand_arr = list(range(start, finish))
    random.shuffle(rand_arr)
    return rand_arr

def get_exam_student_group_match(exam, student_group):
    related_course = []
    
    for course in student_group:
        # pprint.pprint(course['course'])
        if exam in course['course']:
            related_course.append(course['id'])
    
    # pprint.pprint(related_course)
    return related_course




def get_exam_search():
    exam_student_group = []
  
    data = read_student()
   
    exams = get_exam()
  
    start = 1
    finish = get_exam_bound()
    
    rand_arr = rand_gen(start=start, finish=finish)
    for id in rand_arr:
        exam_id = id
        # print(exam_id)
        exam = get_exam(id = exam_id)
        examCode = get_exam_column(columnName='examCode', id=exam_id)
        # print(examCode[0][0])
        group = get_exam_student_group_match(exam=examCode[0][0], student_group=data)
        exam_student_group.append(group)
    return exam_student_group



    

if __name__ == "__main__":
  
    data = get_exam_search()
    print(data)
    

  