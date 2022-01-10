def datetime_subtractor(new_datetime, old_datetime):
	sub = new_datetime - old_datetime
	total_seconds = sub.total_seconds()
	seconds_for_all_days = (sub.days * 24 * 3600)
	remainder = total_seconds - seconds_for_all_days #if we don't consider the days
	hours_left_complete = remainder / 3600
	hours_left = int(remainder//3600)  #														Hours				
	minutes_left_complete = (hours_left_complete - hours_left) * 60 #get the minutes
	minutes_left = int(minutes_left_complete) #decimal part of the number						Minutes
	seconds_left_complete = (minutes_left_complete -  minutes_left) * 60
	seconds_left = int(seconds_left_complete) #													Seconds

	answer = {}

	if sub.days > 0:
		answer['days'] = sub.days
	else:
		answer['days'] = 0

	if hours_left > 0:
		answer['hours'] = hours_left	
	else:
		answer['hours'] = 0

	if minutes_left > 0:
		answer['minutes'] = minutes_left	
	else:
		answer['minutes'] = 0

	if seconds_left > 0:
		answer['seconds'] = seconds_left	
	else:
		answer['seconds'] = 0

	return answer