import pandas as pd
import json
import pymongo
from pymongo import MongoClient

df = pd.read_csv('despl/csv/t_rooms2.csv', encoding='utf-8-sig')

print (df)

client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
db = client["base"]
col = db["rooms"]

my_list = df.columns.values.tolist()
print(my_list)
docs = []
for column in my_list:
    if column.startswith('datasheet') or column.startswith('layout'):
        docs.append(column)
print(docs)
df_docs = df[docs]
print(df_docs)
for doc in docs:
    del df[doc]

print(df)

for i in range(len(df)):
    dict = {'basicos':{},'adicionales':{},'docs':{}}
    row = df.loc[i].to_dict()
    dict['basicos'] = row
    rowdoc = df_docs.loc[i].to_dict()
    dict['docs'] = rowdoc
    print(dict)
    x = col.insert_one(dict)
