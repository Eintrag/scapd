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
from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient

connection = pymongo.MongoClient('ds147821.mlab.com', 47821)
db = connection['scapd']
db.authenticate('admin', '8hMzYgP5b2tDQoesP0Ge')

#post = {"nombre": "Tomates", "precio": "2.4", "comprador": "Sergio"}
#db.compras.insert_one(post).inserted_id

app = Flask(__name__)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

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

@app.route('/compras')
def GetCompras():
    return QueryCompras("")

@app.route('/compras/comprador/<comprador>')
def GetComprasParaComprador(comprador):
    return QueryCompras({"comprador": comprador})
	
@app.route('/compras/nombre/<nombre>')
def GetComprasParaNombre(nombre):
    return QueryCompras({"nombre": nombre})

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
	#app.run(host='127.0.0.1', port=int(port))