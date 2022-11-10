from pyjbd import Database, Table, IndexedTable

class Prova(Table):
    def __init__(self):
        super().__init__()
        self.field = ""
        self.field2 = ""
class Prova2(IndexedTable):
    def __init__(self):
        super().__init__()
        self.field2 = ""

db = Database("n", subfolder="dbs")

#db.reset_database()

p = Prova() #not indexed data
p.field = "prova"
p.field2 = "aa"

p2 = Prova2() #indexed data
p2.field2 = "aasdad"

#NON INSERTA PIU

#print(db.conf)

# print(db.dump())
db.insert(p)
#db.insert(p)
# db.insert(p)
db.insert(p2)
# print(db.dump())
print(db.get(Prova()))
 

#db.delete_database()
db.close()