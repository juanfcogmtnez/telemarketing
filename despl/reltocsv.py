import pandas as pd
import json
import pymongo
from pymongo import MongoClient


proyecto = 'base'
unit = pd.read_csv('csv/units.csv', encoding='utf-8-sig')
sunit = pd.read_csv('csv/sub_unit.csv', encoding='utf-8-sig')
room = pd.read_csv('csv/t_unit_rooms2.csv', encoding='utf-8-sig')
items = pd.read_csv('csv/t_room_items3.csv', encoding='utf-8-sig')
rooms = pd.read_csv('csv/t_rooms2.csv', encoding='utf-8-sig')
opt = pd.read_csv('csv/opciones2.csv',encoding='utf-8-sig')

client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
db = client["base"]
col = db["rel"]


reltotal = pd.DataFrame()

def nombre_unidad(unidad):
    for z in range(len(unit)):
        if unit.loc[z][0] == unidad:
            return unit.loc[z][2]

def nombre_sunidad(sunidad):
    for z in range(len(sunit)):
        if sunit.loc[z][1] == sunidad:
            return sunit.loc[z][3]

def nombre_item(item):
	for y in range(len(items)):
		if items.loc[y][3] == item:
			return items.loc[y][7]

def ta_item(item):
	for y in range(len(items)):
		if items.loc[y][3] == item:
			return items.loc[y][4]

def tb_item(item):
	for y in range(len(items)):
		if items.loc[y][3] == item:
			return items.loc[y][5]

def qty_item(item):
	for y in range(len(items)):
		if items.loc[y][3] == item:
			return items.loc[y][9]

def local_item(item):
	for y in range(len(items)):
		if items.loc[y][3] == item:
			return items.loc[y][2]

def unit_item(item):
	for y in range(len(items)):
		if items.loc[y][3] == item:
			return items.loc[y][1]

def be_unidad(unidad):
    lista = []
    for z in range(len(unit)):
        lista.append(unit.loc[z][0])
    if unidad in lista:
        return "si"
    else:
        return "no"   

def be_sunidad(unidad):
    for y in range(len(sunit)):
        if unit.loc[y][0] == unidad:
            return unit.loc[y][2]

def buscar_padre(sunidad):
    for y in range(len(sunit)):
        if sunit.loc[y][1] == sunidad:
            return sunit.loc[y][0]

def localqty(local):
    for x in range(len(room)):
        if room.loc[x][1] == local:
            return room.loc[x][5]

def localsup(local):
    for x in range(len(room)):
        if room.loc[x][1] == local:
            return room.loc[x][6]
def locales(local):
    for x in range(len(room)):
        if room.loc[x][1] == local:
            return room.loc[x][11]

for z in range(len(unit)):
    print (unit.loc[z][0])
    unidad = unit.loc[z][0]
    unidad_es = unit.loc[z][2]
    #row = {"proyecto":"base","unidad":unidad,"unidad_es":unidad_es,"sunidad":unidad,"sunidad_es":unidad_es}
    #reltotal = reltotal.append(row, ignore_index = True)
    #reltotal.to_csv('reltotal.csv',index=False)

for y in range(len(sunit)):
    sunidad = sunit.loc[y][1]
    unidad = sunit.loc[y][0]
    unidad_es = nombre_unidad(unidad)
    sunidad_es = sunit.loc[y][3]
    #row = {"proyecto":"base","unidad":unidad,"unidad_es":unidad_es,"sunidad":sunidad,"sunidad_es":sunidad_es}
    #reltotal = reltotal.append(row, ignore_index = True)
    #reltotal.to_csv('reltotal.csv',index=False)

for x in range(len(room)):
    local = room.loc[x][1]
    local_qty = room.loc[x][5]
    local_sup = room.loc[x][6]
    local_es = room.loc[x][11]
    unidad = room.loc[x][0]
    unidad_es = be_unidad(unidad)
    if unidad_es == None:
        sunidad_es = be_sunidad(unidad)
        sunidad = unidad
        unidad = buscar_padre(unidad)
        unidad_es = nombre_unidad(unidad)
    else:
        sunidad_es = unidad_es
        sunidad = unidad
    #row = {"proyecto":"base","unidad":unidad,"unidad_es":unidad_es,"sunidad":sunidad,"sunidad_es":sunidad_es,"local":local,"local_qty":local_qty,"local_sup":local_sup,"local_es":local_es}
    #reltotal = reltotal.append(row, ignore_index = True)
    #reltotal.to_csv('reltotal.csv',index=False)

for w in range(len(items)):
    item = items.loc[w][3]
    tipoA = items.loc[w][4]
    tipoB = items.loc[w][5]
    item_qty = items.loc[w][9]
    item_es = items.loc[w][7]
    local = items.loc[w][2]
    local_qty = localqty(local)
    print("pregunto por",local,"localqty respuesta",local_qty)
    local_sup = localsup(local)
    local_es = locales(local)
    unidad = items.loc[w][1]
    esunidad = be_unidad(unidad)
    print("la unidad es",unidad)
    print("la respuesta es",esunidad)
    if esunidad == "si":
        print(unidad, "es unidad")
        unidad = items.loc[w][1]
        unidad_es = nombre_unidad(unidad)
        sunidad = unidad
        sunidad_es = unidad_es
    else:
        unidad = buscar_padre(unidad)
        unidad_es = nombre_unidad(unidad)
        sunidad = items.loc[w][1]
        sunidad_es = nombre_sunidad(sunidad)
    row = {"proyecto":"base","unidad":str(unidad),"unidad_es":str(unidad_es),"unidad_cliente":"","sunidad":str(sunidad),"sunidad_es":str(sunidad_es),"sunidad_cliente":"","local":str(local),"local_qty":str(local_qty),"local_sup":str(local_sup),"local_es":str(local_es),"local_cliente":"","tipoA":str(tipoA),"tipoB":str(tipoB),"item":str(item),"item_qty":str(item_qty),"item_es":str(item_es),"item_cliente":"","fabricante":"","modelo":"","coste":"","ref_proyecto":"","fecha":""}
    reltotal = reltotal.append(row, ignore_index = True)
    print(row)
    print (round(w*100/len(items),2),"%")
    reltotal.to_csv('reltotal.csv',index=False)
    #x = col.insert_one(row)

for u in range(len(opt)):
	fabricante = opt.loc[u][1]
	modelo = opt.loc[u][2]
	coste = opt.loc[u][3]
	item = opt.loc[u][0]
	item_es = nombre_item(item)
	tipoA = ta_item(item)
	tipoB = tb_item(item)
	item_qty = qty_item(item)
	local = local_item(item)
	local_qty = localqty(local)
	local_sup = localsup(local)
	local_es = locales(local)
	unidad = unit_item(item)
	esunidad = be_unidad(unidad)
	print("la unidad es",unidad)
	print("la respuesta es",esunidad)
	if esunidad == "si":
		print(unidad, "es unidad")
		unidad = items.loc[w][1]
		unidad_es = nombre_unidad(unidad)
		sunidad = unidad
		sunidad_es = unidad_es
	else:
		unidad = buscar_padre(unidad)
		unidad_es = nombre_unidad(unidad)
		sunidad = items.loc[w][1]
		sunidad_es = nombre_sunidad(sunidad)
	row = {"proyecto":"base","unidad":str(unidad),"unidad_es":str(unidad_es),"unidad_cliente":"","sunidad":str(sunidad),"sunidad_es":str(unidad_es),"sunidad_cliente":"","local":str(local),"local_qty":str(local_qty),"local_sup":str(local_sup),"local_es":str(local_es),"local_cliente":"","tipoA":str(tipoA),"tipoB":str(tipoB),"item":str(item),"item_qty":str(item_qty),"item_es":str(item_es),"item_cliente":"","fabricante":str(fabricante),"modelo":str(modelo),"coste":str(coste),"ref_proyecto":"medipole","fecha":"12/2020"}
	reltotal = reltotal.append(row, ignore_index = True)
	print(row)
	print (round(w*100/len(items),2),"%")
	reltotal.to_csv('reltotal.csv',index=False)
    #x = col.insert_one(row)
   
	
	
