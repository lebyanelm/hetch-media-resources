# dependencies
import datetime
import months

class TimeCreatedModel():
    def __init__(self, timestamp=None):
        date = datetime.datetime.now()
        if timestamp:
            date = datetime.datetime.fromtimestamp(timestamp)
        month = months.Month(month=date.month, year=date.year)
        
        self.day = date.strftime('%d')
        self.month = month.month_abbr
        self.year = date.strftime('%Y')
        self.formatted_date = f'{self.day} {self.month}, {self.year}'
        self.time = date.strftime('%H:%M:%S')

        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = date.timestamp()