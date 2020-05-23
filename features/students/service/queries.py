from _shared import in_query
from _shared.error_service import QUERY_NOT_FOUND


@in_query
def use_query(params: dict, query_type: str):
    query = ''

    if query_type == 'add-students':
        query = '''
            INSERT INTO student(id, examId, periodId)
            VALUES (
                %(id)s,%(examId)s, %(periodId)s
            )
        '''
    elif query_type == 'get-students':
        query = '''
           SELECT id, examId, periodId FROM student
        '''

        if params.get('id'):
            query += ' WHERE id = %(id)s'

    elif query_type == 'get-all-students-id':
        query = '''
           SELECT id FROM student
        '''

    else:
        raise QUERY_NOT_FOUND(query_type)

    return query
