from _shared import in_query
from _shared.error_service import QUERY_NOT_FOUND


@in_query
def use_query(params: dict, query_type: str):
    query = ''

    if query_type == 'add-periods':
        query = '''
            INSERT INTO periods(id, length, day, time, penalty)
            VALUES (
            %(id)s, %(length)s, %(day)s , %(time)s, %(penalty)s
            )
        '''
    elif query_type == 'get-periods':
        query = '''
           SELECT id, length, day, time, penalty FROM periods
        '''

        if params.get('penalty'):
            query += ' WHERE penalty = %(penalty)s'

        if params.get('penalty'):
            query_type += 'WHERE id = %(id)s'

    else:
        raise QUERY_NOT_FOUND(query_type)

    return query
