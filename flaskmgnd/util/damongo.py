from flaskmgnd.util.pojo import Pojo
from pymongo import MongoClient
from bson import ObjectId

class MongoConfigClass(Pojo):
    host: str
    port: str
    username: str
    password: str
    database: str

class DaMongo:
    creds: MongoConfigClass
    client: MongoClient

    def __init__(self, creds_param) -> None:
        self.creds = MongoConfigClass(creds_param)
        self.connect()

    def connect(self):
        uri = f"mongodb://{self.creds.username}:{self.creds.password}@{self.creds.host}:{self.creds.port}/?authSource=admin"
        self.client = MongoClient(uri)

    def index_control(self):
        pass

    def disconnect(self):
        self.client.close()

    def insert(self, collection:str, data: list) -> list:
        res = self.client[self.creds.database][collection].insert_many(data)
        data = self.result_id_edit(data, with_id=False)
        return [str(e) for e in res.inserted_ids]

    def select(self, collection: str, query: dict, with_id: bool = False) -> list:
        query = self.query_id_edit(query)
        res = list(self.client[self.creds.database][collection].find(query))
        return self.result_id_edit(res, with_id)

    def delete(self, collection: str, query: dict) -> list:
        query = self.query_id_edit(query)
        res = self.client[self.creds.database][collection].delete_many(query)
        return res.deleted_count


    def update(self, collection: str, query: dict, data: dict):
        query = self.query_id_edit(query)
        res = self.client[self.creds.database][collection].update_many(query, {"$set" : data})
        return res.modified_count

    def query_id_edit(self, query):
        if "_id" in query.keys():
            if isinstance(query, dict) and "$in" in query["_id"]:
                query["_id"]["$in"] = [ObjectId(e) for e in query["_id"]["$in"]]
            else:
                query["_id"] = ObjectId(query["_id"])
        return query

    def result_id_edit(self, res, with_id):
        if with_id:
            for i in range(len(res)):
                res[i]["_id"] = str(res[i]["_id"])
        else:
            for i in range(len(res)):
                del res[i]["_id"]
        return res