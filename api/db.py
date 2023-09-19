import pymongo


def uri_db(user, pwd, domaine, port, db, auth_meca):
    port = str(port)

    return "mongodb://{}:{}@{}:{}/?authSource={}&authMechanism={}".format(user, pwd, domaine, port, db, auth_meca)


class DB(object):
    # Database model

    Domain = '127.0.0.1'
    Port = 27017
    Username = 'admin'
    Password = 'admin'
    Database = 'pandachatbot'
    Collection = None
    authMechanism = 'SCRAM-SHA-256'

    def __init__(self):
        self.Domain = DB.Domain
        self.Port = DB.Port
        self.Username = DB.Username
        self.Password = DB.Password
        self.Database = DB.Collection
        self.authMechanism = 'SCRAM-SHA-256'

    # Connexion establishing method
    @staticmethod
    def init():
        uri = str(uri_db(user=DB.Username, pwd=DB.Password, domaine=DB.Domain, port=DB.Port, db=DB.Database,
                         auth_meca=DB.authMechanism))

        client = pymongo.MongoClient(uri)
        DB.DATABASE = client['pandachatbot']

    # Finding method
    @staticmethod
    def find_one(collection, query):
        return DB.DATABASE[collection].find_one(query)

    # Inserting method
    @staticmethod
    def insert_one(collection, query):
        return DB.DATABASE[collection].insert_one(query)


def save(data_object):
    try:
        db = DB()
        db.Collection = 'history'
        db.init()
        db.insert_one(db.Collection, data_object)
        print("Request saved to MongoDB")
    except "connection failed":
        print("Could not save request data to MongoDB")
