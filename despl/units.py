import pandas as pd
import json
import pymongo
from pymongo import MongoClient

df = pd.read_csv('despl/csv/units.csv', encoding='utf-8-sig')

print (df)


client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
db = client["base"]
col = db['propiedades']
col.insert_one({'basicos':{'fecha_inicio':'','fecha_fin':'','nombre':'base','objetivo':'media'},'adicionales':{}})
col = db["unidades"]

for i in range(len(df)):
    dict = {'basicos':{},'adicionales':{}}
    row = df.loc[i].to_dict()
    dict['basicos'] = row
    print(dict)
    x = col.insert_one(dict)
