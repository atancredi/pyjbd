class Error(Exception):
    def __init__(self):
        super().__init__("An error occured")


class DatabaseError(Exception):
    def __init__(self):
        super().__init__("Database does not exsists")


class KeyNotFound(Exception):
    def __init__(self):
        super().__init__("Key not found in database")

class PathNonExists(Exception):
    def __init__(self, path = None):
        if path != None:
            super().__init__("Path does not exists: "+path)
        else: super().__init__("Path does not exists.")