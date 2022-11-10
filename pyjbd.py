import json
import os
import shutil

# NEXT use pydantic
# NEXT this should be a wrapper for ANY database with support for typing like EntityFramework more or less

#####################################################
##### Database Object ###############################
#####################################################
class Database():

    __version__ = "2"

    def __init__(self, name, subfolder = None, working_dir = None):
        

        self.conf = Configuration(name, subfolder, working_dir)
        print(self.conf.__dict__)

        # print(conf.__dict__)
        # self.conf = conf.__dict__

        #open database
        self.open_database(name)
        os.chdir(self.conf.path)

    def create_database(self):

        # TODO: controlla che esista la dir prima
        os.mkdir(self.conf.path)
        os.chdir(self.conf.path)
        with open(self.conf.ref, 'w') as db:
            json.dump({}, db)

    def open_database(self,name):
        if not os.path.exists(self.conf.path+self.conf.sep+'config.json'):
            # print("create new db")
            self.create_database()
            self.save_database()
        else:
            os.chdir(self.conf.path)
            with open('config.json', 'r') as i:
                self.conf.load(json.loads(i.read()))

    def reset_database(self):
        self.delete_database()
        self.create_database()
        self.save_database()

    def delete_database(self):
        self.conf.tables = []
        os.chdir('..')
        shutil.rmtree(self.conf.path)
    
    def save_database(self):
        #os.chdir(self.conf["path"])
        with open("config.json", 'w') as f:
            f.write(json.dumps(self.conf.__dict__))
    
    def close(self):
        self.save_database()
    
    def insert(self, object):
        if not self.validateType(object):
            self.registerType(object)
            
        tablename = object.__class__.__name__
        
        if tablename not in self.conf.tables:
            return False

        
        with open(self.conf.ref, "r") as jf:
            data = json.loads(jf.read())
        
        print("AHHHHHHHHHHHHH")
        print(data)

        if "hasIndex" in object.conf and object.conf["hasIndex"] == True:
            data[tablename][len(data[tablename])] = object.asObject()
        else:
            data[tablename].append(object.asObject())

        with open(self.conf.ref, "w") as jf:
            json.dump(data, jf)

    def get(self,object):
        tablename = object.__class__.__name__
        
        if tablename not in self.conf.tables:
            return False

        retdata = []
        totaldata = self.dump()

        for oo in totaldata[tablename]:
            for key in oo:
                object[str(key)] = oo[str(key)]
            retdata.append(object)
        
        return retdata

    def dump(self):
        with open(self.conf.ref, "r") as jf:
            return json.loads(jf.read())
    
    # SUPPORT FOR TYPES
    def registerType(self,object):
        if object.conf and object.conf["isTable"]:
            name = object.__class__.__name__
            self.conf.tables.append(name)
            self.save_database()
            if object.conf and "hasIndex" in object.conf and object.conf["hasIndex"] == True:
                print('STOINSERNENDO')
                raw_insert(self.conf.ref,name,{})
            else: raw_insert(self.conf.ref,name,[])
        else: raise Exception("not a table")

    def validateType(self, object):
        print(self.conf)
        return object.__class__.__name__ in self.conf.tables

#####################################################
##### Database Type Settings ########################
#####################################################
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

#####################################################
##### Exceptions ####################################
#####################################################
class Exceptions:

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

#####################################################
##### Configuration #################################
#####################################################
class Configuration:

    def __init__(self, name, subfolder = None, working_dir = None) -> None:
        self.name = name
        self.tables = []

        # User-defined path
        if working_dir == None:
            working_dir = os.getcwd()

        self.sep = "\\" if "\\" in working_dir else "/"

        if subfolder != None:
            fullpath = working_dir + self.sep + subfolder
            if not os.path.exists(fullpath):
                os.mkdir(fullpath)
            self.local_path = fullpath
        else: self.local_path = working_dir


        # Generate path for DB files
        self.path = self.local_path + self.sep + name
        self.ref = name  + ".json"
    
    def load(self, object):
        for key in object:
            setattr(self,key,object[key])


#####################################################
##### Utility Functions #############################
#####################################################
def exists(list, name):
    for db in list:
        if db['name'] == name:
            return db
    return False

def raw_insert(ref, key, value):
        with open(ref, "r") as jf:
            data = json.loads(jf.read())

        data[key] = value

        with open(ref, "w") as jf:
            json.dump(data, jf)

