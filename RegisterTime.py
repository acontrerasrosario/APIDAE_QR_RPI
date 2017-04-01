import datetime

#this function return the current time
def currentTime():
    now = datetime.datetime.now()
    return (str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))

# return the name of the day
def currentDateName():
    return datetime.datetime.today().strftime("%A").upper()


def currentDate():
    now = datetime.datetime.now()
    return str(now.month) +'-'+str(now.day)+'-'+str(now.year)
