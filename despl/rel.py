import pandas as pd
import json
import pymongo
from pymongo import MongoClient


df = pd.read_csv('csv/reltotal.csv',encoding='utf-8-sig')

print(df)

client = MongoClient('mongodb://%s:%s@localhost:27017' % ('root', 'pass'))
db = client["base"]
col = db["rel"]


for x in range(len(df)):
	row = df.loc[x].to_dict()
	print(row)
	if row['coste'] != 'NaN':
		row['coste'] = round(float(row['coste']),2)
	if row['local_qty'] == 'NaN':
		row['local_qty'] == 0
	y = col.insert_one(row)
	print (round(x*100/len(df),2),"%")
