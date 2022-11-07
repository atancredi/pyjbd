from pyjbd.pyjbd import Database
from pyjbd.typeutils import Table, IndexedTable

class Prova(Table):
    def __init__(self):
        super().__init__()
        self.field = ""
class Prova2(IndexedTable):
    def __init__(self):
        super().__init__()
        self.field2 = ""

db = Database("m")

p = Prova() #not indexed data
p.field = "prova"

p2 = Prova2() #indexed data
p2.field2 = "aasdad"

db.insert(p)
db.insert(p2)
print(db.dump())

db.delete_database()
#db.close()