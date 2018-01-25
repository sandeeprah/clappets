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

@app.route('/htm/calc/piping/')
def piping_index():
    return render_template("calc/piping/index.html")

@app.route('/htm/calc/controlvalves/')
def controlvalves_index():
    return render_template("calc/controlvalves/index.html")

@app.route('/htm/calc/engines/')
def engines_index():
    return render_template("calc/engines/index.html")

@app.route('/htm/calc/reliefvalves/')
def reliefvalves_index():
    return render_template("calc/reliefvalves/index.html")

@app.route('/htm/calc/pump/')
def pump_index():
    return render_template("calc/pump/index.html")

@app.route('/htm/calc/lighting/')
def lighting_index():
    return render_template("calc/lighting/index.html")

@app.route('/htm/calc/motors/')
def motors_index():
    return render_template("calc/motors/index.html")

@app.route('/htm/calc/cables/')
def cables_index():
    return render_template("calc/cables/index.html")
