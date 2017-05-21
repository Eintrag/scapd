# -*- coding: utf-8 -*-

# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify, url_for, render_template
from flask import request
import pymongo
from pymongo import MongoClient

connection = pymongo.MongoClient('ds147821.mlab.com', 47821)
db = connection['scapd']
db.authenticate('admin', '8hMzYgP5b2tDQoesP0Ge')

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/index')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/compras/consultadas')
def formarQuery():
	nombre = request.form['nombre']
	precio = request.form['precio']
	comprador = request.form['comprador']
	query = {"nombre": nombre, "precio": precio, "comprador": comprador}
	return QueryCompras(query)
	
def QueryCompras(query):
	lista = []
	compra = []
	for entrada in db.compras.find(query):
		compra.append(entrada['nombre'])
		compra.append(entrada['precio'])
		compra.append(entrada['comprador'])
		lista.append(compra)
		compra = []
	return jsonify(results=lista)

@app.route("/compras/consultar")
def consultarCompras():
    return render_template("consultarCompras.html")	
	
@app.route("/compras/add")
def addCompras():
    return render_template("addCompras.html")
 
@app.route("/compras/incluida", methods=['POST'])
def compraIncluida():
	nombre = request.form['nombre']
	precio = request.form['precio']
	comprador = request.form['comprador']
	post = {"nombre": nombre, "precio": precio, "comprador": comprador}
	db.compras.insert_one(post).inserted_id
	return 'Añadida la compra: {} por {}€ de {} <br><br> <a href="/index">Volver al indice</a>'.format(nombre, precio, comprador)
 	
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	#app.run(host='0.0.0.0', port=int(port))
	app.run(host='127.0.0.1', port=int(port))