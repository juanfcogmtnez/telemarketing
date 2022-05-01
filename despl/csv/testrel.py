import pandas as pd
import json
import pymongo
from pymongo import MongoClient
import numpy as np

proyecto = 'base'
unit = pd.read_csv('units.csv', encoding='utf-8-sig')
sunit = pd.read_csv('sub_unit.csv', encoding='utf-8-sig')
room = pd.read_csv('t_unit_rooms2.csv', encoding='utf-8-sig')
items = pd.read_csv('t_room_items3.csv', encoding='utf-8-sig')
rooms = pd.read_csv('t_rooms2.csv', encoding='utf-8-sig')

print(unit)
print(sunit)

newdf = pd.DataFrame()

unidades = []
sub_unidades = []
unidades_name = []
sub_unidades_name = []

def room_name(room):
    for a in range(len(room)):
        if rooms.loc[a][0] == room:
            return (rooms.loc[a][2])

def unit_name(unidad):
    for a in range(len(unit)):
        if unit.loc[a][0] == unidad:
            return (unit.loc[a][2])

def sunit_name(sunidad):
    for a in range(len(sunidad)):
        if sunit.loc[a][1] == sunidad:
            return (sunit.loc[a][3])


for z in range(len(unit)):
    unidades.append(unit.loc[z][0])
    unidades_name.append(unit.loc[z][2])

for y in range(len(sunit)):
    sub_unidades.append(sunit.loc[y][1])
    sub_unidades_name.append(sunit.loc[y][3])

for i in range(len(items)):
    item = items.loc[i][3]
    item_qty = items.loc[i][9]
    tipoA = items.loc[i][4]
    tipoB = items.loc[i][5]
    local = items.loc[i][2]
    item_es = items.loc[i][7]
    for r in range(len(room)):
        if local == room.loc[r][1]:
            area = room.loc[r][3]
            local_qty = room.loc[r][5]
            local_sup = room.loc[r][6]
    if items.loc[i][1] in unidades:
        unidad = items.loc[i][1]
        sub_unidad = "general"
    else:
        for y in range(len(sunit)):
            if sunit.loc[y][1] == items.loc[i][1]:
                unidad = sunit.loc[y][0]
                sub_unidad = sunit.loc[y][1]
    unidad_es = unit_name(unidad)
    if sub_unidad != "general":
        sub_unidad_es = sunit_name(sub_unidad)
    else:
        sub_unidad_es = "general"
    room_es = room_name(local)
    row = {"proyecto":"base","unidad":unidad,"unidad_es":unidad_es,"sub-unidad":sub_unidad,"sub_unidad_es":sub_unidad_es,"area":area,"room":local,"room_es":room_es,"room_qty":local_qty,"room_sup":local_sup,"tipoA":tipoA,"tipoB":tipoB,"item":item,"item_es":item_es,"item_qty":item_qty}
    newdf = newdf.append(row, ignore_index = True)
    avance = i*100 / len(items)
    avance = round(avance, 2)
    print(avance, "%")

'''
for x in range(len(room)):
    local = room.loc[x][1]
    area = room.loc[x][3]
    local_qty = room.loc[x][5]
    local_sup = room.loc[x][6]
    if not pd.isnull(local):
        print("local objetivo:",local)
        if room.loc[x][0] in unidades:
            unidad = room.loc[x][0]
            sub_unidad = "general"
        else:
            for y in range(len(sunit)):
                if sunit.loc[y][1] == room.loc[x][0]:
                    unidad = sunit.loc[y][0]
                    sub_unidad = sunit.loc[y][1]
        row = {"proyecto":"base","unidad":unidad,"sub-unidad":sub_unidad,"area":area,"room":local,"room_qty":local_qty,"room_sup":local_sup}
        newdf = newdf.append(row, ignore_index = True)


for z in range(len(sunit)):
    unidad = sunit.loc[z][0]
    sub_unidad = sunit.loc[z][1]
    row = {"proyecto":"base","unidad":unidad,"sub-unidad":sub_unidad}
    newdf = newdf.append(row, ignore_index = True)

for y in range(len(unit)):
    unidad = unit.loc[y][0]
    sub_unidad = "general"
    row = {"proyecto":"base","unidad":unidad,"sub-unidad":sub_unidad}
    newdf = newdf.append(row, ignore_index = True)
'''

newdf.to_csv('testrel.csv',index=False)
