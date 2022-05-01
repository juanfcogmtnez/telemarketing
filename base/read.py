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

#basico para operaciones de conexion
def get_db():
    client = MongoClient('mongodb://%s:%s@localhost:27017' % ('root', 'pass'))
    db = client["simalga_db"]
    return db

#captura las colecciones para index
def col():
    db = get_db()
    collect = db.list_collection_names()
    proyectos = []
    lista = []
    for col in collect:
        proyectos.append(col)
    proyectos.remove('users')
    for proyecto in proyectos:
        #print (proyecto)
        mycol = db[proyecto]
        for x in mycol.find({}):
            lista.append(x)
    return dumps(lista)

#captura las colecciones para index
def unit(proj):
    db = get_db()
    col = db[proj]
    for x in col.find({},{ "unidades": 1}):
        return dumps(x)

#captura la coleccion base completa
def all(proy):
    db = get_db()
    mycol = db[proy]
    x = mycol.find()
    for element in x:
        return dumps(element)

#cambia los estados en kanban de proyectos
def set_estado(id,estado):
    print(id)
    db = get_db()
    mycol = db[id]
    myquery = {}
    newvalues = { "$set": {"auto.estado": estado} }
    mycol.update_one(myquery, newvalues)
    return ('update', id, estado)

#cambia los estados en kanban de proyectos
def set_estadoin(proj,unit,estado):
    db = get_db()
    mycol = db[proj]
    myquery = {}
    newvalues = { "$set": {"unidades."+unit+".estado": estado} }
    print(newvalues)
    mycol.update_one(myquery, newvalues)
    return ('updatein', proj, unit, estado)

def insert(data):
    #print (data)
    #print('type',type(data))
    longo = len(data)
    claves = []
    keys = data.keys()
    for key in keys:
        claves.append(key)
    #print (claves)
    #print(claves[0])
    llaves = json.loads(claves[0])
    #print(llaves)
    longo = len(llaves)
    db = get_db()
    tipo = llaves[0]['tipo']
    if tipo == "proyecto":
        for i in range(longo):
            if 'basicos' in llaves[i]:
                if 'nombre' in llaves[i]['basicos']:
                    pos = i
                    print ('posicion:',i)
        nombre = llaves[pos]['basicos']['nombre']
        #print('nombre:',nombre)
        newdict = {"adicionales":{},"basicos":{},"auto":{},"unidades":{}}
        for i in range(longo):
            if 'basicos' in llaves[i]:
                newdict['basicos'].update(llaves[i]['basicos'])
            if 'adicionales' in llaves[i]:
                newdict['adicionales'].update(llaves[i]['adicionales'])
            newdict.update({"nombre":nombre})
        col = db['base']
        for x in col.find({},{ "unidades": 1,"auto":1}):
            newdict['unidades'].update(x['unidades'])
            newdict['auto'].update(x['auto'])
        collist = db.list_collection_names()
        if nombre in collist and tipo == "proyecto":
            return ('Ese nombre de proyecto ya existe por favor introduce otro')
        else:
            col = db[nombre]
            x = col.insert_one(newdict)
            #dico = json.loads(llaves[0].strip(']['))
            return 'OK'
    if tipo == "eproyecto":
        for i in range(longo):
            if 'basicos' in llaves[i]:
                if 'nombre' in llaves[i]['basicos']:
                    pos = i
                    print ('posicion:',i)
        nombre = llaves[pos]['basicos']['nombre']
        col = db[nombre]
        print('nombre:',nombre)
        basicos = {}
        adicionales = {}
        for i in range(longo):
            if 'basicos' in llaves[i]:
                key = llaves[i]['basicos'].keys()
                cles = []
                for k in key:
                    basicos[k] = llaves[i]['basicos'][k]
            if 'adicionales' in llaves[i]:
                key = llaves[i]['adicionales'].keys()
                cles = []
                for k in key:
                    adicionales[k] = llaves[i]['adicionales'][k]
        print(basicos)
        print(adicionales)
        myquery = {}
        newvalues = { "$set": {"basicos": basicos} }
        col.update_one(myquery, newvalues)
        myquery = {}
        newvalues = { "$set": {"adicionales": adicionales} }
        col.update_one(myquery, newvalues)
        return 'OK'
    if tipo == "unidad":
        projecto = llaves[0]['proyecto']
        for i in range(longo):
            if 'basicos' in llaves[i]:
                if 'nombre' in llaves[i]['basicos']:
                    pos = i
                    print ('posicion:',i)
        nombre = llaves[pos]['basicos']['nombre']
        #print('nombre:',nombre)
        newdict = {"adicionales":{},"basicos":{},"auto":{},"rooms":{}}
        for i in range(longo):
            if 'basicos' in llaves[i]:
                newdict['basicos'].update(llaves[i]['basicos'])
            if 'adicionales' in llaves[i]:
                newdict['adicionales'].update(llaves[i]['adicionales'])
            newdict.update({"nombre":nombre})
        col = db['base']
        for x in col.find({},{ "unidades": 1,"auto":1}):
            newdict['unidades'].update(x['unidades'])
            newdict['auto'].update(x['auto'])
            #debo meter todas las habitaciones con equipos
        collist = db.list_collection_names()
        if nombre in collist and tipo == "proyecto":
            return ('Ese nombre de proyecto ya existe por favor introduce otro')
        else:
            col = db[proyecto]
            x = col.insert_one(newdict)
            #dico = json.loads(llaves[0].strip(']['))
            return 'OK'
    if tipo == "eunidad":
        projecto = llaves[1]['proyecto']
        unidad = llaves[2]['unidad']
        basicos = {}
        adicionales = {}
        for i in range(longo):
            if 'basicos' in llaves[i]:
                key = llaves[i]['basicos'].keys()
                cles = []
                for k in key:
                    basicos[k] = llaves[i]['basicos'][k]
            if 'adicionales' in llaves[i]:
                key = llaves[i]['adicionales'].keys()
                cles = []
                for k in key:
                    adicionales[k] = llaves[i]['adicionales'][k]
        print(basicos)
        print(adicionales)
        col = db[projecto]
        myquery = {}
        newvalues = { "$set": {"unidades."+unidad+".basicos":basicos} }
        col.update_one(myquery, newvalues)
        newvalues = { "$set": {"unidades."+unidad+".adicionales":adicionales} }
        col.update_one(myquery, newvalues)
        return 'OK'
