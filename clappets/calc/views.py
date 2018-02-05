from flask import request, render_template, jsonify, abort, redirect
from clappets import app

@app.route('/htm/calc/')
def calculation_index():
    return render_template("calc/index.html")


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

@app.route('/calculations/process/pressure_drop/hooper_2K/')
def calc_process_pressure_drop_hooper():
    return redirect("/htm/document/tpl/root/pro/cal/prd/h2k/")




@app.route('/calculations/mechanical/')
def calc_mechanical_index():
    return render_template("calc/mechanical/index.html")

@app.route('/calculations/mechanical/pumps/')
def calc_mechanical_pump_index():
    return render_template("calc/mechanical/pumps/index.html")

@app.route('/calculations/mechanical/pumps/water2viscous/')
def calc_mechanical_pump_water2viscous():
    return redirect("/htm/document/tpl/root/mec/cal/pmp/w2v/")

@app.route('/calculations/mechanical/pumps/viscous2water/')
def calc_mechanical_pump_viscous2water():
    return redirect("/htm/document/tpl/root/mec/cal/pmp/v2w/")

@app.route('/calculations/mechanical/pumps/viscosity_conversions/')
def calc_mechanical_pump_viscosity_conversions():
    return redirect("/htm/document/tpl/root/mec/cal/pmp/vcn/")

@app.route('/calculations/mechanical/engines/')
def calc_mechanical_engines_index():
    return render_template("calc/mechanical/engines/index.html")


@app.route('/calculations/mechanical/engines/gas_turbine_deration/')
def calc_mechanical_engines_gt_derate():
    return redirect("/htm/document/tpl/root/mec/cal/eng/gtd/")

@app.route('/calculations/mechanical/engines/steam_turbine_performance/')
def calc_mechanical_engines_st_performance():
    return redirect("/htm/document/tpl/root/mec/cal/eng/stc/")

@app.route('/calculations/mechanical/engines/diesel_fuel_consumption/')
def calc_mechanical_engines_dfc():
    return redirect("/htm/document/tpl/root/mec/cal/eng/dfc/")


@app.route('/calculations/mechanical/noise/')
def calc_mechanical_noise_index():
    return render_template("calc/mechanical/noise/index.html")

@app.route('/calculations/mechanical/noise/distance_attenuation/')
def calc_mechanical_noise_attenuation():
    return redirect("/htm/document/tpl/root/mec/cal/nos/atn/")

@app.route('/calculations/mechanical/noise/conversions/')
def calc_mechanical_noise_conversions():
    return redirect("/htm/document/tpl/root/mec/cal/nos/con/")

@app.route('/calculations/mechanical/noise/Aweighted_spectrum/')
def calc_mechanical_noise_Aweighting():
    return redirect("/htm/document/tpl/root/mec/cal/nos/awt/")

@app.route('/calculations/mechanical/noise/background_correction/')
def calc_mechanical_noise_background_correction():
    return redirect("/htm/document/tpl/root/mec/cal/nos/bcr/")

@app.route('/calculations/mechanical/noise/map/')
def calc_mechanical_noise_map():
    return redirect("/htm/document/tpl/root/mec/cal/nos/map/")

@app.route('/calculations/mechanical/noise/sum/')
def calc_mechanical_noise_sum():
    return redirect("/htm/document/tpl/root/mec/cal/nos/sum/")

@app.route('/calculations/mechanical/piping/')
def calc_mechanical_piping_index():
    return render_template("calc/mechanical/piping/index.html")

@app.route('/calculations/mechanical/piping/pipe_dimensions/')
def calc_mechanical_piping_pipe_dimensions():
    return redirect("/htm/document/tpl/root/mec/cal/pip/sch/")

@app.route('/calculations/mechanical/psychrometry/')
def calc_mechanical_psychrometry_index():
    return render_template("calc/mechanical/psychrometry/index.html")

@app.route('/calculations/mechanical/psychrometry/humid_air_props/')
def calc_mechanical_psychrometry_ha_props():
    return redirect("/htm/document/tpl/root/mec/cal/psy/hai/")



@app.route('/calculations/instrumentation/')
def calc_instrumentation_index():
    return render_template("calc/instrumentation/index.html")

@app.route('/calculations/instrumentation/control_valves/')
def calc_instrumentation_controlvalves():
    return render_template("calc/instrumentation/controlvalves/index.html")

@app.route('/calculations/instrumentation/control_valves/liquid_service/')
def calc_instrumentation_controlvalves_liquid():
    return redirect("/htm/document/tpl/root/ins/cal/ctv/cvl/")

@app.route('/calculations/instrumentation/control_valves/gas_service/')
def calc_instrumentation_controlvalves_gas():
    return redirect("/htm/document/tpl/root/ins/cal/ctv/cvg/")

@app.route('/calculations/instrumentation/relief_valves/')
def calc_instrumentation_reliefvalves():
    return render_template("calc/instrumentation/reliefvalves/index.html")

@app.route('/calculations/instrumentation/relief_valves/liquid_service/')
def calc_instrumentation_reliefvalves_liquid():
    return redirect("/htm/document/tpl/root/ins/cal/prv/prl/")

@app.route('/calculations/instrumentation/relief_valves/gas_service/')
def calc_instrumentation_reliefvalves_gas():
    return redirect("/htm/document/tpl/root/ins/cal/prv/prg/")

@app.route('/calculations/instrumentation/relief_valves/steam_service/')
def calc_instrumentation_reliefvalves_steam():
    return redirect("/htm/document/tpl/root/ins/cal/prv/prs/")

@app.route('/calculations/electrical/')
def calc_electrical_index():
    return render_template("calc/electrical/index.html")

@app.route('/calculations/electrical/cables/')
def calc_electrical_cables():
    return render_template("calc/electrical/cables/index.html")

@app.route('/calculations/electrical/cables/iec_sizing/')
def calc_electrical_cables_iec_sizing():
    return redirect("/htm/document/tpl/root/ele/cal/cab/iec/")

@app.route('/calculations/electrical/miscellaneous/')
def calc_electrical_miscellaneous_index():
    return render_template("calc/electrical/utilities/index.html")

@app.route('/calculations/electrical/miscellaneous/three_phase/')
def calc_electrical_miscellaneous_three_phase():
    return redirect("/htm/document/tpl/root/ele/cal/utl/phs/")

@app.route('/calculations/electrical/miscellaneous/power_factor_correction/')
def calc_electrical_miscellaneous_pfc():
    return redirect("/htm/document/tpl/root/ele/cal/utl/pfc/")

@app.route('/calculations/electrical/lighting/')
def calc_electrical_lighting_index():
    return render_template("calc/electrical/lighting/index.html")

@app.route('/calculations/electrical/lighting/candela2lumens/')
def calc_electrical_lighting_candela2lumens():
    return redirect("/htm/document/tpl/root/ele/cal/lgt/c2l/")

@app.route('/calculations/electrical/lighting/candela2lux/')
def calc_electrical_lighting_candela2lux():
    return redirect("/htm/document/tpl/root/ele/cal/lgt/c2x/")

@app.route('/calculations/electrical/lighting/lumens2lux/')
def calc_electrical_lighting_lumens2lux():
    return redirect("/htm/document/tpl/root/ele/cal/lgt/l2x/")

@app.route('/calculations/electrical/lighting/watts2lumens/')
def calc_electrical_lighting_watts2lumens():
    return redirect("/htm/document/tpl/root/ele/cal/lgt/w2l/")

@app.route('/calculations/electrical/lighting/watts2lux/')
def calc_electrical_lighting_watts2lux():
    return redirect("/htm/document/tpl/root/ele/cal/lgt/w2x/")

@app.route('/calculations/electrical/motors/')
def calc_electrical_motors_index():
    return render_template("calc/electrical/motors/index.html")

@app.route('/calculations/electrical/motors/starting_time/')
def calc_electrical_motors_starting_time():
    return redirect("/htm/document/tpl/root/ele/cal/mtr/str/")
