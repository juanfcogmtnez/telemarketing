import pandas as pd
import json
import pymongo
from pymongo import MongoClient

df = pd.read_csv('despl/csv/t_room_items3.csv', encoding='utf-8-sig')
print(df)

client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
db = client["base"]
col = db["relre"]



for i in range(len(df)):
    dict = {"basicos":{"estado":"def","asc":df.loc[i][1],"from":df.loc[i][2],"to":df.loc[i][3],"item_name_es":df.loc[i][7],"cantidad":str(df.loc[i][9]),"tipoA":df.loc[i][4],"tipoB":df.loc[i][5],"nombre_cliente":""},"adicionales":{}}
    print(dict)
    x = col.insert_one(dict)
