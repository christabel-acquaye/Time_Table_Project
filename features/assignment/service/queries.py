from _shared import in_query
from _shared.error_service import QUERY_NOT_FOUND
from typing import Literal


@in_query
def use_query(params: dict, query_type: str):
    query = ''

    if query_type == 'add-assignment':
        query = '''
            INSERT INTO assignment(periodId, roomId, examId)
            VALUES (%(periodId)s, %(roomId)s, %(examId)s)

        '''
    elif query_type = 'get-assigment':
        query = '''
            SELECT id, periodId, roomId, examId FROM assignment
        '''
        if 'id' in params:
            query += ' WHERE id=%(id)s'
    else:
        raise QUERY_NOT_FOUND(query_type)

    return query
