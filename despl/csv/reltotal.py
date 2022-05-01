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
opt = pd.read_csv('opciones2.csv',encoding='utf-8-sig')

print(opt)

unidades = []
sub_unidades = []
unidades_name = []
sub_unidades_name = []

for z in range(len(unit)):
    unidades.append(unit.loc[z][0])
    unidades_name.append(unit.loc[z][2])

for y in range(len(sunit)):
    sub_unidades.append(sunit.loc[y][1])
    sub_unidades_name.append(sunit.loc[y][3])


def name_item(item):
    print("busca en items",item)
    for y in range(len(items)):
        if items.loc[y][3] == item:
            return ([items.loc[y][7],items.loc[y][9],items.loc[y][4],items.loc[y][5],items.loc[y][2]])

def room_name(local):
    print("busca en rooms",local)
    for x in range(len(rooms)):
        if rooms.loc[x][0] == local:
            return rooms.loc[x][2]

def room_car(local):
    print("busca en car",local)
    for w in range(len(room)):
        if room.loc[w][1] == local:
            return([room.loc[w][5],room.loc[w][6],room.loc[w][3],room.loc[w][0]])

def sunidad_name(unidad):
    print("busca en su",unidad)
    for u in range(len(sunit)):
        if sunit.loc[u][1] == unidad:
            return ([sunit.loc[u][0],sunit.loc[u][1],sunit.loc[u][3]])

def unidad_name(unidad):
    print("busca en u",unidad)
    for v in range(len(unit)):
        if unit.loc[v][0] == unidad:
            return ([unit.loc[v][2],"GEN","general"])
        else:
            sunidad_name(unidad)


reltotal = pd.DataFrame()

for z in range(len(opt)):
    item_code = opt.loc[z][0]
    fabricante = opt.loc[z][1]
    modelo = opt.loc[z][2]
    coste = opt.loc[z][3]
    equipo = name_item(item_code)
    if equipo != None:
        item_es = equipo[0]
        item_qty = equipo[1]
        tipoA = equipo[2]
        tipoB = equipo[3]
        local = equipo[4]
        room_es = room_name(local)
        rooms_qc = room_car(local)
        print("rooms_qc",rooms_qc)
        room_qty = rooms_qc[0]
        room_sup = rooms_qc[1]
        area_es = rooms_qc[2]
        unidad = rooms_qc[3]
        unidad_qc = unidad_name(unidad)
        unidad_es = unidad_qc[0]
        sunidad = unidad_qc[1]
        sunidad_es = unidad_qc[2]
        row = {"proyecto":"base","unidad":unidad,"unidad_es":unidad_es,"sunidad":sunidad,"sunidad_es":sunidad_es,"area_es":area_es,"local":local,"room_es":room_es,"room_qty":room_qty,"room_sup":room_sup,"tipoA":tipoA,"tipoB":tipoB,"item_code":item_code,"item_es":item_es,"item_qty":item_qty,"fabricante":fabricante,"modelo":modelo,"coste":coste}
        reltotal = reltotal.append(row, ignore_index = True)
        print("Añadido: ",row)
    print("Avance", round(z*100/len(opt),2), "%")
    reltotal.to_csv('reltotal.csv',index=False)

for i in range(len(items)):
    item = items.loc[i][3]
    item_qty = items.loc[i][9]
    tipoA = items.loc[i][4]
    tipoB = items.loc[i][5]
    local = items.loc[i][2]
    item_es = items.loc[i][7]
    item_qc = name_item(item)
    local = item_qc[4]
    local_es = room_name(local)
    room_qc = room_car(local)
    local_qty =rooms_qc[0]
    local_sup = rooms_qc[1]
    area = rooms_qc[2]
    unidad = rooms_qc[3]
    unidad_qc = unidad_name(unidad)
    unidad_es = unidad_qc[0]
    sunidad = unidad_qc[1]
    sunidad_es = unidad_qc[2]
    row = {"proyecto":"base","unidad":unidad,"unidad_es":unidad_es,"sunidad":sunidad,"sunidad_es":sunidad_es,"area_es":area,"local":local,"room_es":local_es,"room_qty":local_qty,"room_sup":local_sup,"tipoA":tipoA,"tipoB":tipoB,"item_code":item,"item_es":item_es,"item_qty":item_qty,"fabricante":"","modelo":"","coste":""}
    print("Añade",row)
    reltotal = reltotal.append(row, ignore_index = True)
    avance = i*100 / len(items)
    avance = round(avance, 2)
    print(avance, "%")
    reltotal.to_csv('reltotal.csv',index=False)
