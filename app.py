from flask import Flask, render_template, request
import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from shapely.geometry import Point,Polygon

app = Flask(__name__)

df=pd.read_csv("http://servizi.apss.tn.it/opendata/FARM001.csv")
comuni=gpd.read_file("/workspace/geopandas-Flask-sjoint-merge/Com01012022_g.zip")

df2=df[(df.LATITUDINE_P!="-") & (df.LONGITUDINE_P!="-") ]
geometry = [Point(xy) for xy in zip(df2.LONGITUDINE_P, df2.LATITUDINE_P)]
geodf = gpd.GeoDataFrame(df2, crs=4326, geometry=geometry)
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/es1')
def es1():
    trovato=geodf.to_html()
    return render_template("risultati.html",risultato=trovato )

if __name__ == '__main__':
    app.run(debug=True)