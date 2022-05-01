import pandas as pd
import json
import pymongo
from pymongo import MongoClient


df = pd.read_csv('despl/csv/t_items3.csv', encoding='utf-8-sig')

print (df)


client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
db = client["base"]
col = db["items"]

for i in range(len(df)):
    dict = {"basicos":{ "code":str(df.loc[i][1]),"type":str(df.loc[i][0]),"item_en":str(df.loc[i][2]),"item_es":str(df.loc[i][3]),"item_fr":str(df.loc[i][4])},"adicionales":{}}
    print(dict)
    x = col.insert_one(dict)
