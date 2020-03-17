from datetime import datetime, timedelta


class Summon:
    def __init__(self, xls_date):
        self.xls_date = xls_date

    def service(self):
        date = datetime(1899, 12, 30) + timedelta(days=self.xls_date)
        return date.isoformat()
