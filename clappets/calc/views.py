from flask import request, render_template, jsonify, abort
from clappets import app
from clappets.document.utils import render_document

@app.route('/calculations/')
def calc_index():
    return render_template("calc/index.html")

@app.route('/calculations/process/')
def calc_process_index():
    return render_template("calc/process/index.html")

@app.route('/calculations/process/thermophysical/')
def calc_process_thermophysical_index():
    return render_template("calc/process/thermophysical/index.html")

@app.route('/calculations/process/thermophysical/chemical-fluid/')
def calc_process_thermophysical_fluid():
    return render_document("pro","cal","tch","flu")

@app.route('/calculations/process/thermophysical/hydrocarbon-mixture/')
def calc_process_thermophysical_hydrocarbon_mixture():
    return render_document("pro","cal","tch","mix")

@app.route('/calculations/process/thermophysical/water-steam/')
def calc_process_thermophysical_water_steam():
    return render_document("pro","cal","tch","wtr")

@app.route('/calculations/process/pressure-drop/')
def calc_process_pressure_drop_index():
    return render_template("calc/process/pressure_drop/index.html")

@app.route('/calculations/process/pressure-drop/hooper-2K/')
def calc_process_pressure_drop_hooper():
    return render_document("pro","cal","prd","h2k")

@app.route('/calculations/mechanical/')
def calc_mechanical_index():
    return render_template("calc/mechanical/index.html")

@app.route('/calculations/mechanical/pumps/')
def calc_mechanical_pump_index():
    return render_template("calc/mechanical/pumps/index.html")

@app.route('/calculations/mechanical/pumps/water2viscous/')
def calc_mechanical_pump_water2viscous():
    return render_document("mec","cal","pmp","w2v")

@app.route('/calculations/mechanical/pumps/viscous2water/')
def calc_mechanical_pump_viscous2water():
    return render_document("mec","cal","pmp","v2w")

@app.route('/calculations/mechanical/pumps/viscosity-conversions/')
def calc_mechanical_pump_viscosity_conversions():
    return render_document("mec","cal","pmp","vcn")

@app.route('/calculations/mechanical/engines/')
def calc_mechanical_engines_index():
    return render_template("calc/mechanical/engines/index.html")

@app.route('/calculations/mechanical/engines/gas-turbine-deration/')
def calc_mechanical_engines_gt_derate():
    return render_document("mec","cal","eng","gtd")

@app.route('/calculations/mechanical/engines/steam-turbine-performance/')
def calc_mechanical_engines_st_performance():
    return render_document("mec","cal","eng","stc")

@app.route('/calculations/mechanical/engines/diesel-fuel-consumption/')
def calc_mechanical_engines_dfc():
    return render_document("mec","cal","eng","dfc")

@app.route('/calculations/mechanical/noise/')
def calc_mechanical_noise_index():
    return render_template("calc/mechanical/noise/index.html")

@app.route('/calculations/mechanical/noise/distance-attenuation/')
def calc_mechanical_noise_attenuation():
    return render_document("mec","cal","nos","atn")

@app.route('/calculations/mechanical/noise/conversions/')
def calc_mechanical_noise_conversions():
    return render_document("mec","cal","nos","con")

@app.route('/calculations/mechanical/noise/Aweighted-spectrum/')
def calc_mechanical_noise_Aweighting():
    return render_document("mec","cal","nos","awt")

@app.route('/calculations/mechanical/noise/background-correction/')
def calc_mechanical_noise_background_correction():
    return render_document("mec","cal","nos","bcr")

@app.route('/calculations/mechanical/noise/map/')
def calc_mechanical_noise_map():
    return render_document("mec","cal","nos","map")

@app.route('/calculations/mechanical/noise/sum/')
def calc_mechanical_noise_sum():
    return render_document("mec","cal","nos","sum")

@app.route('/calculations/mechanical/piping/')
def calc_mechanical_piping_index():
    return render_template("calc/mechanical/piping/index.html")

@app.route('/calculations/mechanical/piping/pipe-dimensions/')
def calc_mechanical_piping_pipe_dimensions():
    return render_document("mec","cal","pip","sch")

@app.route('/calculations/mechanical/psychrometry/')
def calc_mechanical_psychrometry_index():
    return render_template("calc/mechanical/psychrometry/index.html")

@app.route('/calculations/mechanical/psychrometry/humid-air-props/')
def calc_mechanical_psychrometry_ha_props():
    return render_document("mec","cal","psy","hai")

@app.route('/calculations/instrumentation/')
def calc_instrumentation_index():
    return render_template("calc/instrumentation/index.html")

@app.route('/calculations/instrumentation/control-valves/')
def calc_instrumentation_controlvalves():
    return render_template("calc/instrumentation/controlvalves/index.html")

@app.route('/calculations/instrumentation/control-valves/liquid-service/')
def calc_instrumentation_controlvalves_liquid():
    return render_document("ins","cal","ctv","cvl")

@app.route('/calculations/instrumentation/control-valves/gas-service/')
def calc_instrumentation_controlvalves_gas():
    return render_document("ins","cal","ctv","cvg")

@app.route('/calculations/instrumentation/relief-valves/')
def calc_instrumentation_reliefvalves():
    return render_template("calc/instrumentation/reliefvalves/index.html")

@app.route('/calculations/instrumentation/relief-valves/liquid-service/')
def calc_instrumentation_reliefvalves_liquid():
    return render_document("ins","cal","prv","prl")

@app.route('/calculations/instrumentation/relief-valves/gas-service/')
def calc_instrumentation_reliefvalves_gas():
    return render_document("ins","cal","prv","prg")

@app.route('/calculations/instrumentation/relief-valves/steam-service/')
def calc_instrumentation_reliefvalves_steam():
    return render_document("ins","cal","prv","prs")

@app.route('/calculations/electrical/')
def calc_electrical_index():
    return render_template("calc/electrical/index.html")

@app.route('/calculations/electrical/cables/')
def calc_electrical_cables():
    return render_template("calc/electrical/cables/index.html")

@app.route('/calculations/electrical/cables/iec-sizing/')
def calc_electrical_cables_iec_sizing():
    return render_document("ele","cal","cab","iec")

@app.route('/calculations/electrical/miscellaneous/')
def calc_electrical_miscellaneous_index():
    return render_template("calc/electrical/utilities/index.html")

@app.route('/calculations/electrical/miscellaneous/three-phase/')
def calc_electrical_miscellaneous_three_phase():
    return render_document("ele","cal","utl","phs")

@app.route('/calculations/electrical/miscellaneous/power-factor-correction/')
def calc_electrical_miscellaneous_pfc():
    return render_document("ele","cal","utl","pfc")

@app.route('/calculations/electrical/lighting/')
def calc_electrical_lighting_index():
    return render_template("calc/electrical/lighting/index.html")

@app.route('/calculations/electrical/lighting/candela2lumens/')
def calc_electrical_lighting_candela2lumens():
    return render_document("ele","cal","lgt","c2l")

@app.route('/calculations/electrical/lighting/candela2lux/')
def calc_electrical_lighting_candela2lux():
    return render_document("ele","cal","lgt","c2x")

@app.route('/calculations/electrical/lighting/lumens2lux/')
def calc_electrical_lighting_lumens2lux():
    return render_document("ele","cal","lgt","l2x")

@app.route('/calculations/electrical/lighting/watts2lumens/')
def calc_electrical_lighting_watts2lumens():
    return render_document("ele","cal","lgt","w2l")

@app.route('/calculations/electrical/lighting/watts2lux/')
def calc_electrical_lighting_watts2lux():
    return render_document("ele","cal","lgt","w2x")

@app.route('/calculations/electrical/motors/')
def calc_electrical_motors_index():
    return render_template("calc/electrical/motors/index.html")

@app.route('/calculations/electrical/motors/starting-time/')
def calc_electrical_motors_starting_time():
    return render_document("ele","cal","mtr","str")
