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
import pandas as pd
warnings.filterwarnings('ignore')

def get_db():
    client = MongoClient('mongodb://%s:%s@mongo_visioncrm:27017' % ('root', 'pass'))
    db = client["vision_db"]
    return db

def contacts(lista):
    db = get_db()
    col = db[lista]
    myquery = {}
    mydoc = col.find(myquery)
    df =  pd.DataFrame(list(mydoc))
    print(df)
    df = df.sort_values(by=['Open_Count','Clicked_Links_Count'], ascending=False)
    print(df)
    resultado = df.to_dict('records')
    print(resultado)
    return dumps(resultado)

def ficha(email):
    db = get_db()
    col = db['contactos']
    myquery = {'EMAIL':email}
    mydoc = col.find_one(myquery)
    return dumps(mydoc)

def campa(lista,email):
    db = get_db()
    col = db[lista]
    myquery = {'Email_ID':email}
    mydoc = col.find_one(myquery)
    return dumps(mydoc)

def gpais():
    db = get_db()
    cols = db.list_collection_names()
    lista = []
    for col in cols:
        lista.append(col)
    lista.remove("users")
    lista.remove("contactos")
    lista.remove("llamadas")
    return dumps(lista)

def llamada(result,user,client,lista):
    db = get_db()
    col = db[lista]
    myquery = {'Email_ID':client}
    newvalues = { "$set": { "llamado": "si" } }
    col.update_one(myquery, newvalues)
    db = get_db()
    col = db['llamadas']
    x = col.insert_one({"cliente":client,"resultado":result,"agente":user})
    return "ok"

def set_update(email,company,name,surname,tel,family,pais,lista):
    if lista == "españ":
        lista = "españa"
    db = get_db()
    col = db['contactos']
    myquery = {'EMAIL':email}
    mydoc = col.find(myquery)
    item = 0
    for x in mydoc:
        item = item +1
    if item > 0:
        newvalues = { "$set": { "EMAIL": email,"EMPRESA":company,"TELEFONO":tel,"FAMILIA":family,"APELLIDOS":surname,"NOMBRE":name,"LISTA":lista,"PAIS":pais } }
        col.update_one(myquery, newvalues)
    else:
        x = col.insert_one({"EMAIL": email,"EMPRESA":company,"TELEFONO":tel,"FAMILIA":family,"APELLIDOS":surname,"NOMBRE":name,"LISTA":lista,"PAIS":pais})
    return '<script>window.location.assign("/hola/'+lista+'");</script>'

def autoupdate(email,company,name,surname,tel,family,pais,lista):
    if lista == "españ":
        lista = "españa"
    db = get_db()
    col = db['contactos']
    myquery = {'EMAIL':email}
    mydoc = col.find(myquery)
    item = 0
    for x in mydoc:
        item = item +1
    if item > 0:
        newvalues = { "$set": { "EMAIL": email,"EMPRESA":company,"TELEFONO":tel,"FAMILIA":family,"APELLIDOS":surname,"NOMBRE":name,"LISTA":lista,"PAIS":pais } }
        col.update_one(myquery, newvalues)
    else:
        x = col.insert_one({"EMAIL": email,"EMPRESA":company,"TELEFONO":tel,"FAMILIA":family,"APELLIDOS":surname,"NOMBRE":name,"LISTA":lista,"PAIS":pais})
    return 'ok'