from docxtpl import DocxTemplate
import pandas as pd
import pymongo
import json
# importing the required libraries
from pymongo import MongoClient

#basico para operaciones de conexion
def get_db():
    client = MongoClient('mongodb://%s:%s@test_mongodb:27017' % ('root', 'pass'))
    db = client["simalga_db"]
    return client

def get_room(proyecto,room):
    client = get_db()
    db = client['medipole']
    col = db['rooms']
    myquery = {"basicos.room_code":room}
    filter = {"_id":0,"basicos.room_es":1,"basicos.room_hours_operation":1,"basicos.acoustics_es":1,"basicos.description_es":1}
    doc = col.find_one(myquery,filter)
    return doc

     

def texto(proyecto):
    client = get_db()
    db = client[proyecto]
    col = db['rel']
    myquery = {"proyecto":'medipole',"estado":{"$in":["def","cons"]}}
    mydoc = col.find(myquery)
    for x in mydoc:
        print(x)
        proyecto = x['proyecto']
    myquery = {"proyecto":proyecto,"estado":{"$in":["def","cons"]}}
    mydoc = col.find(myquery)
    dict = {"proyecto":"medipole","unidades":{}}
    unidades = []
    for x in mydoc:
        if x['unidad_es'] not in unidades:
            unidades.append(x['unidad_es'])
    print(unidades)
    context = {"proyecto":proyecto,"unidades":{}}
    for unidad in unidades:
        context['unidades'][unidad] = {"nombre":unidad,"sunidades":{}}
        sunidades = []
        myquery = {"proyecto":proyecto,"unidad_es":unidad,"estado":{"$in":["def","cons"]}}
        doc = col.find(myquery)
        #print(context)
        for z in doc:
            if z['sunidad_es'] not in sunidades:
                sunidades.append(z['sunidad_es'])
        for sunidad in sunidades:
            context['unidades'][unidad]['sunidades'][sunidad] = {"nombre":sunidad,"locales":{}}
            locales = []
            myquery = {"proyecto":proyecto,"unidad_es":unidad,"sunidad_es":sunidad,"estado":{"$in":["def","cons"]}}
            doc = col.find(myquery)
            #print(context)
            for y in doc:
                if y['local'] not in locales:
                    locales.append(y['local'])
            for local in locales:
                context['unidades'][unidad]['sunidades'][sunidad]['locales'][local] = {"componentes":{},"caracteristicas":{}}
                print("local:",local)
                a = get_room(proyecto,local)
                print ("get_room",a)
                context['unidades'][unidad]['sunidades'][sunidad]['locales'][local]['caracteristicas'] = {"nombre":a['basicos']['room_es'],"acustica":a['basicos']['acoustics_es'],"descripcion":a['basicos']['description_es']}
                tipos = []
                col = db['rel']
                myquery = {"proyecto":proyecto,"unidad_es":unidad,"sunidad_es":sunidad,"local":local,"estado":{"$in":["def","cons"]}}
                doc = col.find(myquery)
                for v in doc:
                    if v['tipoA'] == 'FA':
                        resultado = 'Estructural'
                    if v['tipoA'] == 'FFE':
                        resultado = 'Equipamiento'
                    if v['tipoA'] == 'SE':
                        resultado = 'Instalaciones'
                    if resultado not in tipos:
                        tipos.append(resultado)
                print("tipos a:",tipos)
                for tipo in tipos:
                    context['unidades'][unidad]['sunidades'][sunidad]['locales'][local]['componentes'][tipo] = {"nombre":tipo}
                    if tipo =='Estructural':
                        resultado = 'FA'
                    if tipo == 'Equipamiento':
                        resultado =  'FFE'
                    if tipo == 'Instalaciones':
                        resultado = 'SE'
                    myquery = {"proyecto":proyecto,"unidad_es":unidad,"sunidad_es":sunidad,"local":local,"tipoA":resultado,"estado":{"$in":["def","cons"]}}
                    doc = col.find(myquery)
                    familias = []
                    for t in doc:
                        if t['tipoB'] == "CL":
                            titulo = "Techos y cornisas"
                        if t['tipoB'] == "DW":
                            titulo = "Puertas, ventanas y accesorios"
                        if t['tipoB'] == "EL":
                            titulo = "Servicios eléctricos"
                        if t['tipoB'] == "FI":
                            titulo = "Enseres y acesorios"
                        if t['tipoB'] == "FL":
                            titulo = "Suelos, acabados y zócalos"
                        if t['tipoB'] == "FQ":
                            titulo = "Mobiliario y equipamiento no médico"
                        if t['tipoB'] == "HY":
                            titulo = "Servicios hidraúlicos"
                        if t['tipoB'] == "IT":
                            titulo = "Servicios informáticos y telecomunicaciones"
                        if t['tipoB'] == "LI":
                            titulo = "Alumbrado"
                        if t['tipoB'] == "ME":
                            titulo = "Servicios mecánicos"
                        if t['tipoB'] == "MG":
                            titulo = "Sistemas de gases medicinales"
                        if t['tipoB'] == "MM":
                            titulo = "Equipamiento médico y laboratorio"
                        if t['tipoB'] == "WL":
                            titulo = "Paredes y acabados"
                        if titulo not in familias:
                            familias.append(titulo)
                    for familia in familias:
                        if familia == "Techos y cornisas":
                            valor = 'CL'
                        if familia == "Puertas, ventanas y accesorios":
                            valor = "DW"
                        if familia == "Servicios eléctricos":
                            valor = "FI"
                        if familia == "Enseres y acesorios":
                            valor = "FL"
                        if familia == "Suelos, acabados y zócalos":
                            valor = "FQ"
                        if familia == "Mobiliario y equipamiento no médico":
                            valor = "FQ"
                        if familia == "Servicios hidraúlicos":
                            valor = "HY"
                        if familia == "Servicios informáticos y telecomunicaciones":
                            valor = "IT"
                        if familia  == "Alumbrado":
                            valor = "LI"
                        if familia == "Servicios mecánicos":
                            valor = "ME"
                        if familia  == "Sistemas de gases medicinales":
                            valor = "MG"
                        if familia  == "Equipamiento médico y laboratorio":
                            valor = "MM"
                        if familia  == "Paredes y acabados":
                            valor = "WL"
                        context['unidades'][unidad]['sunidades'][sunidad]['locales'][local]['componentes'][tipo][familia] = {"nombre":familia,"items":{}}
                        myquery = {"proyecto":proyecto,"unidad_es":unidad,"sunidad_es":sunidad,"local":local,"tipoA":resultado,"tipoB":valor,"estado":{"$in":["def","cons"]}}
                        doc = col.find(myquery)
                        items = []
                        for s in doc:
                            if s['item'] not in items:
                                items.append(s['item'])
                        for item in items:
                            context['unidades'][unidad]['sunidades'][sunidad]['locales'][local]['componentes'][tipo][familia]['items'][item] = {}
                            myquery = {"proyecto":proyecto,"unidad_es":unidad,"sunidad_es":sunidad,"local":local,"tipoA":resultado,"tipoB":valor,"item":item,"estado":{"$in":["def","cons"]}}
                            doc = col.find(myquery)
                            for o in doc:
                                context['unidades'][unidad]['sunidades'][sunidad]['locales'][local]['componentes'][tipo][familia]['items'][item] = {"item_es":o['item_es'],"fabricante":o['fabricante'],"modelo":o['modelo'],"cantidad":o['item_qty']}   
    with open("sample.json", "w") as outfile:
        json.dump(context, outfile)

    doc = DocxTemplate("despl/csv/your_template.docx")
    doc.render(context)
    doc.save("despl/csv/"+proyecto+"_en_word.docx")
    return 'OK'