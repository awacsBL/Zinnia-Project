import os
from bson.son import SON
from bson.json_util import dumps, loads
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient


load_dotenv(find_dotenv())

connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
client = MongoClient(connection_string)

db = client["ZinniaProjectDB"]
collection = db["tweets"]


def aggregationQuery(pipeline):
    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=True
    )

    try:
        cursorList = list(cursor)
        jsonData = dumps(cursorList, indent=2)
        return jsonData
    finally:
        cursor.close()


def topHashtagsPipeline():
    return [
        {
            u"$unwind": {
                u"path": u"$hashtags",
                u"preserveNullAndEmptyArrays": False
            }
        },
        {
            u"$group": {
                u"_id": u"$hashtags",
                u"tagCount": {
                    u"$sum": 1
                }
            }
        },
        {
            u"$sort": SON([(u"tagCount", -1)])
        },
        {
            u"$limit": 100
        }
    ]


def topHashtagsQuery():
    return aggregationQuery(topHashtagsPipeline())
