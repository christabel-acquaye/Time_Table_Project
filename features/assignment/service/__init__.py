from _shared import AuthProvider, hash_value, uuid, with_key

from ..schema import REGISTER_USER_DATA
from .queries import MODE, use_query


def insert_assignment(periodId, roomId, examId):
    params = {'periodId': periodId, 'roomId': roomId, 'examId': examId}
    use_query(params=params, query_type='add-assignment')
    return params


def get_assignment(id):
    return use_query(params={'id': id}, query_type='get-assigment')
