import datetime


def start_of_time_period(time_period):
    """
    Returns start date of the time period
    e.g. today is 19.11.11, time_period == week, return 12.11.11
    """
    if time_period == 'day':
        start_date = datetime.datetime.now() - datetime.timedelta(days=1)

    elif time_period == 'week':
        start_date = datetime.datetime.now() - datetime.timedelta(weeks=1)

    elif time_period == 'month':
        today = datetime.datetime.today()
        if today.month == 1:
            start_date = today.replace(year=today.year - 1, month=12)
        else:
            extra_days = 0
            while True:
                try:
                    start_date = today.replace(month=today.month - 1, day=today.day - extra_days)
                    break
                except ValueError:
                    extra_days += 1

    elif time_period == 'year':
        today = datetime.datetime.today()
        start_date = today.replace(year=today.year - 1)

    else:
        start_date = datetime.datetime.now() - datetime.timedelta(days=1)

    return start_date.strftime("%Y-%m-%d")


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
