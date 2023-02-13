from pyjbd import Database, Table

class Prova(Table):
    def __init__(self):
        super().__init__()
        self.field = ""
        self.field2 = ""

db = Database("n", subfolder="dbs")

#db.reset_database()

p = Prova() #not indexed data
p.field = "prova"
p.field2 = "aa23"

#NON INSERTA PIU

#print(db.conf)

# print(db.dump())
db.insert(p)
#db.insert(p)
print(db.dump())
# print([i.asObject() for i in db.get(Prova())])
 

# db.delete_database()
db.close()