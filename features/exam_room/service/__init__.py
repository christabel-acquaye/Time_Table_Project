from .queries import use_query


def insert_exams_rooms(examId, roomId):
    '''
    Insert exam room assignments into Exam Room Table
    '''
    use_query(params={'examId': examId, 'roomId': roomId}, query_type='add-exam-rooms')


def get_exam_room(id=None):
    return use_query(params={'id': id}, query_type='get-exam-rooms')
