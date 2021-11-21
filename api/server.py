from logging import log
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import json

from werkzeug.wrappers import Request

app = Flask(__name__) #Creamos el servidor con Flask
CORS(app) #Permitimos la política CORS
api = Api(app) #Le damos el caracter de API

data="" #Almacena las vista del sitio web (fichas técnicas)
consulta="" #El string de la consulta del usuario
orden="" #int {0: Relevancia, 1: Autor , 2:Fecha}

class HelloWorld(Resource):
    def get(self):
        return data #Exponemos el archivo con las fichas técnicas

api.add_resource(HelloWorld, '/')


@app.route('/consulta', methods=["POST"])
def obtener_consulta():
    datos= request.get_json(force=True, cache=True) #Obtenemos el JSON que envía el FrontEnd
    print("DATOS: ",datos) #Imprime lo que se recibe
    return 



def abrirJSON():
    with open('data.json') as file:
        data=json.load(file)
    return data

if __name__ == '__main__':
    data= abrirJSON()
    app.run(host="192.168.100.2", port=5000, debug=True)