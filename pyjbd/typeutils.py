class Table:

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __init__(self):
        self.conf = {
            "isTable": True
        }
    
    # RETURN as Object
    def asObject(self):
        obj = dict(self.__dict__)
        del obj["conf"]
        return obj

class IndexedTable(Table):

    def __init__(self):
        super().__init__()
        self.conf["hasIndex"] = True