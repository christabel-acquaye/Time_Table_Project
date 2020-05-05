import datetime

start_date = datetime.datetime.now()
number_of_days = 11
end_date = start_date + datetime.timedelta(days=number_of_days)
print(start_date)
print(end_date)
day_diff = end_date.weekday() - start_date.weekday()

days = ((end_date-start_date).days - day_diff) / 7 * 5 + min(day_diff,5) - (max(end_date.weekday() - 4, 0) % 5)
print(days)

end_date = start_date + datetime.timedelta(days=(number_of_days + (number_of_days - days)))
print(end_date)
