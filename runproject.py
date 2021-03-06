from flask import Flask, render_template, url_for, request, send_from_directory
import numpy as np
import pandas as pd
import folium
import joblib

# server = Flask(__name__)

# translate Flask to python object
server = Flask(__name__,static_url_path='', 
            static_folder='web')

@server.route("/")
def home():
    return render_template("index.html")

@server.route("/predict")
def predict():
    return render_template("predict.html")

@server.route("/statistic")
def statistic():
    return render_template("statistic.html")


@server.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        input = request.form
        #Region
        region = input["geo"]
        strRegion = ""
        if region == "fra":
            fra = 1
            ger = 0
            spa = 0
            strRegion = "France"
        if region == "ger":
            fra = 0
            ger = 1
            spa = 0
            strRegion = "German"
        if region == "spa":
            fra = 0
            ger = 0
            spa = 1
            strRegion = "Spain"
        #Gender
        gender = input["gender"]
        strGender = ""
        if gender == "m":
            mal = 1
            fem = 0
            strGender = "Male"
        if gender == "f":
            mal = 0
            fem = 1
            strGender = "Female"
        #CCard
        ccard = input["ccard"]
        strCard = ""
        if ccard == "y":
            cc = 1
            strCard = "Yes"
        else:
            cc = 0
            strCard = "No"
        #Active
        active = input["active"]
        strAct = ""
        if active == "y":
            act = 1
            strAct = "Yes"
        else:
            act = 0
            strAct = "No"
        #Product
        prod = int(input["prod"])
        #Age
        age = int(input["age"])
        #Tenure
        ten = int(input["tenure"])
        #Credit
        crd = int(input["credit"])
        #Salary
        sal = float(input["salary"])
        #Balance
        bal = float(input["balance"])
        # Result
        # data yang di masukan harus urut sesuai dataset dummy
        datainput = [[crd, age, ten, bal, prod, cc, act, sal, fra, ger, spa, fem, mal]]
        pred_proba = model.predict_proba(datainput)[0]
        if pred_proba[0] < 0.495443:
            # pred = 0
            prbb = round((pred_proba[0]*100), 1)
            rslt = "RETAIN"
        else:
            # pred = 1
            prbb = round((pred_proba[1]*100), 1)
            rslt = "EXIT"
        return render_template(
            "result.html", region= strRegion, gender= strGender,
            credit= crd, age= age, tenure= ten, balance= bal,
            product= prod, ccard = strCard, active= strAct, salary= sal,
            result= rslt, proba = prbb
        )

if __name__ == '__main__':
    model = joblib.load("model")
    server.run(debug=True, port=1212)