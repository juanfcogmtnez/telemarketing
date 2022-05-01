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
warnings.filterwarnings('ignore')

def get_db():
    client = MongoClient('mongodb://%s:%s@mongo_visioncrm:27017' % ('root', 'pass'))
    db = client["vision_db"]
    return db

def create_first():
	db = get_db()
	col = db.list_collection_names()
	if "users" in col:
		return 'OK'
	else:
		col = db["users"]
		pass_hasheada = generate_password_hash('Jfgm_4778')
		mydict = { "name": "Juan", "email": "juanfcogmtnez@gmail.com", "pwd":pass_hasheada, "role":"Admin" }
		x = col.insert_one(mydict)
		return 'OK'

def checkpwd(email,texto):
	db = get_db()
	mycol = db["users"]
	x = mycol.find_one({'email':email})
	print(x)
	keep = x['pwd']
	if check_password_hash(keep,texto):
		return (x['role'],x['name'])
	else:
		return("Error")
def uppwd(email,p1,p2):
	if p1 != p2:
		return "Las contraseñas no coinciden"
	else:
		with open('static/json/u.json') as f:
			data = json.load(f)
			for x in data:
				if email == data[x]['email']:
					a_file = open('static/json/u.json', "w")
					pass_hasheada = generate_password_hash(p1)
					data[x]['password'] = pass_hasheada
					json.dump(data, a_file)
					a_file.close()
					if check_password_hash(pass_hasheada,p1):
						return("La contraseña se ha actualizado con éxito")
					else:
						return("Error")
				else:
					return("no coincide")

def registro(nombre,email,role,p1,p2):
	if p1 != p2:
		return "Las contraseñas no coinciden"
	else:
		newpass = generate_password_hash(p1)
		db = get_db()
		mycol = db["users"]
		filter = { 'email': email }
		mydoc = mycol.find(filter)
		lista = []
		for x in mydoc:
			lista.append(x)
		if lista != []:
			return "Un usuario con ese email ya existe"
		newrecord = {"name":nombre,"email":email,"role":role,"pwd":newpass}
		rec = mycol.insert_one(newrecord)
		return "Usuario creado, serás redirigido en cinco segundos"

def uppwd(email,p1,p2):
    if p1 != p2:
        return "Las contraseñas no coinciden"
    else:
        db = get_db()
        mycol = db["users"]
        count = mycol.find( {'email': email } )
        count = len(list(count))
        print('count:',count,type(count))
        if count > 0:
            pass_hasheada = generate_password_hash(p1)
            print ('newpass:',pass_hasheada)
            myquery = {'email':email}
            print('myquery:',myquery)
            newvalues = { "$set": { "pwd": pass_hasheada } }
            mycol.update_one(myquery, newvalues)
            if check_password_hash(pass_hasheada,p1):
                return("La contraseña se ha actualizado con éxito")
            else:
                return("Error")
        else:
            print('no es mayor que 0')
            return("no existe un usuario con este email")
