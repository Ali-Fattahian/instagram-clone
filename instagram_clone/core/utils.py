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

def datetime_generator(datetime_dict, date_created):
    """This function changes the format of datetime dictionary(from datetime_subtractor) given to it, to ...ago format"""
    days = datetime_dict.get('days')
    hours = datetime_dict.get('hours')
    minutes = datetime_dict.get('minutes')
    seconds = datetime_dict.get('seconds')

    if days > 0:
        if days == 7:
            return 'a week ago'
        elif days == 1:
            return 'yesterday'
        elif 1 < days < 7:
            return f'{days} days ago'
        elif days > 7:
            return date_created
    elif days == 0:  # 23 hours and less
        if hours > 0:
            if hours == 1:
                return 'an hour ago'
            elif 1 < hours < 24:
                return f'{hours} hours ago'
        elif hours == 0:  # 59 minutes and less
            if minutes > 0:
                if minutes == 1:
                    return 'a minute ago'
                elif 1 < minutes < 60:
                    return f'{minutes} minutes ago'
            elif minutes == 0:  # 59 seconds and less
                if seconds > 0:
                    if seconds == 1:
                        return 'a seconds ago'
                    elif 1 < seconds < 60:
                        return f'{seconds} seconds ago'
