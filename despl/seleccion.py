import pymongo
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
# importing the required libraries
from pymongo import MongoClient
from bson.json_util import dumps
import pprint
import json
import warnings
import jsonify
from bson.objectid import ObjectId
import pandas as pd

#basico para operaciones de conexion
def get_db():
    client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
    db = client["simalga_db"]
    return client

def cal_barato(proy,item,cal):
    client = get_db()
    db = client[proy]
    col = db['opts']
    doc = col.find({"item_code":item,"calidad":cal})
    seleccionado = {'coste':99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}
    for x in doc:
        if x['coste'] < seleccionado['coste']:
            seleccionado = x
        return seleccionado 

def solo_barato(proy,item):
    client = get_db()
    db = client[proy]
    col = db['opts']
    doc = col.find({"item_code":item})
    seleccionado = {'coste':99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}
    for x in doc:
        if x['coste'] < seleccionado['coste']:
            seleccionado = x
        return seleccionado 

def seleccion(proy,objetivo):

    client = get_db()
    db = client[proy]
    col = db['rel']
    doc = col.find({})

    items = []
    for x in doc:
        if x['item'] not in items:
            items.append(x['item'])

    print(items)

    client = get_db()
    db = client[proy]
    col = db['rel']
    doc = col.find({})

    for item in doc:
        check = tiene_oferta(proy,item['item'])
        if check == 'si':
            #print(item, " tiene oferta")
            select = cal_barato(proy,item['item'],objetivo)
            #print ("select claidad es: ",select)
            if select != None:
                #print ("not none")
                if item['estado'] != 'cons':
                    #print("no cons")
                    newval = {"$set":{"estado":"def","fabricante":select['fabricante'],"modelo":select['modelo'],"coste":select['coste'],"ref_proyecto":select['ref_proyecto'],"fecha":select['fecha'],"n_oferta":select['n_oferta']}}
                    col.update_one(item,newval)
                    #print("update done")
            else:
                select = solo_barato(proy,item['item'])
                #print ("select precio es: ",select)
                if item['estado'] != 'cons':
                    newval = {"$set":{"estado":"def","fabricante":select['fabricante'],"modelo":select['modelo'],"coste":select['coste'],"ref_proyecto":select['ref_proyecto'],"fecha":select['fecha'],"n_oferta":select['n_oferta']}}
                    col.update_one(item,newval)
        else:
            #print(item, " no tiene oferta")
            client = get_db()
            db = client[proy]
            col = db['rel']
            newval = {"$set":{"estado":"sin"}}
            col.update_one(item,newval)
    return "ok"

def tiene_oferta(proy,item):
    client = get_db()
    db = client[proy]
    col = db['opts']
    doc = col.find({})
    ofertas = []
    for x in doc:
        if x['item_code'] not in ofertas:
            ofertas.append(x['item_code'])

    if item in ofertas:
        return 'si'
    else:
        return 'no'