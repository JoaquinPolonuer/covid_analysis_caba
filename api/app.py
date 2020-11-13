from flask import Flask,jsonify,request
from flask_restful import Api,Resource
import pandas as pd

from data import Data

app = Flask(__name__)
api = Api(app)

dt = Data()
dt.getDataFromSource()

class getCasesOnDay(Resource):
    def post(self):
        body = request.get_json()
        place = None
        try:
            place = body["place"]
        except:
            pass
        if place is None:
            place = "CABA"
        day = body["day"]
        casos_confirmados = dt.getCasosConfirmados(place)
        cant = casos_confirmados[casos_confirmados["id"]==day].shape[0]
        barrios = casos_confirmados["barrio"].value_counts(dropna=False)
        barrios.fillna('NA',inplace=True)
        barrios = barrios.to_dict()
        barrios = jsonify(barrios)
        return jsonify({"cant":cant,"barrios":barrios})
    

class getDeadOnDay(Resource):
    def post(self):
        body = request.get_json()
        place = None
        try:
            place = body["place"]
        except:
            pass
        if place is None:
            place = "CABA"
        day = body["day"]
        casos_confirmados = dt.getCasosConfirmados(place)
        casos_fallecidos_dia = casos_confirmados[(casos_confirmados["id"] == day) & (casos_confirmados["fallecido"] == "si")].copy()
        casos_fallecidos_dia.fillna("NA",inplace=True)
        barrios = casos_fallecidos_dia["barrio"].value_counts(dropna=False)
        cant = casos_fallecidos_dia.shape[0]
        print(barrios)
        barrios = barrios.to_dict()
        print(barrios)

        return jsonify({"cant":cant,"barrios":barrios})


api.add_resource(getCasesOnDay,"/getCasesOnDay")
api.add_resource(getDeadOnDay,"/getDeadOnDay")


if __name__ == "__main__":
    app.run(debug = True)