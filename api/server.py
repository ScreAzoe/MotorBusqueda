from logging import log
from operator import methodcaller
from flask import Flask, request, jsonify
from flask.helpers import make_response
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from motor import motor


import json

from werkzeug.wrappers import Request


app = Flask(__name__) #Creamos el servidor con Flask
CORS(app, resources={r"/":{"origins":"*"}}) #Permitimos la política CORS
app.config['CORS_HEADERS']= 'Content-type'

consulta=""
data="" #Almacena las vista del sitio web (fichas técnicas)
orden="" #int {0: Relevancia, 1: Autor , 2:Fecha}


@app.route("/consulta", methods=["POST"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def consultar():
    datos= request.get_json(force=True, cache=True) #Obtenemos el JSON que envía el FrontEnd
    global consulta
    consulta= datos["consulta"]
    print(consulta)
    headers = {'Content-Type': 'text/plain'}
    return make_response("Consulta hecha", 200, headers)

@app.route("/resultados", methods=["GET"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def algoritmo():
    data= abrirJSON()
    return motor(consulta, data)




'''
class Consulta(Resource):
    def post(self):
        datos= request.get_json(force=True, cache=True) #Obtenemos el JSON que envía el FrontEnd
        consulta= datos["consulta"]
        print(consulta)
        headers = {'Content-Type': 'text/plain'}
        return make_response("Consulta hecha", 200, headers)
'''
#api.add_resource(Consulta, '/consulta')
    



def abrirJSON():
    with open('articulos.json') as file:
        data=json.load(file)
    return data

if __name__ == '__main__':
    data= abrirJSON()
    app.run(host="192.168.100.2", port=5000, debug=True)