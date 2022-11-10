import json
import os
import shutil
import sys


# Instead of using connector i should wrap it into database for opening a database class for every connection
# NEXT use pydantic
# NEXT this should be a wrapper for ANY database with support for typing like EntityFramework more or less

# GOAL: i have a table in any db, i have an object matching the properties of that table:
# ---> one function to insert, delete, update, select

class connector:

    db_list = []
    db_prefs = None

    def __init__(self,conf, path = None):

        try:
            self.conf = conf
            
            #separator specific for system - can be done better
            self.sep = "\\" if "\\" in conf["local_path"] else "/"

        except Exception as ex:
            print(ex)
            sys.exit()

    def delete_database(self, db_name):
        if os.getcwd() == self.conf['path']:
            os.chdir("..")
            shutil.rmtree(self.conf['path'])
        # db = utils.exists(self.db_list, db_name)
        # if db:
            
        # else:
        #     raise DatabaseError

    def set_db(self, db_name):
        os.chdir(self.conf['path'])
        return
        db = utils.exists(self.db_list, db_name)
        if db:
            self.db_prefs = db
            os.chdir(db['path'])
        else:
            raise DatabaseError

    def insert(self, key, value):
        with open(self.conf['ref'], "r") as jf:
            data = json.loads(jf.read())

        data[key] = value

        with open(self.conf['ref'], "w") as jf:
            json.dump(data, jf)

    
    def delete(self, key):
        with open(self.db_prefs['ref'], "r") as jf:
            data = json.loads(jf.read())

        if key in data:
            data.pop(key, None)
        else:
            raise Exceptions.KeyNotFound

        with open(self.db_prefs['ref'], "w") as jf:
            json.dump(data, jf)

    def update(self, key, new_value):
        with open(self.db_prefs['ref'], "r") as jf:
            data = json.loads(jf.read())

        if key in data:
            data[key] = new_value
        else:
            raise Exceptions.KeyNotFound

        with open(self.db_prefs['ref'], "w") as jf:
            json.dump(data, jf)

    def get(self, key):
        with open(self.db_prefs['ref'], "r") as jf:
            data = json.loads(jf.read())

            if key in data:
                return data[key]
            else:
                raise Exceptions.KeyNotFound

#####################################################
##### Database Object ###############################
#####################################################
class Database():

    __version__ = "1.1.4"

    def __init__(self, name, subfolder = None, cwd = None):
        
        # Define configuration
        conf = {
            "name": name,
            "local_path": "",
            "tables": []
        }

        sep = "\\" if "\\" in conf["local_path"] else "/"
        self.sep = sep

        # User-defined path
        if cwd == None:
            cwd = os.getcwd()
        
        if subfolder != None:
            # if os.path.exists(cwd + sep + subfolder):
            #     conf["local_path"] = cwd + sep + subfolder
            # else:
            #     raise PathNonExists(cwd + sep + subfolder)
            fullpath = cwd + sep + subfolder
            if not os.path.exists(fullpath):
                os.mkdir(fullpath)
            conf["local_path"] = fullpath
        else: conf["local_path"] = cwd

        # print(conf)

        # Generate path for DB files
        conf["path"] = conf["local_path"] + sep + name
        conf["ref"] = name  + ".json"

        conn = connector(conf)

        self.connector = conn
        self.conf = conf

        #open database
        self.open_database(name)
        conn.set_db(name)

    def create_database(self):

        # TODO: controlla che esista la dir prima
        os.mkdir(self.conf['path'])
        os.chdir(self.conf['path'])
        with open(self.conf['ref'], 'w') as db:
            json.dump({}, db)

    def open_database(self,name):
        if not os.path.exists(self.conf["path"]+self.sep+'config.json'):
            # print("create new db")
            self.create_database()
            self.save_database()
        else:
            os.chdir(self.conf["path"])
            with open('config.json', 'r') as i:
                self.conf = json.loads(i.read())

    def reset_database(self):
        self.delete_database()
        self.create_database()
        self.save_database()

    def delete_database(self):
        self.conf['tables'] = []
        os.chdir('..')
        shutil.rmtree(self.conf['path'])
    
    def save_database(self):
        #os.chdir(self.conf["path"])
        with open("config.json", 'w') as f:
            f.write(json.dumps(self.conf))
    
    def close(self):
        self.save_database()
    
    def insert(self, object):
        if not self.validateType(object):
            self.registerType(object)
            
        tablename = object.__class__.__name__
        
        if tablename not in self.conf["tables"]:
            return False

        
        with open(self.conf['ref'], "r") as jf:
            data = json.loads(jf.read())

        if "hasIndex" in object.conf and object.conf["hasIndex"] == True:
            data[tablename][len(data[tablename])] = object.asObject()
        else:
            data[tablename].append(object.asObject())

        with open(self.conf['ref'], "w") as jf:
            json.dump(data, jf)

    def get(self,object):
        tablename = object.__class__.__name__
        
        if tablename not in self.conf["tables"]:
            return False

        retdata = []
        totaldata = self.dump()

        for oo in totaldata[tablename]:
            for key in oo:
                object[str(key)] = oo[str(key)]
            retdata.append(object)
        
        return retdata

    def dump(self):
        with open(self.conf['ref'], "r") as jf:
            return json.loads(jf.read())
    
    # SUPPORT FOR TYPES
    def registerType(self,object):
        if object.conf and object.conf["isTable"]:
            name = object.__class__.__name__
            self.conf["tables"].append(name)
            self.save_database()
            if object.conf and "hasIndex" in object.conf and object.conf["hasIndex"] == True:
                self.connector.insert(name,{})
            else: self.connector.insert(name,[])
        else: raise Exception("not a table")

    def validateType(self, object):
        return object.__class__.__name__ in self.conf["tables"]

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
##### Utility Functions #############################
#####################################################
def exists(list, name):
    for db in list:
        if db['name'] == name:
            return db
    return False

