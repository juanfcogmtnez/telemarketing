import pymongo
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
# importing the required libraries
from pymongo import MongoClient
from bson.json_util import dumps
import pprint
import json
import warnings
import jsonify
from bson.objectid import ObjectId
import pandas as pd


client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
db = client["base"]
col = db['rel']
mydoc = col.find({"item":"hola"},{"_id":0,"local":1})

i = 0
for x in mydoc:
    i = i+1
    print(x)
    if x == None:
        print("none")

print(i)