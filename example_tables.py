from pyjbd.pyjbd import connector
from pyjbd.typeutils import Table, IndexedTable
db = connector()

class Prova(Table):
    def __init__(self):
        super().__init__()
        self.field = ""
class Prova2(IndexedTable):
    def __init__(self):
        super().__init__()
        self.field2 = ""

db.open_database("m")
db.set_db('m') 

p = Prova()
p.field = "prova"
p2 = Prova2()
p2.field2 = "aasdad"

db.insert_table(p)
db.insert_table(p2)
print(db.dump("m"))

#db.delete_database("m")
db.save_database() #SHOULD BE INCLUDED INTO CONN.CLOSE