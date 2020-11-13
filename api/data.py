import pandas as pd
import matplotlib.pyplot as plt


class Data:
    def __init__(self):
        self.casos_confirmados_bsas = None
        self.casos_confirmados_caba = None
        self.casos_descartados_caba = None
        self.casos_descartados_bsas = None

    def fixData(self,casos):
        del casos["fecha_apertura_snvs"]
        del casos["fecha_toma_muestra"]
        del casos["clasificacion"]
        meses_replace = {"JAN":"01","FEB":"02","MAR":"03","APR":"04","MAY":"05","JUN":"06","JUL":"07","AUG":"08","SEP":"09","OCT":"10","NOV":"11","DEC":"12"}
        casos["mes_confirmado"] = casos["fecha_clasificacion"].str[2:5]
        casos["dia_confirmado"] = casos["fecha_clasificacion"].str[:2]
        casos["mes_confirmado_num"] = casos["mes_confirmado"].replace(meses_replace)
        casos = casos.sort_values(["mes_confirmado_num", "dia_confirmado"])
        casos["mes_confirmado_num"] = casos["mes_confirmado_num"].astype(str)
        casos["id"] = casos["mes_confirmado_num"].map(str) +"/"+casos["dia_confirmado"].map(str)
        casos_caba = casos.copy()[casos["provincia"]=="CABA"]
        casos_bsas = casos.copy()[casos["provincia"] == "Buenos Aires"]
        return casos_caba,casos_bsas

    
    def getDataFromSource(self):
        dat = pd.read_csv("https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/casos-covid-19/casos_covid19.csv")
        casos_confirmados = dat[dat["clasificacion"]=="confirmado"].copy()
        casos_descartados = dat[dat["clasificacion"] == "descartado"].copy()
        self.casos_confirmados_caba,self.casos_confirmados_bsas = self.fixData(casos_confirmados.copy())
        self.casos_descartados_caba,self.casos_descartados_bsas = self.fixData(casos_descartados.copy())


    def getCasosConfirmados(self,place = "CABA"):
        if place == "CABA":
            return self.casos_confirmados_caba.copy()
        elif place == "Buenos Aires":
            return self.casos_confirmados_bsas.copy()

    def getCasosDescartados(self,place = "CABA"):
        if place == "CABA":
            return self.casos_descartados_caba.copy()
        elif place == "Buenos Aires":
            return self.casos_descartados_bsas.copy()
