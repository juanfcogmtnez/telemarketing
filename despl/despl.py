from flask import Flask, render_template, jsonify, url_for, send_file, Blueprint, redirect, session, request, send_from_directory
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
import pandas as pd
import despl.read as read
import despl.texto as texto
import json
import os
import datetime


despl = Blueprint('despl', __name__ ,template_folder='templates',static_folder='static')


@despl.route('/upload', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('index'))
    
@despl.route('/')
def index():
	try:
		username = session["nombre"]
		role = session["role"]
		print(username)
		return render_template('despl_index.html',username=username,role=role)
	except:
		return redirect(url_for('login'))

@despl.route('/getproy')
def getproy():
	get = read.get()
	return jsonify(get)

@despl.route('/getproj/<proy>')
def getproyp(proy):
	get = read.getproyp(proy)
	return jsonify(get)

@despl.route('/getproj/<proy>/<unit>')
def getproyu(proy,unit):
	get = read.getproyu(proy,unit)
	return jsonify(get)

@despl.route('/getproj/<proy>/<unit>/<subunit>')
def getproysu(proy,unit,subunit):
	get = read.getproysu(proy,unit,subunit)
	return jsonify(get)

@despl.route('/getproj/<proy>/<unit>/<sunit>/<room>')
def getproyr(proy,unit,sunit,room):
	get = read.getproyr(proy,unit,sunit,room)
	return jsonify(get)
@despl.route('/getproj/<proy>/<unit>/<sunit>/<room>/<item>')
def getproyi(proy,unit,sunit,room,item):
	get = read.getproyi(proy,unit,sunit,room,item)
	return jsonify(get)

@despl.route('/getunits/<proy>')
def getunits(proy):
	get = read.units(proy)
	return jsonify(get)

@despl.route('/getsunit/<proy>/<unit>')
def getsunits(proy,unit):
	get = read.sunits(proy,unit)
	return jsonify(get)


@despl.route('/getrooms/<proy>/<unit>/<sunit>')
def getrooms(proy,unit,sunit):

	get = read.rooms(proy,unit,sunit)
	return jsonify(get)

@despl.route('/getitems/<proy>/<unit>/<sunit>/<room>/<typeA>/<typeB>')
def getitems(proy,unit,sunit,room,typeA,typeB):
	get = read.items(proy,unit,sunit,room,typeA,typeB)
	return jsonify(get)

@despl.route('/gettypes/<proy>/<unit>/<sunit>/<room>')
def gettypes(proy,unit,sunit,room):
	get = read.types(proy,unit,sunit,room)
	return jsonify(get)

@despl.route('/gettypesb/<proy>/<unit>/<sunit>/<room>/<typeA>')
def gettypesb(proy,unit,sunit,room,typeA):
	get = read.typesb(proy,unit,sunit,room,typeA)
	return jsonify(get)

@despl.route('/getopts/<proy>/<unit>/<sunit>/<room>/<typeA>/<typeB>/<item>')
def getopts(proy,unit,sunit,room,typeA,typeB,item):
	get = read.opts(proy,unit,sunit,room,typeA,typeB,item)
	return jsonify(get)

@despl.route('/getcoreunit/<proy>')
def getcoreunit(proy):
	get = read.coreunit(proy)
	return jsonify(get)

@despl.route('/getcoreroom/<proy>/<unit>')
def getcoreroom(proy,unit):
	get = read.coreroom(proy,unit)
	return jsonify(get)

@despl.route('/getallunits')
def getallunits():
	get = read.allunits()
	return jsonify(get)

@despl.route('/getallsunits')
def getallsunits():
	get = read.allsunits()
	return jsonify(get)

@despl.route('/getallrooms')
def getallroom():
	get = read.allroom()
	return jsonify(get)

@despl.route('/getallta')
def getallta():
	get = read.allta()
	return jsonify(get)

@despl.route('/getallitems/<ta>/<tb>')
def getallitems(ta,tb):
	get = read.allitems(ta,tb)
	return jsonify(get)

@despl.route('/ver/<proy>')
def verp(proy):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_verp.html',username=username,proy=proy)
	except:
		return redirect(url_for('login'))

@despl.route('/crea/<proy>')
def creap(proy):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_creap.html',username=username)
	except:
		return redirect(url_for('login'))

@despl.route('/crea/u/<proy>')
def creau(proy):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_creau.html',username=username,proy=proy)
	except:
		return redirect(url_for('login'))

@despl.route('/crearel/<proy>')
def crearelu(proy):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_crearelu.html',username=username,proy=proy)
	except:
		return redirect(url_for('login'))

@despl.route('/crearel/<proy>/<unit>')
def crearels(proy,unit):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_crearels.html',username=username,proy=proy,unit=unit)
	except:
		return redirect(url_for('login'))

@despl.route('/crearel/<proy>/<unit>/<sunit>')
def crearelr(proy,unit,sunit):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_crearelr.html',username=username,proy=proy,unit=unit,sunit=sunit)
	except:
		return redirect(url_for('login'))

@despl.route('/crearel/<proy>/<unit>/<sunit>/<room>')
def crearelta(proy,unit,sunit,room):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_crearelta.html',username=username,proy=proy,unit=unit,sunit=sunit,room=room)
	except:
		return redirect(url_for('login'))

@despl.route('/crearel/<proy>/<unit>/<sunit>/<room>/<ta>/<tb>')
def creareli(proy,unit,sunit,room,ta,tb):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_creareli.html',username=username,proy=proy,unit=unit,sunit=sunit,room=room,ta=ta,tb=tb)
	except:
		return redirect(url_for('login'))

@despl.route('/crearel/<proy>/<unit>/<sunit>/<room>/<ta>/<tb>/<item>')
def crearelo(proy,unit,sunit,room,ta,tb,item):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_crearelo.html',username=username,proy=proy,unit=unit,sunit=sunit,room=room,ta=ta,tb=tb,item=item)
	except:
		return redirect(url_for('login'))


@despl.route('/crea/r/<proy>/<unit>')
def crear(proy,unit):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_crear.html',username=username,proy=proy,unit=unit)
	except:
		return redirect(url_for('login'))

@despl.route('/ver/<proy>/<unit>')
def veru(proy,unit):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_veru.html',username=username,proy=proy,unit=unit)
	except:
		return redirect(url_for('login'))
		
@despl.route('/ver/<proy>/<unit>/<sunit>')
def vers(proy,unit,sunit):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_vers.html',username=username,proy=proy,unit=unit,sunit=sunit)
	except:
		return redirect(url_for('login'))

@despl.route('/ver/<proy>/<unit>/<sunit>/<room>')
def verr(proy,unit,sunit,room):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_verr.html',username=username,proy=proy,unit=unit,sunit=sunit,room=room)
	except:
		return redirect(url_for('login'))

@despl.route('/ver/<proy>/<unit>/<sunit>/<room>/<item>')
def veri(proy,unit,sunit,room,item):
	try:
		username = session["nombre"]
		print(username)
		return render_template('despl_veri.html',username=username,proy=proy,unit=unit,sunit=sunit,room=room,item=item)
	except:
		return redirect(url_for('login'))

@despl.route('/ver/<proy>/<unit>/<sunit>/<room>/<item>/<int:n_offer>')
def verof(proy,unit,sunit,room,item,n_offer):
	username = session["nombre"]
	print(username)
	path = os.path.abspath(os.getcwd())
	print("ruta actual",path)
	filepath = path+'/despl/ofertas/'+item+'/'
	#return filepath+item+'_'+str(n_offer)+'.pdf'
	return send_from_directory(filepath,item+'_'+str(n_offer)+'.pdf')

@despl.route('/updatep', methods=["POST"])
def updatep():
	if request.method == 'POST':
		username = session["nombre"]
		imd = request.values
		data = imd.to_dict(flat=False)
		set = read.updatep(data,username)
		return set

@despl.route('/updateu', methods=["POST"])
def updateu():
	if request.method == 'POST':
		username = session["nombre"]
		imd = request.values
		data = imd.to_dict(flat=False)
		set = read.updateu(data,username)
		return set

@despl.route('/updater', methods=["POST"])
def updater():
	if request.method == 'POST':
		username = session["nombre"]
		imd = request.values
		data = imd.to_dict(flat=False)
		set = read.updater(data,username)
		return set

@despl.route('/readprops/<proj>', methods=["GET"])
def readprops(proj):
	objetivo = read.objetivo(proj)
	return objetivo


@despl.route('/insertp', methods=["POST"])
def insertp():
	if request.method == 'POST':
		username = session["nombre"]
		imd = request.values
		data = imd.to_dict(flat=False)
		set = read.insertp(data,username)
		return set

@despl.route('/insertu', methods=["POST"])
def insertu():
	if request.method == 'POST':
		username = session["nombre"]
		imd = request.values
		data = imd.to_dict(flat=False)
		set = read.insertp(data,username)
		return set

@despl.route('/del/<proj>', methods=["GET"])
def borra(proj):
	username = session["nombre"]
	borra = read.borra(proj,username)
	return (borra)

@despl.route('/del/<proj>/<unit>', methods=["GET"])
def borraunit(proj,unit):
	username = session["nombre"]
	borra = read.borraunit(proj,unit,username)
	return (borra)

@despl.route('/del/<proj>/<unit>/<sunit>', methods=["GET"])
def borrasunit(proj,unit,sunit):
	username = session["nombre"]
	borra = read.borrasunit(proj,unit,sunit,username)
	return (borra)

@despl.route('/del/<proj>/<unit>/<sunit>/<room>', methods=["GET"])
def borraroom(proj,unit,sunit,room):
	username = session["nombre"]
	borra = read.borraroom(proj,unit,sunit,room,username)
	return (borra)
@despl.route('/del/<proj>/<unit>/<sunit>/<room>/<ta>', methods=["GET"])
def borrata(proj,unit,sunit,room,ta):
	username = session["nombre"]
	borra = read.borrata(proj,unit,sunit,room,ta,username)
	return (borra)
@despl.route('/del/<proj>/<unit>/<sunit>/<room>/<ta>/<tb>', methods=["GET"])
def borratb(proj,unit,sunit,room,ta,tb):
	username = session["nombre"]
	borra = read.borratb(proj,unit,sunit,room,ta,tb,username)
	return (borra)
@despl.route('/del/<proj>/<unit>/<sunit>/<room>/<ta>/<tb>/<item>', methods=["GET"])
def borrai(proj,unit,sunit,room,ta,tb,item):
	username = session["nombre"]
	borra = read.borrai(proj,unit,sunit,room,ta,tb,item,username)
	return (borra)

@despl.route('/del/<proj>/<unit>/<sunit>/<room>/<ta>/<tb>/<item>/<opt>', methods=["GET"])
def borrao(proj,unit,sunit,room,ta,tb,item,opt):
	username = session["nombre"]
	borra = read.borrao(proj,unit,sunit,room,ta,tb,item,opt,username)
	return (borra)

@despl.route('/deltotal/<proj>/<ta>', methods=["GET"])
def borratotalta(proj,ta):
	username = session["nombre"]
	borra = read.borratotalta(proj,ta,username)
	return (borra)

@despl.route('/newrel/<proj>/<unit>', methods=["GET"])
def newrelu(proj,unit):
	haz = read.newrelu(proj,unit)
	return (haz)

@despl.route('/newrel/<proj>/<unit>/<sunit>', methods=["GET"])
def newrels(proj,unit,sunit):
	haz = read.newrels(proj,unit,sunit)
	return (haz)

@despl.route('/newrel/<proj>/<unit>/<sunit>/<room>', methods=["GET"])
def newrelr(proj,unit,sunit,room):
	haz = read.newrelr(proj,unit,sunit,room)
	return (haz)

@despl.route('/newrel/<proj>/<unit>/<sunit>/<room>/<ta>/<tb>/<item>', methods=["GET"])
def newreli(proj,unit,sunit,room,ta,tb,item):
	haz = read.newreli(proj,unit,sunit,room,ta,tb,item)
	return (haz)

@despl.route('/count/<proj>/<unit>/<sunit>/<room>/<ta>/<tb>/<item>', methods=['GET'])
def countitem(proj,unit,sunit,room,ta,tb,item):
	cuenta = read.countitem(proj,unit,sunit,room,ta,tb,item)
	return cuenta

@despl.route('/count/<proj>/<unit>/<sunit>/<room>/<ta>/<tb>', methods=['GET'])
def counttb(proj,unit,sunit,room,ta,tb):
	cuenta = read.counttb(proj,unit,sunit,room,ta,tb)
	return cuenta

@despl.route('/count/<proj>/<unit>/<sunit>/<room>/<ta>', methods=['GET'])
def countta(proj,unit,sunit,room,ta):
	cuenta = read.countta(proj,unit,sunit,room,ta)
	return cuenta

@despl.route('/count/<proj>', methods=['GET'])
def countp(proj):
	cuenta = read.countp(proj)
	return cuenta

@despl.route('/actualizar/<proj>/<calidad>', methods=['GET'])
def actualizar(proj,calidad):
	hazesto = read.actualizar(proj,calidad)
	return hazesto

@despl.route('/check_offer/<item>', methods=['GET'])
def tiene_oferta(item):
	hazesto = read.solo_barato('base',item)
	return hazesto

@despl.route('/newname/<proj>/<unit>/<name>', methods=['GET'])
def newnameu(proj,unit,name):
	hazesto = read.nuevo_nombreu(proj,unit,name)
	return hazesto


@despl.route('/newname/<proj>/<unit>/<sunit>/<name>', methods=['GET'])
def newnames(proj,unit,sunit,name):
	hazesto = read.nuevo_nombres(proj,unit,sunit,name)
	return hazesto

@despl.route('/newname/<proj>/<unit>/<sunit>/<room>/<name>', methods=['GET'])
def newnamer(proj,unit,sunit,room,name):
	hazesto = read.nuevo_nombrer(proj,unit,sunit,room,name)
	return hazesto

@despl.route('/reqty/<proj>/<unit>/<sunit>/<room>/<int:qty>', methods=['GET'])
def newqtyr(proj,unit,sunit,room,qty):
	hazesto = read.nuevo_qtyr(proj,unit,sunit,room,qty)
	return hazesto

@despl.route('/newname/<proj>/<unit>/<sunit>/<room>/<ta>/<tb>/<item>/<name>', methods=['GET'])
def newnamei(proj,unit,sunit,room,ta,tb,item,name):
	hazesto = read.nuevo_nombrei(proj,unit,sunit,room,ta,tb,item,name)
	return hazesto

@despl.route('/reqty/<proj>/<unit>/<sunit>/<room>/<ta>/<tb>/<item>/<int:qty>', methods=['GET'])
def newqtyi(proj,unit,sunit,room,ta,tb,item,qty):
	hazesto = read.nuevo_qtyi(proj,unit,sunit,room,ta,tb,item,qty)
	return hazesto

@despl.route('consolida/<proj>/<unit>/<sunit>/<room>/<ta>/<tb>/<item>/<int:n_oferta>', methods=['GET'])
def consolida(proj,unit,sunit,room,ta,tb,item,n_oferta):
	hazesto = read.consolida(proj,unit,sunit,room,ta,tb,item,n_oferta)
	return hazesto

@despl.route('sin_oferta/<proj>', methods=['GET'])
def sin_oferta(proj):
	hazesto = read.sin_oferta(proj)
	print("hazesto:",hazesto)
	if hazesto == 'OK':
		username = session["nombre"]
		print(username)
		path = os.path.abspath(os.getcwd())
		print("ruta actual",path)
		filepath = path+"/despl/csv/"
		file = proj+'_sin_ofertas.xlsx'
		print(filepath,file)
		return send_from_directory(filepath,file)

@despl.route('en_excel/<proj>', methods=['GET'])
def en_excel(proj):
	hazesto = read.en_excel(proj)
	print("hazesto:",hazesto)
	if hazesto == 'OK':
		username = session["nombre"]
		print(username)
		path = os.path.abspath(os.getcwd())
		print("ruta actual",path)
		filepath = path+"/despl/csv/"
		file = proj+'_en_excel.xlsx'
		print(filepath,file)
		return send_from_directory(filepath,file)

@despl.route('en_word/<proj>', methods=['GET'])
def en_texto(proj):
	hazesto = texto.texto(proj)
	if hazesto == 'OK':
		username = session["nombre"]
		print(username)
		path = os.path.abspath(os.getcwd())
		print("ruta actual",path)
		filepath = path+"/despl/csv/"
		file = proj+'_en_word.docx'
		print(filepath,file)
		return send_from_directory(filepath,file)

