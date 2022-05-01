from flask import Flask, render_template, jsonify, url_for, send_file, Blueprint, redirect, session, request
from werkzeug.datastructures import ImmutableMultiDict
import base.read as read
import json

base = Blueprint('base', __name__ ,template_folder='templates',static_folder='static')

@base.route('/')
def index():
	try:
		username = session["nombre"]
		return render_template('base_index.html',username=username, centro='Centros sanitarios')
	except:
		return redirect(url_for('login'))

@base.route('/proj/<proj>',methods=['GET'])
def proj(proj):
	try:
		username = session["nombre"]
		return render_template('base_proyecto.html',username=username,proj=proj,centro=proj)
	except:
		return redirect(url_for('login'))

@base.route('/nav/<proj>/<unidad>',methods=['GET'])
def unit(proj,unidad):
	try:
		username = session["nombre"]
		return render_template('base_unidad.html',username=username,proj=proj,centro=proj,unidad=unidad)
	except:
		return redirect(url_for('login'))

#VENTANAS crud crear
@base.route('/crear/<text>',methods=['GET'])
@base.route('/crear/<proj>/<text>',methods=['GET'])
def ventanas(text,proj=None):
	try:
		username = session["nombre"]
		if text == "proyecto":
			return render_template('base_crear.html',crear=text, username=username)
		if text == "unidad":
			return render_template('base_crearunidad.html',crear=text,proj=proj,username=username)
	except:
		return redirect(url_for('login'))

#VENTANAS crud update
@base.route('/edit/<text>/<proy>',methods=['GET'])
@base.route('/edit/<text>/<proy>/<unidad>',methods=['GET'])
def vent_edit(text,proy,unidad=None):
	try:
		print('unidad:',unidad)
		username = session["nombre"]
		if text == "proyecto":
			return render_template('base_edit.html',item='proyecto',proy=proy, username=username)
		if text == "unidad":
			return render_template('base_editunidad.html',item='unidad',proy=proy, unidad=unidad, username=username)
	except:
		return redirect(url_for('login'))

#peticiones ajax GET
@base.route('/getcol')
def getcol():
	resultado = read.col()
	return jsonify(resultado)

#peticiones ajax GET
@base.route('/getcol/<proj>', methods=["GET","POST"])
def getcolpro(proj):
	resultado = read.unit(proj)
	return jsonify(resultado)


@base.route('/getpro/<proy>')
@base.route('/getpro/<proy>/<unidad>')
def getpro(proy,unidad=None):
	resultado = read.all(proy,unidad=None)
	return jsonify(resultado)

#peticiones ajax PUT
@base.route('/upestado', methods=["POST"])
def up_estado():
	if request.method == 'POST':
		id = request.form['id'];
		estado = request.form['estado']
		set = read.set_estado(id,estado)
		return set

@base.route('/upunit', methods=["POST"])
def up_unit():
	if request.method == 'POST':
		proj = request.form['proj'];
		unit = request.form['unit']
		estado = request.form['estado']
		print('form:',proj,unit,estado)
		set = read.set_estadoin(proj,unit,estado)
		return 'ok'
#peticiones ajax POST
@base.route('/insert', methods=["POST"])
def insert():
	if request.method == 'POST':
		imd = request.values
		data = imd.to_dict(flat=False)
		set = read.insert(data)
		return set
