import json
import os
import shutil
import sys

from pyjbd import dbutils as utils
from pyjbd.exceptions import *


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
        except Exception as ex:
            print(ex)
            sys.exit()

    def create_database(self, name):

        sep = "/"
        if "\\" in self.local_path:
            sep = "\\"
        db = {
            'name': name,
            'path': self.local_path + sep + name,
            'ref': name + '.json'
        }

        # TODO: controlla che esista la dir prima
        os.mkdir(db['path'])
        os.chdir(db['path'])
        with open(db['ref'], 'w') as db_name:
            tmp_db = {}
            json.dump(tmp_db, db_name)

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
            return False
            
        tablename = object.__class__.__name__
        
        if tablename not in self.tables:
            return False
        
        with open(self.db_prefs['ref'], "r") as jf:
            data = json.loads(jf.read())

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
            self.tables.append(name)
            self.insert(name,[])
        else: raise Exception("not a table")

    def validateType(self, object):
        return object.__class__.__name__ in self.tables