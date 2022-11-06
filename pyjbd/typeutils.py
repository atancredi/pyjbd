class Table:

    def __init__(self):
        self.conf = {
            "isTable": True
        }
    
    # RETURN as Object
    def asObject(self):
        obj = dict(self.__dict__)
        del obj["conf"]
        return self.__dict__