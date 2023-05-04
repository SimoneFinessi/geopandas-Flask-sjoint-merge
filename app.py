from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)

df=pd.read_excel("https://github.com/PolisenoRiccardo/perilPopolo/blob/main/milano_housing_02_2_23.xlsx?raw=true")

@app.route('/')
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)