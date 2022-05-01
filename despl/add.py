import pandas as pd
import json
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
db = client["base"]
col = db["rel"]

myquery = {}
newvalues = { "$set": {"calidad":""} }

mydoc = col.find(myquery)

for x in mydoc:
  x['calidad'
