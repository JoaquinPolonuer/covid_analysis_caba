import pandas as pd
import matplotlib.pyplot as plt

def plot_casos(df):
    casos_dict = {}

    for i in df["id"]:
        casos_dict[i] = casos_dict.get(i,0)+1

    x,y = zip(*casos_dict.items())
    plt.plot(x,y)
    plt.savefig('foo.png')
    plt.show()

dat = pd.read_csv("https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/casos-covid-19/casos_covid19.csv")
casos_confirmados = dat[dat["clasificacion"]=="confirmado"].copy()
del casos_confirmados["fecha_apertura_snvs"]
del casos_confirmados["fecha_toma_muestra"]
del casos_confirmados["clasificacion"]
meses_replace = {"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,"JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}
casos_confirmados["mes_confirmado"] = casos_confirmados["fecha_clasificacion"].str[2:5]
casos_confirmados["dia_confirmado"] = casos_confirmados["fecha_clasificacion"].str[:2]
casos_confirmados["mes_confirmado_num"] = casos_confirmados["mes_confirmado"].replace(meses_replace)
casos_confirmados = casos_confirmados.sort_values(["mes_confirmado_num", "dia_confirmado"])
casos_confirmados["mes_confirmado_num"] = casos_confirmados["mes_confirmado_num"].astype(str)
casos_confirmados["id"] = casos_confirmados["dia_confirmado"].map(str) +"/"+casos_confirmados["mes_confirmado_num"].map(str)
casos_confirmados_caba = casos_confirmados.copy()[casos_confirmados["provincia"]=="CABA"]
plot_casos(casos_confirmados_caba)
plot_casos(casos_confirmados)