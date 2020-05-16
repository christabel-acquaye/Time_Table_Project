from _shared import in_query
from _shared.error_service import QUERY_NOT_FOUND


@in_query
def use_query(params: dict, query_type: str):
    query = ''

    if query_type == 'add-exam':
        query = '''
            INSERT INTO exams(id, length, alt, minSize, maxRooms, average, examCode )
            VALUES (
                %(id)s,%(length)s, %(alt)s ,%(minSize)s, %(maxRooms)s, %(average)s, %(examCode)s
            )
        '''
    elif query_type == 'get-exams':
        query = '''
            SELECT
                id, length, alt, minSize, maxRooms, average, examCode
            FROM exams
        '''

        if params.get('id'):
            query += ' WHERE id = %(id)s'

        if params.get('examCode'):
            query += ' WHERE examCode = %(examCode)s'
        if params.get('order_by'):
            order_by = params.get('order_by')
            query += f' ORDER BY {order_by} DESC'

    elif query_type == 'get-exams-count':
        query = '''
            SELECT COUNT(*) as count FROM exams
        '''
    else:
        raise QUERY_NOT_FOUND(query_type)

    return query
