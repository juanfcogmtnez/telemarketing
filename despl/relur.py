import pandas as pd
import json
import pymongo
from pymongo import MongoClient

df = pd.read_csv('despl/csv/t_unit_rooms2.csv', encoding='utf-8-sig')
print(df)

client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
db = client["base"]
col = db["relur"]

for i in range(len(df)):
    if not pd.isnull(df.loc[i][1]):
        dict = {"basicos":{"asc":"base","from":df.loc[i][0],"to":df.loc[i][1],"room_es":df.loc[i][11],"cantidad":df.loc[i][5],"m2":df.loc[i][6],"area":df.loc[i][2],"remarks_es":df.loc[i][8],"estado":"def","nombre_cliente":""},"adicionales":{}}
        print(dict)
        x = col.insert_one(dict)

db = client["base"]
col = db["relur"]
