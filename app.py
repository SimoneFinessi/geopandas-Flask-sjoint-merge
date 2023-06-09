from flask import Flask, render_template, request, Response
import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from shapely.geometry import Point,Polygon
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

df=pd.read_csv("http://servizi.apss.tn.it/opendata/FARM001.csv")
comuni=gpd.read_file("/workspace/geopandas-Flask-sjoint-merge/Com01012022_g.zip")

df2=df[(df.LATITUDINE_P!="-") & (df.LONGITUDINE_P!="-") ]
geometry = [Point(xy) for xy in zip(df2.LONGITUDINE_P, df2.LATITUDINE_P)]
geodf = gpd.GeoDataFrame(df2, crs=4326, geometry=geometry)
geodf=geodf.drop("COMUNE", axis=1)
joint=gpd.sjoin(geodf.to_crs(32632),comuni,predicate="intersects",how="left")
nfarm=joint.groupby("COMUNE")[["FARMACIA"]].count().reset_index()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/es1')
def es1():
    trovato=geodf.to_html()
    return render_template("risultati.html",risultato=trovato )

@app.route('/es2', methods = ['POST'])
def es2():
    farm=request.form["farmacia"]
    return render_template("es2.html",farmacia=farm)

@app.route("/immagineEs2", methods = ['GET'])
def immagineEs2():
    farm=request.args["farmacia"]
    fig , ax = plt.subplots()
    geodf[geodf.FARMACIA.str.contains(farm)].to_crs(3857).plot(ax=ax)
    ctx.add_basemap(ax=ax)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/es3')
def es3():
    return render_template("es3.html")

@app.route("/immagineEs3")
def immagineEs3():
    fig, ax=plt.subplots()
    comuni[comuni.intersects(geodf.to_crs(32632).unary_union)].to_crs(3857).plot(ax=ax,edgecolor="black",alpha=0.3)
    geodf.to_crs(3857).plot(ax=ax,color="Red",markersize=1)
    ctx.add_basemap(ax=ax)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/es4')
def es4():
    global nfarm
    
    trovato=nfarm.to_html()
    return render_template("risultati.html",risultato=trovato)

@app.route('/es5')
def es5():
    return render_template("es5.html")

@app.route("/immagineEs5")
def immagineEs5():
    finale=comuni.merge(nfarm,on="COMUNE")
    fig , ax=plt.subplots()
    finale[finale.intersects(geodf.to_crs(32632).unary_union)].to_crs(3857).plot(ax=ax,edgecolor="black",alpha=0.3,column="FARMACIA",legend=True)
    geodf.to_crs(3857).plot(ax=ax,color="Red",markersize=1)
    ctx.add_basemap(ax=ax)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/es6')
def es6():
    return render_template("es6.html")

@app.route("/immagineEs6")
def immagineEs6():
    fig , ax=plt.subplots()
    ax.pie(nfarm.FARMACIA,labels=nfarm.COMUNE)
    plt.show()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
if __name__ == '__main__':
    app.run(debug=True)