import pandas as pd
import json
import pymongo
from pymongo import MongoClient


df = pd.read_csv('csv/opciones2.csv', encoding='utf-8-sig')

print (df)


client = MongoClient('mongodb://%s:%s@localhost:27017' % ('root', 'pass'))
db = client["base"]
col = db["opts"]

for i in range(len(df)):
    dict = df.loc[i].to_dict()
    dict['coste'] = round(float(dict['coste']),2)
    print(dict)
    x = col.insert_one(dict)