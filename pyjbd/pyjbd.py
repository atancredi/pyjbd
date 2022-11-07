import json
import os
import shutil
import sys

from pyjbd import dbutils as utils
from pyjbd.exceptions import *

# Instead of using connector i should wrap it into database for opening a database class for every connection
# NEXT use pydantic
# NEXT this should be a wrapper for ANY database with support for typing like EntityFramework more or less

# GOAL: i have a table in any db, i have an object matching the properties of that table:
# ---> one function to insert, delete, update, select

class connector:

    db_list = []
    db_prefs = None

    def __init__(self, path = None):
        try:
            if path != None:
                if os.path.exists(path):
                    self.local_path = path
                else:
                    raise PathNonExists(path)
            self.local_path = os.getcwd()
            self.tables = []
            self.db = {}
            
            #separator specific for system - can be done better
            self.sep = "/"
            if "\\" in self.local_path:
                self.sep = "\\"

        except Exception as ex:
            print(ex)
            sys.exit()

    def create_database(self, name):

        db = {
            'name': name,
            'path': self.local_path + self.sep + name,
            'ref': name + '.json'
        }

        self.db = db

        # TODO: controlla che esista la dir prima
        os.mkdir(db['path'])
        os.chdir(db['path'])
        with open(db['ref'], 'w') as db_name:
            tmp_db = {}
            json.dump(tmp_db, db_name)

        self.db_list.append(db)
        self.save_database()

    def save_database(self):
        os.chdir(self.db["path"])
        info = dict(self.db)
        info["tables"] = self.tables
        with open("config.json", 'w') as f:
            f.write(json.dumps(info))

    def open_database(self,name):
        path = self.local_path + self.sep + name
        if not os.path.exists(path):
            self.create_database(name)
        else:
            with open(path + self.sep + 'config.json', 'r') as i:
                db = json.loads(i.read())
                self.db = db
                self.tables = db["tables"]
                self.db_list.append(db)

    def delete_database(self, db_name):
        db = utils.exists(self.db_list, db_name)
        if db:
            if os.getcwd() == db['path']:
                os.chdir("..")
            shutil.rmtree(db['path'])
        else:
            raise DatabaseError

    def set_db(self, db_name):
        db = utils.exists(self.db_list, db_name)
        if db:
            self.db_prefs = db
            os.chdir(db['path'])
        else:
            raise DatabaseError

    def dump(self, db_name):
        db = utils.exists(self.db_list, db_name)
        if db:
            with open(db['ref']) as _db:
                data = json.loads(_db.read())
                return data
        else:
            raise DatabaseError

    def insert(self, key, value):
        with open(self.db_prefs['ref'], "r") as jf:
            data = json.loads(jf.read())

        data[key] = value

        with open(self.db_prefs['ref'], "w") as jf:
            json.dump(data, jf)

    def insert_table(self, object):
        if not self.validateType(object):
            self.registerType(object)
            
        tablename = object.__class__.__name__
        
        if tablename not in self.tables:
            return False
        
        with open(self.db_prefs['ref'], "r") as jf:
            data = json.loads(jf.read())

        if "hasIndex" in object.conf and object.conf["hasIndex"] == True:
            #oo = dict(object.asObject())
            #oo["_id"] = len(data)-1
            data[tablename][len(data[tablename])] = object.asObject()
        else:
            data[tablename].append(object.asObject())

        with open(self.db_prefs['ref'], "w") as jf:
            json.dump(data, jf)

    def delete(self, key):
        with open(self.db_prefs['ref'], "r") as jf:
            data = json.loads(jf.read())

        if key in data:
            data.pop(key, None)
        else:
            raise KeyNotFound

        with open(self.db_prefs['ref'], "w") as jf:
            json.dump(data, jf)

    def update(self, key, new_value):
        with open(self.db_prefs['ref'], "r") as jf:
            data = json.loads(jf.read())

        if key in data:
            data[key] = new_value
        else:
            raise KeyNotFound

        with open(self.db_prefs['ref'], "w") as jf:
            json.dump(data, jf)

    def get(self, key):
        with open(self.db_prefs['ref'], "r") as jf:
            data = json.loads(jf.read())

            if key in data:
                return data[key]
            else:
                raise KeyNotFound

    # SUPPORT FOR TYPES
    def registerType(self,object):
        if object.conf and object.conf["isTable"]:
        #if "isTable" in object.__dict__.keys() :
            name = object.__class__.__name__
            if name not in self.tables:
                self.tables.append(name)
                if object.conf and "hasIndex" in object.conf and object.conf["hasIndex"] == True:
                    self.insert(name,{})
                else: self.insert(name,[])
        else: raise Exception("not a table")

    def validateType(self, object):
        return object.__class__.__name__ in self.tables

class DBActions:

    def __init__(self,name):
        self.db = connector()
        self.name = name

    def create(self):
        self.db.create_database(self.name)

    def delete(self):
        self.db.delete_database(self.name)

    def open(self):
        pass

    def save(self):
        pass

class Database():

    def __init__(self, name, path = None):
        pass

        if path == None:
            path = os.getcwd()

        #try to open database

        #if not exists create