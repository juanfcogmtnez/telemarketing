import pandas as pd
import json
import pymongo
from pymongo import MongoClient

df = pd.read_csv('despl/csv/units.csv', encoding='utf-8-sig')
print(df)

client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
db = client["base"]
col = db["relpu"]

for i in range(len(df)):
    dict = {"basicos":{"unit_code":df.loc[i][0],"unit_es":df.loc[i][2],"estado":df.loc[i][7],"nombre_cliente":''},"adicionales":{}}
    print(dict)
    x = col.insert_one(dict)
