
def get_closed_period():
    closed_periods = []
    while True:
        period = input('Period(id): ')
        exam = input('Exam: ')

        # exam_id = get_exam_id_from_name(exam)
        closed_dic = {
            'Period_id': period,
            'Exam_id': exam
        }
        closed_periods.append(closed_dic)
    return closed_periods


if __name__ == "__main__":
    print(get_closed_period())
