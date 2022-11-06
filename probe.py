import time
from datetime import timedelta
class TimeProbe:
    def __init__(self):
        self.jobs = {}

    def start(self, job):
        self.jobs[job] = {
            "name": job,
            "startTime": time.monotonic(),
            "stopTime": ""
        }

    def stop(self, job):
        self.jobs[job]["stopTime"] = time.monotonic()

    def print(self, job):
        elapsed = timedelta(seconds=self.jobs[job]["startTime"] - self.jobs[job]["stopTime"])
        print("Time for job '"+job+"': "+str(elapsed))
    
    def printAll(self):
        for job in self.jobs:
            self.print(job)

t = TimeProbe()


t.start("import")
from pyjbd.pyjbd import connector
from pyjbd import typeutils as tp
db = connector()
t.stop("import")

class Prova():
    def __init__(self):
        super().__init__()
        self.field = ""

t.start("createdb")
db.create_database("m")
db.set_db('m')
t.stop("createdb")

t.start("add")
db.add("nome", "giuseppe")
db.add("cognome", "criscione")
db.add('list', [])
t.stop("add")

t.start("dump")
print(db.dump('m'))
t.stop("dump")

t.start("update")
db.update('list', [1, 2])
t.stop("update")

print(db.dump('m'))

t.start("get")
print(db.get("cognome"))
t.stop("get")

t.start("delete")
db.delete("cognome")
t.stop("delete")

print(db.dump("m"))

t.start("deletedb")
db.delete_database("m")
t.stop("deletedb")

t.printAll()

p = Prova()
p.field = "prova"
db.registerType(p)
db.validateType(p)
print(p.__dict__)