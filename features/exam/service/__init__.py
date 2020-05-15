from .queries import use_query


def insert_exam(length, id, alt, minSize, maxRooms, average, examCode):
    '''
    Insert Exam details into Exam Table
    '''
    params = {
        'length': length,
        'alt': alt,
        'id': id,
        'minSize': minSize,
        'maxRooms': maxRooms,
        'examCode':  examCode,
        'average':  average
    }

    use_query(params=params, query_type='add-exam')


def get_exams(id=None, order_by=None, examCode=None):
    return use_query(params={'id': id, 'order_by': order_by, 'examCode': examCode}, query_type='get-exams')


def get_exam_column(cur, columnName, id=None):
    '''
    Get Specific  Exam deatils for a particular exams column
    '''
    exams = get_exams(id=id)
    return (exam[columnName] for exam in exams)


def get_exam_order_by_size():
    '''
    Function that gets all exams arranged by decreasing order of enrollment size
    '''
    return get_exams(order_by='minSize')


def get_exam_id_from_name(examName):
    data = get_exams(examCode=examName)
    return data[0]['id']


def get_exam_bound(cur):
    # Get total number of exams in db
    data = use_query(query_type='get-exams-count')
    return int(data[0][0])


if __name__ == '__main__':
    from main import app
    with app.app_context():
        id = "42"
        length = 125
        alt = True
        minSize = 21
        maxRooms = 2
        average = 10
        examCode = "IRAI ALL"
        columnName = 'length'
        update = 120

        # insert_exam(id = id,length= length, alt = alt,
        # minSize = minSize,maxRooms =  maxRooms, average = average, examCode = examCode)
        # update_exam(columnName = columnName, update = update, id=examCode)
        # get_exam()

        # get_exam(id = id)

        # delete_exam(id=examCode)

        # get_exam_column(columnName='id', id=None)

        data = get_exam_id_from_name(examName='CAT 154')
        print(data)