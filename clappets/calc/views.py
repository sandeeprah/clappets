from flask import request, render_template, jsonify, abort, redirect
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


@app.route('/calculations/')
def calc_index():
    return render_template("calc/index.html")

@app.route('/calculations/process/')
def calc_process_index():
    return render_template("calc/process/index.html")

@app.route('/calculations/process/thermophysical/')
def calc_process_thermophysical_index():
    return render_template("calc/process/thermophysical/index.html")


@app.route('/calculations/process/thermophysical/chemical_fluid/')
def calc_process_thermophysical_fluid():
    return redirect("/htm/document/tpl/root/pro/cal/tch/flu/")

@app.route('/calculations/process/thermophysical/hydrocarbon_mixture/')
def calc_process_thermophysical_hydrocarbon_mixture():
    return redirect("/htm/document/tpl/root/pro/cal/tch/mix/")

@app.route('/calculations/process/thermophysical/water_steam/')
def calc_process_thermophysical_water_steam():
    return redirect("/htm/document/tpl/root/pro/cal/tch/wtr/")

@app.route('/calculations/process/pressure_drop/')
def calc_process_pressure_drop_index():
    return render_template("calc/process/pressure_drop/index.html")

@app.route('/calculations/mechanical/')
def calc_mechanical_index():
    return render_template("calc/mechanical/index.html")

@app.route('/calculations/mechanical/pumps/')
def calc_mechanical_pump_index():
    return render_template("calc/mechanical/pumps/index.html")

@app.route('/calculations/mechanical/engines/')
def calc_mechanical_engines_index():
    return render_template("calc/mechanical/engines/index.html")

@app.route('/calculations/mechanical/noise/')
def calc_mechanical_noise_index():
    return render_template("calc/mechanical/noise/index.html")

@app.route('/calculations/mechanical/psychrometry/')
def calc_mechanical_psychrometry_index():
    return render_template("calc/mechanical/psychrometry/index.html")
