import copy
import crypt
import datetime
from collections import UserDict

from bson import ObjectId
from Extensions import flask_pymongo

__author__ = 'lonnstyle'



class User(UserDict):
    """
    Represent user, implementing proper methods
    """

    _data = {
    }

    def __init__(self,_id=None, _data=None, username=None, email=None, password=None):
        super().__init__(copy.deepcopy(self._data))
        print(self._data)
        if _data is not None:
            self.update(_data)
    
        find_by = {}
        print(self._data)
        if _id is not None:
            self._data['_id'] = _id if isinstance(_id, ObjectId) else ObjectId(_id)
    
        if email is not None:
            self._data['email'] = email.lower()
        if username is not None:
            self._data['username'] = username
        if len(find_by) > 0:
            user = flask_pymongo.db.users.find_one(find_by)
            if user is not None:
                self.update(user)
        

        if password is not None:
            self._data['password'] = self.generate_password(password)

        
    def update(self, data):
        for key, value in data.items():
            self._data[key] = value


    @classmethod
    def create_from(cls, data):
        if 'password' in data:
            data['password_hash'] = cls.generate_password(data['password'])
            del data['password']
        # data['created_at'] = datetime.datetime.utcnow()
        user = cls(_data=data)
        return user

    @property
    def id(self):
        return self._data.get('_id', None)

    @staticmethod
    def generate_password(password):
        return str.encode(crypt.crypt(password, salt=crypt.METHOD_SHA512))

    def check_password(self, input_password):
        password_hash = self._data.get('password_hash', None)
        if password_hash is None:
            return False
        password_hash = password_hash.decode()
        return crypt.crypt(input_password, password_hash) == password_hash

    def insert(self):
        if '_id' in self._data:
            del self._data['_id']
        self._data['_id'] = flask_pymongo.db.users.insert_one(self._data).inserted_id

    @classmethod
    def find_one(cls, query):
        user = flask_pymongo.db.users.find_one(query)
        if user is None:
            return None
        return cls(_data=user)

    def save(self):
        if "_id" in self._data and self._data["_id"] is not None:
            flask_pymongo.db.users.update_one({
                '_id': self.id}, {'$set': self._data},
                upsert=True)
            print("update")  
        else:
            flask_pymongo.db.users.insert_one(self._data)
            print("insert")
        


    def __str__(self):
        return "<%s (id:%s, username:%s)>" % (self.__class__.__name__,
                                                    self.id,
                                                    self.get('steam_profile', None))
