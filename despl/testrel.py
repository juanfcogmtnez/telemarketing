import pandas as pd
import json
import pymongo
from pymongo import MongoClient

proyecto = 'base'
unit = pd.read_csv('units.csv', encoding='utf-8-sig')
sunit = pd.read_csv('sub_units.csv', encoding='utf-8-sig')

for z in range(len(unit)):
    unit = unit.loc[z][0]
    for y in range(len(sunit)):
        if sunit.loc[y][0] == unit:
            sunit = sunit.loc[y][1]
            print('unit:',unit,'sub:',sunit)
