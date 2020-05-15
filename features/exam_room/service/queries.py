from _shared import in_query
from _shared.error_service import QUERY_NOT_FOUND


@in_query
def use_query(params: dict, query_type: str):
    query = ''

    if query_type == 'add-exam-rooms':
        query = '''
            INSERT INTO examRoomRelation(examId, roomId)
            VALUES (
                %(examId)s, %(roomId)s
            )
        '''
    elif query_type == 'get-exam-rooms':
        query = '''
            SELECT * FROM examRoomRelation
        '''

        if params.get('id'):
            query += ' WHERE id = %(id)s'

    else:
        raise QUERY_NOT_FOUND(query_type)

    return query
