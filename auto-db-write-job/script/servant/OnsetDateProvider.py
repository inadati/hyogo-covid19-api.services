from datetime import datetime, timedelta


class Summon:
    def __init__(self, onset_date):
        self.onset_date = onset_date

    def service(self):
        if type(self.onset_date) is int:
            date = datetime(1899, 12, 30) + timedelta(days=self.onset_date)
            return "{0:%m月%d日}".format(date)
        else:
            return self.onset_date
