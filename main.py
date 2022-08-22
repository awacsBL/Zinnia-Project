import os
import pprint
from twitter import TwitterSearchScraper
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

# load_dotenv(find_dotenv())
#
# connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
# client = MongoClient(connection_string)
#
# dbs = client.list_database_names()
# print(dbs)
# test_db = client.testdb
# collections = test_db.list_collection_names()
# print(collections)

tweets_list = []
f = open("test.jsonl", "a")
for i, test in enumerate(TwitterSearchScraper('hi').get_items()):
    if i > 10:
        break
    f.write(test.json()+"\n")
f.close()
