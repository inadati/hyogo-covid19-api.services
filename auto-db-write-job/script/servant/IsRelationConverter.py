class Summon:
    def __init__(self, xls_is_relation):
        self.xls_is_relation = xls_is_relation

    def service(self):
        if self.xls_is_relation is None:
            return False
        else:
            return True
