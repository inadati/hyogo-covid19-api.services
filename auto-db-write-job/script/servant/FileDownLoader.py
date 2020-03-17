import urllib.request


class Summon:
    def __init__(self, url, title):
        self.url = url
        self.title = title

    def service(self):
        urllib.request.urlretrieve(self.url, "{0}".format(self.title))
