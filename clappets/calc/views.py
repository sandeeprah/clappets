from flask import request, render_template, jsonify, abort
from clappets import app

@app.route('/htm/calc/')
def calculation_index():
    return render_template("calc/index.html")

@app.route('/htm/calc/thermochem/')
def thermochem_index():
    return render_template("calc/thermochem/index.html")

@app.route('/htm/calc/pressuredrop/')
def pressuredrop_index():
    return render_template("calc/pressuredrop/index.html")

@app.route('/htm/calc/noise/')
def noise_index():
    return render_template("calc/noise/index.html")

@app.route('/htm/calc/pump/')
def pump_index():
    return render_template("calc/pump/index.html")
