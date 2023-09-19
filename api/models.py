from api.db import DB
import random


class NluObjectWithEntity(object):
    # Object class with Entity

    def __init__(self, collection, intent, entity, response):
        self.collection = collection
        self.intent = intent
        self.entity = entity
        self.response = response

    def json(self):
        return {
            'collection': self.collection,
            'intent': self.intent,
            'entity': self.entity,
            'response': self.response
        }

    @property
    def find(self):
        db = DB()
        db.init()

        if db.find_one(self.collection, {"intent": self.intent,
                                         "entity": self.entity}):
            return True
        else:
            return False

    @property
    def find_response(self):
        db = DB()
        db.init()

        if self.find:
            get = db.find_one(self.collection, {"intent": self.intent,
                                                "entity": self.entity})
            return get['response']
        else:
            return {"message": "Object not found."}


class NluObjectSimple(object):
    # Object class without Entity

    def __init__(self, collection, intent, response):
        self.collection = collection
        self.intent = intent
        self.response = response

    def json(self):
        return {
            'collection': self.collection,
            'intent': self.intent,
            'response': self.response
        }

    @property
    def find(self):
        db = DB()
        db.init()

        if db.find_one(self.collection, {"intent": self.intent}):
            return True
        else:
            return False

    @property
    def find_response(self):
        db = DB()
        db.init()

        if self.intent == "admissibilite_congé":
            if self.find:
                get = db.find_one(self.collection, {"intent": self.intent})
                return random.choice(get['response'])
            else:
                return {"message": "Object not found."}
        else:
            if self.find:
                get = db.find_one(self.collection, {"intent": self.intent})
                return get['response']
            else:
                return {"message": "Object not found."}

