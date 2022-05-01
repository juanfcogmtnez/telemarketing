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
import despl.seleccion as seleccion
import datetime
import xlsxwriter

#basico para operaciones de conexion
def get_db():
    client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
    db = client["simalga_db"]
    return client

def isNaN(num):
    return num!= num

def get():
    client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
    lista = client.list_database_names()
    print('lista:',lista)
    lista.remove('admin')
    lista.remove('config')
    lista.remove('local')
    lista.remove('simalga_db')
    dict = []
    for l in lista:
        dict.append(l)
    print('dict:',dict)
    if 'base' not in lista:
        import despl.units, despl.sunits,despl.rooms,despl.items,despl.rel,despl.opt
        a = despl.units
        b = despl.sunits
        c = despl.rooms
        d = despl.items
        e = despl.rel
        f = despl.opt
    dictado = {}    
    for i in range(len(dict)):
        dictado[i] = {"nombre":dict[i],"n_def":"","n_sin":"","n_cons":""}
        db = client[dict[i]]
        col = db['rel']
        mydoc = col.find({"proyecto":dict[i]},{"_id":0,"estado":1,"coste":1})
        n_def = 0
        n_sin = 0
        n_cons = 0
        for x in mydoc:
            if x['estado'] == "sin":
                n_sin = n_sin +1
            else:
                if x['estado'] == 'def':
                    n_def = n_def + 1
                if x['estado'] == 'cons':
                    n_cons = n_cons + 1
        dictado[i]["n_def"] = str(n_def)
        dictado[i]["n_sin"] = str(n_sin)
        dictado[i]["n_cons"] = str(n_cons)
    return dumps(dictado)

def getproy():
    client = get_db()
    db = client['base']
    col = db['propiedades']
    myquery = {}
    mydoc = col.find(myquery)
    lista = []
    for x in mydoc:
        lista.append(x)
    return dumps(lista)

def objetivo(proj):
    client = get_db()
    db = client[proj]
    col = db['propiedades']
    myquery = {}
    mydoc = col.find(myquery)
    lista = []
    for x in mydoc:
        print(x)
        lista.append(x)
    return dumps(lista)

def getproyp(proy):
    print('proy:',proy)
    client = get_db()
    db = client[proy]
    col = db['propiedades']
    myquery = {}
    mydoc = col.find(myquery)
    lista = []
    for x in mydoc:
        lista.append(x)
    return dumps(lista)

def getproyu(proy,unit):
    client = get_db()
    db = client[proy]
    col = db['unidades']
    myquery = {"basicos.unit_code":unit}
    mydoc = col.find(myquery)
    filtro1 = []
    for x in mydoc:
        filtro1.append(x)
    return dumps(filtro1)

def getproysu(proy,unit,sunit):
    client = get_db()
    db = client[proy]
    col = db['sub_unidades']
    myquery = {"basicos.unit_code":sunit,"basicos.asc_unit":unit}
    print(myquery)
    mydoc = col.find(myquery)
    filtro1 = []
    for x in mydoc:
        filtro1.append(x)
    return dumps(filtro1)

def getproyr(proy,unit,sunit,room):
    client = get_db()
    db = client[proy]
    col = db['rooms']
    myquery = {"basicos.room_code":room}
    mydoc = col.find(myquery)
    lista = []
    for x in mydoc:
        lista.append(x)
    return dumps(lista)

def getproyi(proy,unit,sunit,room,item):
    client = get_db()
    db = client[proy]
    col = db['items']
    myquery = {"basicos.code":item}
    mydoc = col.find(myquery)
    lista = []
    for x in mydoc:
        lista.append(x)
    return dumps(lista)

def types(proy,unit,sunit,room):
    client = get_db()
    db = client[proy]
    col = db['rel']
    myquery = {}
    mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":sunit,"local":room},{"_id":0,"tipoA":1})
    lista = []
    no_copy = []
    for x in mydoc:
        if x['tipoA'] not in no_copy:
            lista.append(x)
            no_copy.append(x['tipoA'])
    print (lista)
    for t in lista:
        print("tipoA:",t)
        mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":t['tipoA']},{"_id":0,"estado":1,"coste":1})
        n_def = 0
        n_sin = 0
        n_cons = 0
        for x in mydoc:
            if x['estado'] == "sin":
                n_sin = n_sin +1
            else:
                if x['estado'] == 'def':
                    n_def = n_def + 1
                if x['estado'] == 'cons':
                    n_cons = n_cons + 1
        t['n_def'] = str(n_def)
        t['n_sin'] = str(n_sin)
        t['n_cons'] = str(n_cons)
    dictado = dumps(lista)
    return dictado

def typesb(proy,unit,sunit,room,typeA):
    print('estas en typesb')
    client = get_db()
    db = client[proy]
    col = db['rel']
    mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":typeA},{"_id":0,"tipoB":1})
    lista = []
    for x in mydoc:
        if x not in lista:
            lista.append(x)
    print (lista)
    for tb in lista:
        print("tipoA:",tb)
        mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":typeA,"tipoB":tb['tipoB']},{"_id":0,"estado":1,"coste":1})
        n_def = 0
        n_sin = 0
        n_cons = 0
        for x in mydoc:
            if x['estado'] == "sin":
                n_sin = n_sin +1
            else:
                if x['estado'] == 'def':
                    n_def = n_def + 1
                if x['estado'] == 'cons':
                    n_cons = n_cons + 1
        tb['n_def'] = str(n_def)
        tb['n_sin'] = str(n_sin)
        tb['n_cons'] = str(n_cons)
    dictado = dumps(lista)
    return dictado

def opts(proy,unit,sunit,room,typeA,typeB,item):
    client = get_db()
    db = client[proy]
    col = db['rel']
    mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":typeA,"tipoB":typeB,"item":item})
    lista = []
    no_copy = []
    for x in mydoc:
        print ("x es: ",x)
        if x["coste"] not in no_copy and isNaN(x['n_oferta']) != True:
            lista.append(x)
            no_copy.append(x["coste"])
    print("lista:",lista)
    for o in lista:
        print("opt:",o)
        mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":typeA,"tipoB":typeB,"item":item,"n_oferta":o['n_oferta']},{"_id":0,"estado":1,"coste":1})
        n_def = 0
        n_sin = 0
        n_cons = 0
        for x in mydoc:
            if x['coste'] == "NaN":
                n_sin = n_sin +1
            else:
                if x['estado'] == 'def':
                    n_def = n_def + 1
                if x['estado'] == 'cons':
                    n_cons = n_cons + 1
        o['n_def'] = str(n_def)
        o['n_sin'] = str(n_sin)
        o['n_cons'] = str(n_cons)
    dictado = dumps(lista)
    return dictado

def units(proy):
    client = get_db()
    db = client[proy]
    col = db['rel']
    mydoc = col.find({"proyecto":proy},{"unidad":1,"unidad_es":1,"_id":0})
    unidad = []
    no_copy = []
    for x in mydoc:
        if x["unidad"] not in no_copy:
            unidad.append(x)
            no_copy.append(x["unidad"])
    dictado = dumps(unidad)
    print("dictado:",dictado)
    print("unidad:",unidad[0])
    for u in unidad:
        print("unidad:",u)
        mydoc = col.find({"proyecto":proy,"unidad":u['unidad']},{"_id":0,"estado":1,"coste":1})
        n_def = 0
        n_sin = 0
        n_cons = 0
        for x in mydoc:
            if x['estado'] == "sin":
                n_sin = n_sin +1
            else:
                if x['estado'] == 'def':
                    n_def = n_def + 1
                if x['estado'] == 'cons':
                    n_cons = n_cons + 1
        u['n_def'] = str(n_def)
        u['n_sin'] = str(n_sin)
        u['n_cons'] = str(n_cons)
    dictado = dumps(unidad)
    return dictado

def sunits(proy,unit):
    client = get_db()
    db = client[proy]
    col = db['rel']
    mydoc = col.find({"proyecto":proy,"unidad":unit},{"sunidad":1,"sunidad_es":1,"_id":0})
    sunidad = []
    no_copy = []
    for x in mydoc:
        if x["sunidad"] not in no_copy:
            sunidad.append(x)
            no_copy.append(x["sunidad"])
    for s in sunidad:
        print("sunidad:",s)
        mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":s['sunidad']},{"_id":0,"estado":1,"coste":1})
        n_def = 0
        n_sin = 0
        n_cons = 0
        for x in mydoc:
            if x['estado'] == "sin":
                n_sin = n_sin +1
            else:
                if x['estado'] == 'def':
                    n_def = n_def + 1
                if x['estado'] == 'cons':
                    n_cons = n_cons + 1
        s['n_def'] = str(n_def)
        s['n_sin'] = str(n_sin)
        s['n_cons'] = str(n_cons)
    dictado = dumps(sunidad)
    return dictado

def areas(proy,unit,sunit):
    client = get_db()
    db = client[proy]
    col = db['rel']
    mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":sunit},{"area_es":1,"_id":0})
    unidad = []
    unidad_es = []
    for x in mydoc.distinct("area"):
        unidad.append(x)
    return dumps(unidad)

def rooms(proy,unit,sunit):
    print("query room:",proy,unit,sunit)
    client = get_db()
    db = client[proy]
    col = db['rel']
    mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":sunit},{"local":1,"local_es":1,"local_qty":1,"local_sup":1,"_id":0})
    lista = []
    no_copy = []
    for x in mydoc:
        #print ("x es:",x['local'])
        if x['local'] not in no_copy:
            #print("no en lista se añade")
            lista.append(x)
            no_copy.append(x['local'])
    for r in lista:
        print("room:",r)
        mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":sunit,"local":r['local']},{"_id":0,"estado":1,"coste":1})
        n_def = 0
        n_sin = 0
        n_cons = 0
        for x in mydoc:
            if x['estado'] == "sin":
                n_sin = n_sin +1
            else:
                if x['estado'] == 'def':
                    n_def = n_def + 1
                if x['estado'] == 'cons':
                    n_cons = n_cons + 1
        r['n_def'] = str(n_def)
        r['n_sin'] = str(n_sin)
        r['n_cons'] = str(n_cons)
    dictado = dumps(lista)
    return dictado

def items(proy,unit,sunit,room,typeA,typeB):
    print("estas en items",proy,unit,sunit,room,typeA,typeB)
    client = get_db()
    db = client[proy]
    col = db['rel']
    mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":typeA,"tipoB":typeB},{"_id":0,"item":1,"item_qty":1,"item_es":1})
    lista = []
    no_copy = []
    for x in mydoc:
        if x['item'] not in no_copy:
            lista.append(x)
            no_copy.append(x['item'])
    for i in lista:
        print("item:",i)
        mydoc = col.find({"proyecto":proy,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":typeA,"tipoB":typeB,"item":i['item']},{"_id":0,"estado":1,"coste":1})
        n_def = 0
        n_sin = 0
        n_cons = 0
        for x in mydoc:
            if x['estado'] == "sin":
                n_sin = n_sin +1
            else:
                if x['estado'] == 'def':
                    n_def = n_def + 1
                if x['estado'] == 'cons':
                    n_cons = n_cons + 1
        i['n_def'] = str(n_def)
        i['n_sin'] = str(n_sin)
        i['n_cons'] = str(n_cons)
    dictado = dumps(lista)
    return dictado

def coreunit(proy):
    client = get_db()
    db = client[proy]
    col = db['unidades']
    myquery = {"basicos.unit_code":"ICU"}
    mydoc = col.find(myquery)
    lista = []
    for x in mydoc:
        if x not in lista:
            lista.append(x)
    return dumps(lista)

def coreroom(proy,unit):
    client = get_db()
    db = client[proy]
    col = db['rooms']
    myquery = {"basicos.room_code":"1BR-BA"}
    mydoc = col.find(myquery)
    lista = []
    for x in mydoc:
        lista.append(x)
    return dumps(lista)

def allunits():
    client = get_db()
    db = client['base']
    col = db['unidades']
    myquery = {}
    mydoc = col.find({},{"_id":0,"basicos.unit_code":1,"basicos.unit_es":1})
    lista = []
    for x in mydoc:
        lista.append(x)
    return dumps(lista)

def allsunits():
    client = get_db()
    db = client['base']
    col = db['sub_unidades']
    myquery = {}
    mydoc = col.find({},{"_id":0,"basicos.unit_code":1,"basicos.unit_es":1})
    lista = []
    for x in mydoc:
        lista.append(x)
    return dumps(lista)

def allroom():
    client = get_db()
    db = client['base']
    col = db['rooms']
    myquery = {}
    mydoc = col.find(myquery)
    lista = []
    for x in mydoc:
        lista.append(x)
    return dumps(lista)

def allta():
    client = get_db()
    db = client['base']
    col = db['ta']
    myquery = {}
    mydoc = col.find(myquery)
    lista = []
    for x in mydoc:
        lista.append(x)
    return dumps(lista)

def allitems(ta,tb):
    client = get_db()
    db = client['base']
    col = db['items']
    myquery = {"basicos.type":ta}
    mydoc = col.find(myquery)
    lista = []
    for x in mydoc:
        if x["basicos"]["code"].startswith(tb):
            lista.append(x)
    return dumps(lista)

def updatep(data,username):
    print (data)
    print('type',type(data))
    longo = len(data)
    claves = []
    keys = data.keys()
    for key in keys:
        claves.append(key)
    print ("claves0", claves[0])
    llaves = json.loads(claves[0])
    print("llaves:",llaves)
    basicos = []
    adicionales = []
    for i in range(len(llaves)):
        dato = llaves[i]
        print('dato:',dato)
        if "proyecto" in dato:
            proyecto = dato['proyecto']
        if "basicos" in dato:
            basicos.append(dato['basicos'])
        if "adicionales" in dato:
            adicionales.append(dato['adicionales'])
    print('proyecyo: ',proyecto)
    print('nivel:',proyecto)
    editproy = {"basicos":{},"adicionales":{}}
    print(editproy)
    for i in range(len(basicos)):
        editproy['basicos'].update(basicos[i])
    for i in range(len(adicionales)):
        editproy['adicionales'].update(adicionales[i])
    print ('editproy:',editproy)
    print ('proyecto: ',proyecto)
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"actualiza proyecto","nombre":proyecto,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    db = client[proyecto]
    col = db['propiedades']
    myquery = {}
    print ('myquery: ',myquery)
    newvalues = { "$set": editproy}
    x = col.update_one(myquery,newvalues)
    return 'OK'

def updateu(data,username):
    print (data)
    print('type',type(data))
    longo = len(data)
    claves = []
    keys = data.keys()
    for key in keys:
        claves.append(key)
    print ("claves0", claves[0])
    llaves = json.loads(claves[0])
    print("llaves:",llaves)
    basicos = []
    adicionales = []
    for i in range(len(llaves)):
        dato = llaves[i]
        print('dato:',dato)
        if 'unidad' in dato:
            unidad = dato['unidad']
        if 'proyecto' in dato:
            proyecto = dato['proyecto']
        if "basicos" in dato:
            basicos.append(dato['basicos'])
        if "adicionales" in dato:
            adicionales.append(dato['adicionales'])
    print('nivel:',unidad)
    editunit = {"basicos":{},"adicionales":{}}
    print(editunit)
    for i in range(len(basicos)):
        editunit['basicos'].update(basicos[i])
    for i in range(len(adicionales)):
        editunit['adicionales'].update(adicionales[i])
    print ('editunit:',editunit)
    print ('unidad: ',unidad)
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"actualiza unidad proyecto","nombre":proyecto,"unidad":unidad,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    db = client[proyecto]
    col = db['relpu']
    myquery = {"basicos.unit_code":unidad}
    print ('myquery: ',myquery)
    newvalues = { "$set": editunit}
    x = col.update_one(myquery,newvalues)
    return 'OK'

def updater(data,username):
    print (data)
    print('type',type(data))
    longo = len(data)
    claves = []
    keys = data.keys()
    for key in keys:
        claves.append(key)
    print ("claves0", claves[0])
    llaves = json.loads(claves[0])
    print("llaves:",llaves)
    basicos = []
    adicionales = []
    for i in range(len(llaves)):
        dato = llaves[i]
        print('dato:',dato)
        if 'room' in dato:
            room = dato['room']
        if 'unidad' in dato:
            unidad = dato['unidad']
        if 'proyecto' in dato:
            proyecto = dato['proyecto']
        if "basicos" in dato:
            basicos.append(dato['basicos'])
        if "adicionales" in dato:
            adicionales.append(dato['adicionales'])
    print('nivel:',room)
    editroom = {"basicos":{},"adicionales":{}}
    print(editroom)
    for i in range(len(basicos)):
        editroom['basicos'].update(basicos[i])
    for i in range(len(adicionales)):
        editroom['adicionales'].update(adicionales[i])
    print ('editroom:',editroom)
    print ('room: ',room)
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"actualiza local","proyecto":proyecto,"unidad":unidad,"local":room,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    db = client[proyecto]
    col = db['relur']
    myquery = {"basicos.from":unidad,"basicos.to":room}
    print ('myquery: ',myquery)
    newvalues = { "$set": editroom}
    x = col.update_one(myquery,newvalues)
    return 'OK'

def itemcal(item,cal):
    client = get_db()
    db = client['base']
    col = db['opts']
    mydoc = col.find({"item_code":item,"calidad":cal},{"_id":0,"item_code":1,"fabricante":1,"modelo":1,"calidad":1,"coste":1,"ref_proyecto":1,"fecha":1})
    lista = []
    df = pd.DataFrame()
    i = 0
    for x in mydoc:
        df = df.append(x, ignore_index = True)
        i = i+1
        if i > 0:
            df = df.sort_values(by=['coste']).reset_index(drop=True)
            print(df)
            resultado = df.loc[0].to_dict()
            return resultado
        else:
            resultado = "sin_oferta"
        return resultado

def itemof(item):
    client = get_db()
    db = client['base']
    col = db['opts']
    mydoc = col.find({"item_code":item},{"_id":0,"item_code":1,"calidad":1,"coste":1})
    lista = []
    df = pd.DataFrame()
    i = 0
    for x in mydoc:
        df = df.append(x, ignore_index = True)
        i = i+1
        if i > 0:
            df = df.sort_values(by=['coste']).reset_index(drop=True)
            print(df)
            resultado = df.loc[0].to_dict()
            return resultado
        else:
            resultado = "sin_oferta"
        return resultado


def insertp(data,username):
    #print (data)
    #print('type',type(data))
    longo = len(data)
    claves = []
    keys = data.keys()
    for key in keys:
        claves.append(key)
    #print ("claves0", claves[0])
    llaves = json.loads(claves[0])
    #print("llaves:",llaves)
    basicos = []
    adicionales = []
    for i in range(len(llaves)):
        dato = llaves[i]
        #print('dato:',dato)
        if "basicos" in dato:
            basicos.append(dato['basicos'])
        if "adicionales" in dato:
            adicionales.append(dato['adicionales'])
    editproy = {"basicos":{},"adicionales":{}}
    #print(editproy)
    for i in range(len(basicos)):
        editproy['basicos'].update(basicos[i])
    for i in range(len(adicionales)):
        editproy['adicionales'].update(adicionales[i])
    #print ('editproy:',editproy)
    nombre = editproy['basicos']['nombre']
    objetivo = editproy['basicos']['objetivo']
    editproy['nombre'] = nombre
    #print ('proyecto: ',nombre)
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"crea proyecto","proyecto":nombre,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    lista = client.list_database_names()
    if nombre in lista:
        return 'Un proyecto con este nombre ya existe, por favor elija otro'
    db=client[nombre]
    col = db['propiedades']
    x = col.insert_one(editproy)
    db = client['base']
    cols = db.list_collection_names()
    #print ('cols:',cols)
    cols.remove('propiedades')
    #print ('cols:',cols)
    for col in cols:
        db = client['base']
        datosbase = db[col]
        myquery = {}
        doc = datosbase.find(myquery)
        for x in doc:
            db = client[nombre]
            datoscopy = db[col]
            x = datoscopy.insert_one(x)
    db = client[nombre]
    col = db['rel']
    myquery = {"proyecto": "base" }
    newvalues = { "$set": { "proyecto": nombre } }
    doc = col.find(myquery)
    for x in doc:
        col.update_one(myquery, newvalues)
    print("aqui empiezo selección automatica")
    seleccion.seleccion(nombre,objetivo)
    return 'OK'

def insertu(data,username):
    print (data)
    print('type',type(data))
    longo = len(data)
    claves = []
    keys = data.keys()
    for key in keys:
        claves.append(key)
    print ("claves0", claves[0])
    llaves = json.loads(claves[0])
    print("llaves:",llaves)
    basicos = []
    adicionales = []
    relaciones = {}
    for i in range(len(llaves)):
        dato = llaves[i]
        print('dato:',dato)
        if 'proyecto' in dato:
            proyecto = dato['proyecto']
        if "basicos" in dato:
            basicos.append(dato['basicos'])
        if "adicionales" in dato:
            adicionales.append(dato['adicionales'])
        if "relaciones" in dato:
            relaciones.update(dato["relaciones"])

    editunit = {"basicos":{},"adicionales":{}}
    print(editunit)
    for i in range(len(basicos)):
        editunit['basicos'].update(basicos[i])
    for i in range(len(adicionales)):
        editunit['adicionales'].update(adicionales[i])
    print ('editunit:',editunit)
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"inserta unidad","proyecto":proyecto,"unidad":nombre,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    db = client[proyecto]
    col = db['unidades']
    nombre = editunit['basicos']['unit_code']
    print('nombre:',nombre)
    myquery = {"unit_code":nombre}
    mydoc = col.find(myquery)
    result = []
    for x in mydoc:
        result.append(x)
    print('result:',result)
    if (len(result)) > 0:
        return "Ya existe una unidad con este código, por favor cambialo"
    x = col.insert_one(editunit)
    col = db['relpu']
    editrel1 = {"basicos":{"unit_code":nombre,"unit_es":editunit['basicos']['unit_es'],"estado":"def","nombre_cliente":""},"adicionales":{}}
    print("editrel:",editrel1)
    x = col.insert_one(editrel1)
    print ('relaciones:',relaciones)
    for key, value in relaciones.items():
        db = client['base']
        col = db['rooms']
        myquery = {"basicos.room_code":key}
        filtro = {"_id":0,"basicos.room_code":1,"basicos.room_es":1,"basicos.room_area":1}
        print('myquery:',myquery)
        mydoc = col.find(myquery,filtro)
        for x in mydoc:
            print('x:',x)
            editrel2 = {"basicos":{"from":nombre,"to":x['basicos']['room_code'],"room_es":x['basicos']['room_es'],"cantidad":value,"m2":x['basicos']['room_area'],"area":"","remarks_es":"","estado":"def","nombre_cliente":""},"adicionales":{}}
            print(editrel2)
            db = client[proyecto]
            col = db['relur']
            x = col.insert_one(editrel2)
            db = client['base']
            col = db['relur']
            x = col.insert_one(editrel2)
    db = client['base']
    col = db['unidades']
    x = col.insert_one(editunit)
    col = db['relpu']
    x = col.insert_one(editrel1)
    return 'OK'

def borra(proj,username):
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"borra proyecto","proyecto":proj,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    client.drop_database(proj)
    return 'OK'

def borraunit(proj,unit,username):
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"borra unidad","proyecto":proj,"unidad":unit,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    db = client[proj]
    col = db['rel']
    doc = mydoc = col.find({"unidad":unit})
    for x in doc:
        print("borrando",x)
        col.delete_one(x)
    return 'OK'

def borrasunit(proj,unit,sunit,username):
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"borra sub-unidad","proyecto":proj,"unidad":unit,"sub-unidad":sunit,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    db = client[proj]
    col = db['rel']
    doc = mydoc = col.find({"unidad":unit,"sunidad":sunit})
    for x in doc:
        print("borrando",x)
        col.delete_one(x)
    return 'OK'

def borraroom(proj,unit,sunit,room,username):
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"borra local","proyecto":proj,"unidad":unit,"sub-unidad":sunit,"local":room,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    db = client[proj]
    col = db['rel']
    doc = mydoc = col.find({"unidad":unit,"sunidad":sunit,"local":room})
    for x in doc:
        print("borrando",x)
        col.delete_one(x)
    return 'OK'

def borrata(proj,unit,sunit,room,ta,username):
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"borra tipo","proyecto":proj,"unidad":unit,"sub-unidad":sunit,"local":room,"tipo":ta,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    db = client[proj]
    col = db['rel']
    doc = mydoc = col.find({"unidad":unit,"sunidad":sunit,"local":room,"tipoA":ta})
    for x in doc:
        print("borrando",x)
        col.delete_one(x)
    return 'OK'

def borratb(proj,unit,sunit,room,ta,tb,username):
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"borra familia","proyecto":proj,"unidad":unit,"sub-unidad":sunit,"local":room,"tipo":ta,"familia":tb,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    db = client[proj]
    col = db['rel']
    doc = mydoc = col.find({"unidad":unit,"sunidad":sunit,"local":room,"tipoA":ta,"tipoB":tb})
    for x in doc:
        print("borrando",x)
        col.delete_one(x)
    return 'OK'

def borrai(proj,unit,sunit,room,ta,tb,item,username):
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"borra item","proyecto":proj,"unidad":unit,"sub-unidad":sunit,"local":room,"tipo":ta,"familia":tb,"item":item,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    db = client[proj]
    col = db['rel']
    doc = mydoc = col.find({"unidad":unit,"sunidad":sunit,"local":room,"tipoA":ta,"tipoB":tb,"item":item})
    for x in doc:
        print("borrando",x)
        col.delete_one(x)
    return 'OK'

def borrao(proj,unit,sunit,room,ta,tb,item,opt,username):
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"borra item","proyecto":proj,"unidad":unit,"sub-unidad":sunit,"local":room,"tipo":ta,"familia":tb,"item":item,"oferta":opt,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    print("cliente:",client)
    db = client[proj]
    print("db:",proj)
    col = db['rel']
    print("coleccion:",'rel')
    print("item:",item,"opt:",opt)
    doc = col.find({"item":item,"n_oferta":opt})
    print("doc:",doc)
    for x in doc:
        print("borrando",x)
        col.delete_one(x)
    return 'OK'

def borratotalta(proj,ta,username):
    client = get_db()
    db = client['simalga_db']
    col = db['logs']
    mydict = {"usuario":username,"accion":"borra capitulo","proyecto":proj,"tipo":ta,"timestamp":datetime.datetime.now()}
    x = col.insert_one(mydict)
    client = get_db()
    print("cliente:",client)
    db = client[proj]
    print("db:",proj)
    col = db['rel']
    print("coleccion:",'rel')
    doc = col.find({"tipoA":ta})
    print("doc:",doc)
    for x in doc:
        print("borrando",x)
        col.delete_one(x)
    return 'OK'


def newrelu(proj,unit):
    client = get_db()
    db = client['base']
    col = db['rel']
    doc = mydoc = col.find({"unidad":unit},{"_id":0})
    for x in doc:
        db = client[proj]
        col = db['rel']
        print("añadiendo",x, "a", proj)
        x['proyecto'] = proj
        y = col.insert_one(x)
    return 'OK'

def newrels(proj,unit,sunit):
    client = get_db()
    db = client['base']
    col = db['rel']
    doc = mydoc = col.find({"sunidad":sunit},{"_id":0})
    for x in doc:
        db = client[proj]
        col = db['rel']
        print("añadiendo",x, "a", proj)
        x['proyecto'] = proj
        x['unidad'] = unit
        y = col.insert_one(x)
    return 'OK'

def newrelr(proj,unit,sunit,room):
    client = get_db()
    db = client['base']
    col = db['rel']
    x = mydoc = col.find_one({"local":room},{"_id":0})
    print('doc es:',x)
    db = client[proj]
    col = db['rel']
    print("añadiendo",x, "a", proj,unit,sunit)
    x['proyecto'] = proj
    x['unidad'] = unit
    x['sunidad'] = sunit
    y = col.insert_one(x)
    return 'OK'

def newreli(proj,unit,sunit,room,ta,tb,item):
    client = get_db()
    db = client['base']
    col = db['rel']
    mydoc = col.find({"item":item},{"_id":0})
    for x in mydoc:
        db = client[proj]
        col = db['rel']
        y = mydocy = col.find_one({"proyecto":proj,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":ta,"tipoB":tb},{"_id":0})
        print("y es:",y)
        y["item"] = item
        y["item_qty"] = x["item_qty"]
        y["item_es"] = x["item_es"]
        y["fabricante"] = x["fabricante"]
        y["modelo"] = x["modelo"]
        y["coste"] = x["coste"]
        y["ref_proyecto"] = x["ref_proyecto"]
        y["fecha"] = x["fecha"]
        no_copy = []
        if y["coste"] not in no_copy:
            no_copy.append(y["coste"])
            z = col.insert_one(y)
    return 'OK'

def countitem(proj,unit,sunit,room,ta,tb,item):
    client = get_db()
    db = client[proj]
    col = db['rel']
    mydoc = col.find({"proyecto":proj,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":ta,"tipoB":tb,"item":item},{"_id":0,"estado":1,"coste":1})
    n_def = 0
    n_sin = 0
    n_cons = 0
    for x in mydoc:
        if x['coste'] == "NaN":
            n_sin = n_sin +1
        else:
            if x['estado'] == 'def':
                n_def = n_def + 1
            if x['estado'] == 'cons':
                n_cons = n_cons + 1
    return ({"n_def":n_def,"n_sin":n_sin,"n_cons":n_cons})

def counttb(proj,unit,sunit,room,ta,tb):
    client = get_db()
    db = client[proj]
    col = db['rel']
    mydoc = col.find({"proyecto":proj,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":ta,"tipoB":tb},{"_id":0,"estado":1,"coste":1})
    n_def = 0
    n_sin = 0
    n_cons = 0
    for x in mydoc:
        if x['coste'] == "NaN":
            n_sin = n_sin +1
        else:
            if x['estado'] == 'def':
                n_def = n_def + 1
            if x['estado'] == 'cons':
                n_cons = n_cons + 1
    return ({"n_def":n_def,"n_sin":n_sin,"n_cons":n_cons})

def countta(proj,unit,sunit,room,ta):
    client = get_db()
    db = client[proj]
    col = db['rel']
    mydoc = col.find({"proyecto":proj,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":ta},{"_id":0,"estado":1,"coste":1})
    n_def = 0
    n_sin = 0
    n_cons = 0
    for x in mydoc:
        if x['coste'] == "NaN":
            n_sin = n_sin +1
        else:
            if x['estado'] == 'def':
                n_def = n_def + 1
            if x['estado'] == 'cons':
                n_cons = n_cons + 1
    return ({"n_def":n_def,"n_sin":n_sin,"n_cons":n_cons})

def countp(proj):
    client = get_db()
    db = client[proj]
    col = db['rel']
    mydoc = col.find({"proyecto":proj},{"_id":0,"estado":1,"coste":1})
    n_def = 0
    n_sin = 0
    n_cons = 0
    for x in mydoc:
        if x['coste'] == "NaN":
            n_sin = n_sin +1
        else:
            if x['estado'] == 'def':
                n_def = n_def + 1
            if x['estado'] == 'cons':
                n_cons = n_cons + 1
    return ({"n_def":n_def,"n_sin":n_sin,"n_cons":n_cons})

def actualizar(proj,calidad):
    hazesto = seleccion.seleccion(proj,calidad)
    return hazesto

def solo_barato(proj,item):
    hazesto = seleccion.tiene_oferta(proj,item)
    return hazesto

def nuevo_nombreu(proj,unit,nombre):
    client = get_db()
    db = client[proj]
    col = db['rel']
    query = {"proyecto":proj,"unidad":unit}
    doc = col.find(query)
    newvalue = {"$set":{"unidad_es":nombre}}
    for x in doc:
        col.update_one(query,newvalue)
    return 'OK'

def nuevo_nombres(proj,unit,sunit,nombre):
    client = get_db()
    db = client[proj]
    col = db['rel']
    query = {"proyecto":proj,"unidad":unit,"sunidad":sunit}
    doc = col.find(query)
    newvalue = {"$set":{"sunidad_es":nombre}}
    for x in doc:
        col.update_one(query,newvalue)
    return 'OK'

def nuevo_nombrer(proj,unit,sunit,room,nombre):
    client = get_db()
    db = client[proj]
    col = db['rel']
    query = {"proyecto":proj,"unidad":unit,"sunidad":sunit,"local":room}
    doc = col.find(query)
    newvalue = {"$set":{"local_es":nombre}}
    for x in doc:
        col.update_one(query,newvalue)
    return 'OK'

def nuevo_qtyr(proj,unit,sunit,room,qty):
    client = get_db()
    db = client[proj]
    col = db['rel']
    query = {"proyecto":proj,"unidad":unit,"sunidad":sunit,"local":room}
    doc = col.find(query)
    newvalue = {"$set":{"local_qty":qty}}
    for x in doc:
        col.update_one(query,newvalue)
    return 'OK'

def nuevo_nombrei(proj,unit,sunit,room,ta,tb,item,nombre):
    client = get_db()
    db = client[proj]
    col = db['rel']
    query = {"proyecto":proj,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":ta,"tipoB":tb,"item":item}
    doc = col.find(query)
    newvalue = {"$set":{"item_es":nombre}}
    for x in doc:
        col.update_one(query,newvalue)
    return 'OK'

def nuevo_qtyi(proj,unit,sunit,room,ta,tb,item,numero):
    client = get_db()
    db = client[proj]
    col = db['rel']
    query = {"proyecto":proj,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":ta,"tipoB":tb,"item":item}
    doc = col.find(query)
    newvalue = {"$set":{"item_qty":numero}}
    for x in doc:
        col.update_one(query,newvalue)
    return 'OK'

def consolida(proj,unit,sunit,room,ta,tb,item,n_o):
    client = get_db()
    db = client[proj]
    col = db['rel']
    query = {"proyecto":proj,"unidad":unit,"sunidad":sunit,"local":room,"tipoA":ta,"tipoB":tb,"item":item,"n_oferta":n_o}
    doc = col.find(query)
    newvalue = {"$set":{"estado":"cons"}}
    for x in doc:
        col.update_one(query,newvalue)
    return 'OK'

def sin_oferta(proj):
    client = get_db()
    db = client[proj]
    col = db['rel']
    doc = col.find({"proyecto":proj,"estado":"sin"},{"_id":0})
    excel = pd.DataFrame()
    itemxls = pd.DataFrame()
    items = []
    for x in doc:
        excel = excel.append(x, ignore_index = True)
        if x['item'] not in items:
            items.append(x["item"])
    items.sort()
    print("items:",items)
    for item in items:
        doc = col.find({"proyecto":proj,"estado":"sin","item":item},{"_id":0})
        for x in doc:
            itemxls = itemxls.append(x, ignore_index = True)
    writer = pd.ExcelWriter('despl/csv/'+proj+'_sin_ofertas.xlsx', engine='xlsxwriter')
    frames = {'sin_oferta': excel, 'Abc': itemxls}
    excel.to_excel(writer, sheet_name ='sin_ofertas', index=False)
    itemxls.to_excel(writer, sheet_name ='Abc', index=False)
    writer.save()
    return 'OK'

def en_excel(proj):
    client = get_db()
    db = client[proj]
    col = db['rel']
    doc = col.find({"proyecto":proj,"estado":{"$in":["def","cons"]}},{"_id":0})
    excel = pd.DataFrame()
    itemxls = pd.DataFrame()
    items = []
    for x in doc:
        excel = excel.append(x, ignore_index = True)
        if x['item'] not in items:
            items.append(x["item"])
    items.sort()
    print("items:",items)
    for item in items:
        doc = col.find({"proyecto":proj,"estado":{"$in":["def","cons"]},"item":item},{"_id":0})
        for x in doc:
            itemxls = itemxls.append(x, ignore_index = True)
    writer = pd.ExcelWriter('despl/csv/'+proj+'_en_excel.xlsx', engine='xlsxwriter')
    frames = {'sin_oferta': excel, 'Abc': itemxls}
    excel.to_excel(writer, sheet_name ='plan equipamiento', index=False)
    itemxls.to_excel(writer, sheet_name ='Abc', index=False)
    writer.save()
    return 'OK'


