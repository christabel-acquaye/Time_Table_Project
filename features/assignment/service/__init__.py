from _shared import with_key, AuthProvider, uuid, hash_value
from .queries import use_query, MODE
from ..schema import REGISTER_USER_DATA


def insert_assignment(periodId, roomId, examId):
    params = {'periodId': periodId, 'roomId': roomId, 'examId': examId}
    use_query(params=params, query_type='add-assignment')
    return params


def get_assignment(id):
    return use_query(params={'id': id}, query_type='get-assigment')
