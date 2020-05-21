from _shared import uuid

from .queries import use_query


def insert_period(id,  length, day, time, penalty):
    '''
    Insert Period deatils into Period Table
    '''
    params = {'id': id, 'length': length, 'day': day, 'time': time, 'penalty': penalty}
    return use_query(params=params, query_type='add-periods')


def get_periods(penalty=None, id=None):
    '''Get all Periods in db'''
    return use_query(params={'penalty': penalty, 'id': id}, query_type='get-periods')


def get_period_date(id=None):
    data = get_periods(id=id)
    return [period['day'] for period in data]


def get_period_penalty(id):
    data = get_period_penalty(id=id)
    return data[0]['penalty']


def get_periods_with_lengths():
    return list(((int(period['id']), period['length']) for period in get_periods()))


def get_period_bound():
    periods = get_periods()
    return len(periods)


if __name__ == '__main__':

    # length = 120
    # day = "1997-06-04"
    # time = "8:00am-11:30am"
    # penalty = 1
    # id = "3"
    # print(list(get_periods_with_lengths()))
    from main import app
    with app.app_context():
        print(get_periods(id=1))

    # insert_period(
    #               length=length,
    #               day=day,
    #               time=time,
    #               penalty=penalty,
    # id = id)
    # get_period(penalty = penalty)
    # update_period(columnName = 'length', update = 100, id=id)
    # delete_period(penalty=penalty)
    # get_period()
    # data = get_period()
    # print(data)

    # print(get_periods(penalty=None, id=1))
