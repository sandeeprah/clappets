import json
import sys
import math
import os
import fluids
import pandas as pd
from fluids.friction import friction_factor
from fluids.core import Reynolds, K_from_f, K_from_L_equiv, dP_from_K
from fluids.fittings import Hooper2K, entrance_sharp, exit_normal
from fluids.piping import nearest_pipe
from marshmallow import Schema, fields, pprint, pre_load, validate, validates,  validates_schema, ValidationError
#from techclappets.core import noemptySchema, schOneOf, schema_dquant, sXfld , sXfld , CalcOutput, check_positive, check_nonnegative
#from techclappets.pressuredrop.reducer import reducer_sizes, reducer_dimensions
from collections import OrderedDict
from techclappets.core import sXfld , chkChoice, chkNumber, chkMin, chkMax, chkString, chkDim, chkPrm, isMissing, sDocBase
from techclappets.core import validator as vd

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def reducer_sizes():
    my_file = os.path.join(THIS_FOLDER, 'reducer.csv')
    reducerdf = pd.read_csv(my_file)
    reducerdf = reducerdf.set_index('size_inches')
    return reducerdf.index.tolist()

def reducer_dimensions(reducer_size):
    my_file = os.path.join(THIS_FOLDER, 'reducer.csv')
    reducerdf = pd.read_csv(my_file)
    reducerdf = reducerdf.set_index('size_inches')
    D1 = reducerdf.loc[reducer_size, 'D1']/1000
    D2 = reducerdf.loc[reducer_size, 'D2']/1000
    L = reducerdf.loc[reducer_size, 'L']/1000
    return D1, D2, L

def pdrop_NPSreducer(reducer_size, Q, rho, mu, roughness):
    Dinlet, Doutlet, L = reducer_dimensions(reducer_size)
    Aoutlet = 3.1416 * (Dinlet ** 2) / 4
    Voutlet = Q / Aoutlet
    Re = fluids.core.Reynolds(Voutlet, Doutlet, rho, mu)
    relative_roughness = roughness/Dinlet
    fd = fluids.friction.friction_factor(Re, relative_roughness)
    K = fluids.fittings.contraction_conical(Dinlet, Doutlet, fd=fd, l=L)
    deltaP = fluids.core.dP_from_K(K,rho, Vinlet)
    return deltaP

def pdrop_NPSexpander(reducer_size, Q, rho, mu, roughness):
    Doutlet, Dinlet, L = reducer_dimensions(reducer_size)
    Ainlet = 3.1416 * (Dinlet ** 2) / 4
    Vinlet = Q / Ainlet
    Re = fluids.core.Reynolds(Vinlet, Dinlet, rho, mu)
    relative_roughness = roughness/Dinlet
    fd = fluids.friction.friction_factor(Re, relative_roughness)
    Kf = fluids.fittings.diffuser_pipe_reducer(Dinlet, Doutlet, l=L, fd1=fd)
    Kl = fluids.fittings.diffuser_conical(Dinlet, Doutlet, l=L*0.6, fd=fd)
    K = Kf+Kl
    deltaP = fluids.core.dP_from_K(K,rho, Vinlet)
    return deltaP


def get_hooper_list():
    Hooper = []
    Hooper.append('Elbow, 90°, Standard (R/D = 1), Screwed')
    Hooper.append('Elbow, 90°, Standard (R/D = 1), Flanged/welded')
    Hooper.append('Elbow, 90°, Long-radius (R/D = 1.5), All types')
    Hooper.append('Elbow, 90°, Mitered (R/D = 1.5), 1 weld (90° angle)')
    Hooper.append('Elbow, 90°, Mitered (R/D = 1.5), 2 weld (45° angle)')
    Hooper.append('Elbow, 90°, Mitered (R/D = 1.5), 3 weld (30° angle)')
    Hooper.append('Elbow, 90°, Mitered (R/D = 1.5), 4 weld (22.5° angle)')
    Hooper.append('Elbow, 90°, Mitered (R/D = 1.5), 5 weld (18° angle)')
    Hooper.append('Elbow, 45°, Standard (R/D = 1), All types')
    Hooper.append('Elbow, 45°, Long-radius (R/D 1.5), All types')
    Hooper.append('Elbow, 45°, Mitered (R/D=1.5), 1 weld (45° angle)')
    Hooper.append('Elbow, 45°, Mitered (R/D=1.5), 2 weld (22.5° angle)')
    Hooper.append('Elbow, 45°, Standard (R/D = 1), Screwed')
    Hooper.append('Elbow, 180°, Standard (R/D = 1), Flanged/welded')
    Hooper.append('Elbow, 180°, Long-radius (R/D = 1.5), All types')
    Hooper.append('Elbow, Used as, Standard, Screwed')
    Hooper.append('Elbow, Elbow, Long-radius, Screwed')
    Hooper.append('Elbow, Elbow, Standard, Flanged/welded')
    Hooper.append('Elbow, Elbow, Stub-in type branch')
    Hooper.append('Tee, Run, Screwed')
    Hooper.append('Tee, Through, Flanged or welded')
    Hooper.append('Tee, Tee, Stub-in type branch')
    Hooper.append('Valve, Gate, Full line size, Beta = 1')
    Hooper.append('Valve, Ball, Reduced trim, Beta = 0.9')
    Hooper.append('Valve, Plug, Reduced trim, Beta = 0.8')
    Hooper.append('Valve, Globe, Standard')
    Hooper.append('Valve, Globe, Angle or Y-type')
    Hooper.append('Valve, Diaphragm, Dam type')
    Hooper.append('Valve, Butterfly,')
    Hooper.append('Valve, Check, Lift')
    Hooper.append('Valve, Check, Swing')
    Hooper.append('Valve, Check, Tilting-disc')
    return Hooper

def hooper_name(item_index):
    Hooper = get_hooper_list()
    return Hooper[item_index]


def get_darby_list():
    Darby = []
    Darby.append('Elbow, 90°, threaded, standard, (r/D = 1)')
    Darby.append('Elbow, 90°, threaded, long radius, (r/D = 1.5)')
    Darby.append('Elbow, 90°, flanged, welded, bends, (r/D = 1)')
    Darby.append('Elbow, 90°, (r/D = 2)')
    Darby.append('Elbow, 90°, (r/D = 4)')
    Darby.append('Elbow, 90°, (r/D = 6)')
    Darby.append('Elbow, 90°, mitered, 1 weld, (90°)')
    Darby.append('Elbow, 90°, 2 welds, (45°)')
    Darby.append('Elbow, 90°, 3 welds, (30°)')
    Darby.append('Elbow, 45°, threaded standard, (r/D = 1)')
    Darby.append('Elbow, 45°, long radius, (r/D = 1.5)')
    Darby.append('Elbow, 45°, mitered, 1 weld, (45°)')
    Darby.append('Elbow, 45°, mitered, 2 welds, (22.5°)')
    Darby.append('Elbow, 180°, threaded, close-return bend, (r/D = 1)')
    Darby.append('Elbow, 180°, flanged, (r/D = 1)')
    Darby.append('Elbow, 180°, all, (r/D = 1.5)')
    Darby.append('Tee, Through-branch, (as elbow), threaded, (r/D = 1)')
    Darby.append('Tee, Through-branch,(as elbow), (r/D = 1.5)')
    Darby.append('Tee, Through-branch, (as elbow), flanged, (r/D = 1)')
    Darby.append('Tee, Through-branch, (as elbow), stub-in branch')
    Darby.append('Tee, Run-through, threaded, (r/D = 1)')
    Darby.append('Tee, Run-through, flanged, (r/D = 1)')
    Darby.append('Tee, Run-through, stub-in branch')
    Darby.append('Valve, Angle valve, 45°, full line size, β = 1')
    Darby.append('Valve, Angle valve, 90°, full line size, β = 1')
    Darby.append('Valve, Globe valve, standard, β = 1')
    Darby.append('Valve, Plug valve, branch flow')
    Darby.append('Valve, Plug valve, straight through')
    Darby.append('Valve, Plug valve, three-way (flow through)')
    Darby.append('Valve, Gate valve, standard, β = 1')
    Darby.append('Valve, Ball valve, standard, β = 1')
    Darby.append('Valve, Diaphragm, dam type')
    Darby.append('Valve, Swing check')
    Darby.append('Valve, Lift check')
    return Darby

def darby_name(item_index):
    Darby = get_darby_list()
    return Darby[item_index]

class schema_meta(Schema):
    line_id = fields.String()
    upstream_line_id = fields.String()
    downstream_line_id = fields.String()
    class Meta:
        ordered = True

class schema_fluidData(Schema):
    Q = fields.Nested(sXfld , validate=[chkNumber(), chkDim(['flow'])]) #Capacity, m3/s
    rho = fields.Nested(sXfld , validate=[chkNumber(), chkDim(['density'])]) #Density, kg/m3
    mu = fields.Nested(sXfld , validate=[chkNumber(), chkDim(['dynViscosity'])]) #Dynamic Viscosity, Pa.s
    class Meta:
        ordered = True


class schema_pipe(Schema):
    #size_definition = fields.String(required=True, validate=validate.OneOf(choices=size_definition_list))
    size_definition_list = ["NPS", "Custom"]
    size_definition = fields.Nested(sXfld , validate=chkChoice(size_definition_list))
    nps_list = [0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 10,
            12, 14, 16, 18, 20, 24, 26, 28, 30,
            32, 34, 36, 38, 40, 42, 44, 46, 48, 50,
            52, 54, 56, 58, 60, 66, 72, 78, 84, 90, 96,
            102, 108, 114, 120]
    NPS = fields.Nested(sXfld , validate=chkChoice(nps_list))
    Dia_inner = fields.Nested(sXfld , validate=chkNumber())
    schedule = fields.Nested(sXfld )
    material_list = ["Carbon Steel", "Cast Iron"]
    material = fields.Nested(sXfld )
    roughness_basis_list = ["Material", "Custom"]
    roughness_basis = fields.Nested(sXfld )
    roughness = fields.Nested(sXfld , validate=[chkNumber(), chkDim(['length', 'length_mili'])])
    length = fields.Nested(sXfld , validate=[chkNumber(), chkDim(['length'])])
    elevation = fields.Nested(sXfld , validate=[chkNumber(), chkDim(['length'])])

    class Meta:
        ordered = True


class schema_entrance(Schema):
    entry_type_list = ["None", "Sharp", "Rounded", "Angled", "Projecting"]
    entry_type = fields.Nested(sXfld , validate = chkChoice(choices=entry_type_list))
    Di = fields.Nested(sXfld , validate=[chkNumber(blank=True), chkDim(['length', 'length_mili'])])
    Rc = fields.Nested(sXfld , validate=[chkNumber(blank=True), chkDim(['length', 'length_mili'])])
    angle = fields.Nested(sXfld , validate=[chkNumber()])
    wall_thickness = fields.Nested(sXfld , validate=[chkNumber(), chkDim(['length', 'length_mili'])])

    class Meta:
        ordered = True


    @validates_schema()
    def check_missingvalid(self,data):
        err_fields = []
        if 'entry_type' in data:
            if (data['entry_type']['_val']=='Rounded'):
                if isMissing(data,'Di'):
                    err_fields.append('Di')
                if isMissing(data,'Rc'):
                    err_fields.append('Rc')
            elif (data['entry_type']['_val']=='Angled'):
                if isMissing(data,'angle'):
                    err_fields.append('angle')
            elif (data['entry_type']['_val']=='Projecting'):
                if isMissing(data,'Di'):
                    err_fields.append('Di')
                if isMissing(data,'wall_thickness'):
                    err_fields.append('wall_thickness')

            if (len(err_fields)>0):
                raise ValidationError("Field is required", err_fields)



class schema_exit(Schema):
    exit_type_list = ["None", "Normal"]
    exit_type = fields.Nested(sXfld , validate=chkChoice(exit_type_list))
    class Meta:
        ordered = True

class schema_fitting_quantity(Schema):
    index = fields.Integer(required=True)
    quantity = fields.Integer(required=True, missing=0)
    class Meta:
        ordered = True

class schema_coldim_contraction(Schema):
    allowable_dims_length = ['length', 'length_mili']
    D1 = fields.String(validate=validate.OneOf(choices=allowable_dims_length))
    D2 = fields.String(validate=validate.OneOf(choices=allowable_dims_length))
    Rc = fields.String(validate=validate.OneOf(choices=allowable_dims_length))
    L = fields.String(validate=validate.OneOf(choices=allowable_dims_length))

class schema_contraction_sharp(Schema):
    D1 = fields.Float(required=True, validate=validate.Range(min=0))
    D2 = fields.Float(required=True, validate=validate.Range(min=0))
    quantity = fields.Integer(required=True, validate=validate.Range(min=0))
    class Meta:
        ordered = True

    @validates_schema()
    def check_contraction(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] < data['D2']):
                raise ValidationError("D1 > D2 required")

class schema_contractions_sharp(Schema):
    _coldim = fields.Nested(schema_coldim_contraction)
    _list = fields.Nested(schema_contraction_sharp, many=True)


class schema_contraction_rounded(Schema):
    D1 = fields.Float(required=True, validate=vd.check_positive)
    D2 = fields.Float(required=True, validate=vd.check_positive)
    Rc = fields.Float(required=True, validate=vd.check_positive)
    quantity = fields.Integer(required=True, validate=vd.check_nonnegative)
    class Meta:
        ordered = True

    @validates_schema()
    def check_contraction(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] < data['D2']):
                raise ValidationError("D1 > D2 required")

class schema_contractions_rounded(Schema):
    _coldim = fields.Nested(schema_coldim_contraction)
    _list = fields.Nested(schema_contraction_rounded, many=True)


class schema_contraction_conical(Schema):
    D1 = fields.Float(required=True, validate=check_positive)
    D2 = fields.Float(required=True, validate=check_positive)
    L = fields.Float(required=True, validate=check_positive)
    quantity = fields.Integer(required=True, validate=check_nonnegative)
    class Meta:
        ordered = True

    @validates_schema()
    def check_contraction(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] < data['D2']):
                raise ValidationError("D1 > D2 required")

class schema_contractions_conical(Schema):
    _coldim = fields.Nested(schema_coldim_contraction)
    _list = fields.Nested(schema_contraction_conical, many=True)

class schema_contraction_reducer(Schema):
    size_list = reducer_sizes()
    reducer_size = fields.String(required=True, validate=validate.OneOf(choices=size_list))
    quantity = fields.Integer(required=True)
    class Meta:
        ordered = True

class schema_contractions_reducer(Schema):
    _coldim = fields.Nested(schema_coldim_contraction)
    _list = fields.Nested(schema_contraction_reducer, many=True)


class schema_expansion_sharp(Schema):
    D1 = fields.Float(required=True, validate=check_positive)
    D2 = fields.Float(required=True, validate=check_positive)
    quantity = fields.Integer(required=True, validate=check_nonnegative)
    class Meta:
        ordered = True

    @validates_schema()
    def check_expansion(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] > data['D2']):
                raise ValidationError("D1 < D2 required")

class schema_expansions_sharp(Schema):
    _coldim = fields.Nested(schema_coldim_contraction)
    _list = fields.Nested(schema_expansion_sharp, many=True)

class schema_expansion_rounded(Schema):
    D1 = fields.Float(required=True, validate=check_positive)
    D2 = fields.Float(required=True, validate=check_positive)
    Rc = fields.Float(required=True, validate=check_positive)
    quantity = fields.Integer(required=True, validate=check_nonnegative)
    class Meta:
        ordered = True

    @validates_schema()
    def check_expansion(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] > data['D2']):
                raise ValidationError("D1 < D2 required")

class schema_expansions_rounded(Schema):
    _coldim = fields.Nested(schema_coldim_contraction)
    _list = fields.Nested(schema_expansion_rounded, many=True)

class schema_expansion_conical(Schema):
    D1 = fields.Float(required=True, validate=check_positive)
    D2 = fields.Float(required=True, validate=check_positive)
    L = fields.Float(required=True, validate=check_positive)
    quantity = fields.Integer(required=True, validate=check_nonnegative)
    class Meta:
        ordered = True

    @validates_schema()
    def check_expansion(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] > data['D2']):
                raise ValidationError("D1 < D2 required")

class schema_expansions_conical(Schema):
    _coldim = fields.Nested(schema_coldim_contraction)
    _list = fields.Nested(schema_expansion_conical, many=True)


class schema_expansion_reducer(Schema):
    size_list = reducer_sizes()
    reducer_size = fields.String(required=True, validate=validate.OneOf(choices=size_list))
    quantity = fields.Integer(required=True)
    class Meta:
        ordered = True

class schema_expansions_reducer(Schema):
    _coldim = fields.Nested(schema_coldim_contraction)
    _list = fields.Nested(schema_expansion_reducer, many=True)

class schema_orifice(Schema):
    orifice_type_list = ["Thin_Sharp", "Thick"]
    orifice_type = fields.String(required=True, validate=validate.OneOf(choices=orifice_type_list))
    quantity = fields.Integer()
    class Meta:
        ordered = True

class schema_coldim_loss(Schema):
    deltaP = fields.String()


class schema_fixed_K_loss(Schema):
    K = fields.Float(required=True, validate=validate.Range(min=0))
    remark = fields.String()
    quantity = fields.Integer(required=True, validate=validate.Range(min=0))
    class Meta:
        ordered = True

class schema_fixed_K_losses(Schema):
    _coldim = fields.Nested(schema_coldim_loss)
    _default = fields.Nested(schema_fixed_K_loss)
    _list = fields.Nested(schema_fixed_K_loss, many=True)

class schema_fixed_LbyD_loss(Schema):
    LbyD = fields.Float(required=True, validate=check_nonnegative)
    remark = fields.String()
    quantity = fields.Integer(required=True, validate=check_nonnegative)
    class Meta:
        ordered = True

class schema_fixed_LbyD_losses(Schema):
    _coldim = fields.Nested(schema_coldim_loss)
    _default = fields.Nested(schema_fixed_LbyD_loss)
    _list = fields.Nested(schema_fixed_LbyD_loss, many=True)


class schema_fixed_deltaP_loss(Schema):
    deltaP = fields.Float(required=True, validate=check_nonnegative)
    remark = fields.String()
    quantity = fields.Integer(required=True, validate=check_nonnegative)
    class Meta:
        ordered = True


class schema_fixed_deltaP_losses(Schema):
    _coldim = fields.Nested(schema_coldim_loss)
    _default = fields.Nested(schema_fixed_deltaP_loss)
    _list = fields.Nested(schema_fixed_deltaP_loss, many=True)

class sInputLineDrop(Schema):
    fluidData = fields.Nested(schema_fluidData)
    pipe = fields.Nested(schema_pipe)
    entrance = fields.Nested(schema_entrance)
    exit = fields.Nested(schema_exit)
    fittings = fields.Nested(schema_fitting_quantity, many=True)
    contractions_sharp = fields.Nested(schema_contractions_sharp)
    contractions_rounded = fields.Nested(schema_contractions_rounded)
    contractions_conical = fields.Nested(schema_contractions_conical)
    contractions_reducer = fields.Nested(schema_contractions_reducer)
    expansions_sharp = fields.Nested(schema_expansions_sharp)
    expansions_rounded = fields.Nested(schema_expansions_rounded)
    expansions_conical = fields.Nested(schema_expansions_conical)
    expansions_reducer = fields.Nested(schema_expansions_reducer)
    orifice = fields.Nested(schema_orifice, many=True)
    fixed_K_losses = fields.Nested(schema_fixed_K_losses)
    fixed_LbyD_losses = fields.Nested(schema_fixed_LbyD_losses)
    fixed_deltaP_losses = fields.Nested(schema_fixed_deltaP_losses)

    class Meta:
        ordered = True

class sResultLineDrop(Schema):
    a = fields.String()

class sDocLineDrop(sDocBase):
    _input = fields.Nested(sInputLineDrop)
    _result = fields.Nested(sResultLineDrop)

def linedrop(input):
    result = OrderedDict()
    errors = OrderedDict()
    warnings = OrderedDict()
    input_schema = sInputLineDrop()
    parsed_input = input_schema.load(input)

    if (len(parsed_input.errors) > 0 ):
        errors = parsed_input.errors.copy()
    else:
        K_pipe = 0
        K_fittings = 0
        K_entry = 0
        K_exit = 0
        K_fixed = 0
        K_LbyD = 0
        K_total = 0
        LbyD_total = 0
        deltaP_fixed = 0
        deltaP_total = 0
        nominal_size = parsed_input.data['pipe']['NPS']['_val']
        schedule = parsed_input.data['pipe']['schedule']['_val']

        NPS, Di, Do, t = nearest_pipe(NPS=nominal_size, schedule=schedule)

        result.update({'Di' : {'_val':Di, '_dim': 'length_mili'} })
        result.update({'Do' : {'_val':Do, '_dim': 'length_mili'}})
        result.update({'t' : {'_val':t, '_dim': 'length_mili'}})

        area = math.pi*pow(Di/2, 2)
        Q = parsed_input.data['fluidData']['Q']['_val']
        V = Q/area
        result.update({'V' : {'_val':V, '_dim': 'speed'}})

        mu = parsed_input.data['fluidData']['mu']['_val']
        rho = parsed_input.data['fluidData']['rho']['_val']
        Re = Reynolds(V=V, D=Di, rho=rho, mu=mu)
        result.update({'Re' : {'_val':Re, '_dim': 'none'}})

        Hdyn = rho*pow(V,2)/2
        result.update({'Hdyn' : {'_val':Hdyn, '_dim': 'length'}})

        #K calculation for straigth pipe
        roughness = parsed_input.data['pipe']['roughness']['_val']
        eD = roughness/Di
        result.update({'eD' : eD})
        fd = friction_factor(Re=Re, eD=eD, Method="Moody")
        result.update({'fd Moody' : {'_val':fd, '_dim': 'none'}})


        length = parsed_input.data['pipe']['length']['_val']
        K_pipe = K_from_f(fd=fd, L=length, D=Di)
        result.update({'K_pipe' : {'_val':K_pipe, '_dim': 'none'}})
        deltaP_pipe = dP_from_K(K_pipe, rho, V)
        result.update({'deltaP_pipe' : {'_val':deltaP_pipe, '_dim': 'pressure'}})

        #calculating pressure drop for entrance
        entrance = parsed_input.data['entrance']
        entry_type = entrance['entry_type']['_val']
        if entry_type=='none':
            K_entry = 0
        elif entry_type=='sharp':
            K_entry = fluids.fittings.entrance_sharp()
        elif entry_type=='rounded':
            Di = entrance['Di']
            Rc = entrance['Rc']
            K_entry = fluids.fittings.entrance_rounded(Di, Rc)
        elif entry_type=='angled':
            angle = entrance['angle']
            K_entry = fluids.fittings.entrance_angled(angle)
        elif entry_type=='projecting':
            Di = entrance['Di']
            wall_thickness = entrance['wall_thickness']
            K_entry = fluids.fittings.entrance_distance(Di, wall_thickness)
        result.update({'K_entry' : {'_val':K_entry, '_dim': 'none'}})
        deltaP_entry = dP_from_K(K_entry, rho, V)
        result.update({'deltaP_entry' : {'_val':deltaP_entry, '_dim': 'pressure'}})

        #calculating pressure drop for exit
        exit_type = parsed_input.data['exit']['exit_type']
        if (exit_type=='Normal'):
            K_exit = exit_normal()
        else:
            K_exit = 0
        result.update({'K_exit' : {'_val':K_exit, '_dim': 'none'}})
        deltaP_exit = dP_from_K(K_exit, rho, V)
        result.update({'deltaP_exit' : {'_val':deltaP_exit, '_dim': 'pressure'}})

        #calculating pressure drop for fittings
        fittings_list = parsed_input.data['fittings']
        for fitting in fittings_list:
            name = get_hooper_list()[fitting['index']]
            Di_inch = Di*39.3701
            K_fitting = Hooper2K(Di_inch, Re, name=name)
            K_fittings += K_fitting*fitting['quantity']
        result.update({'K_fittings' : {'_val':K_fittings, '_dim': 'none'}})
        deltaP_fittings = dP_from_K(K_fittings, rho, V)
        result.update({'deltaP_fittings' : {'_val':deltaP_fittings, '_dim': 'pressure'}})

        #calculating pressure drop for sharp contractions
        deltaP_contractions_sharp = 0
        contractions_sharp = parsed_input.data['contractions_sharp']['_list']
        for contraction in contractions_sharp:
            D1 = contraction['D1']
            D2 = contraction['D2']
            A2 = 3.1416 * (D2 ** 2) / 4
            V2 = Q / A2
            K_contraction = fluids.fittings.contraction_sharp(D1, D2)
            deltaP = dP_from_K(K_contraction, rho, V2)
            deltaP_contractions_sharp += deltaP
        result.update({'deltaP_contractions_sharp' : {'_val':deltaP_contractions_sharp, '_dim': 'pressure'}})

        #calculating pressure drop for rounded contractions
        deltaP_contractions_rounded = 0
        contractions_rounded = parsed_input.data['contractions_rounded']['_list']
        for contraction in contractions_rounded:
            D1 = contraction['D1']
            D2 = contraction['D2']
            Rc = contraction['Rc']
            A2 = 3.1416 * (D2 ** 2) / 4
            V2 = Q / A2
            K_contraction = fluids.fittings.contraction_round(D1, D2, Rc)
            deltaP = dP_from_K(K_contraction, rho, V2)
            deltaP_contractions_rounded += deltaP
        result.update({'deltaP_contractions_rounded' : {'_val':deltaP_contractions_rounded, '_dim': 'pressure'}})

        #calculating pressure drop for conical contractions
        deltaP_contractions_conical = 0
        contractions_conical = parsed_input.data['contractions_conical']['_list']
        for contraction in contractions_conical:
            D1 = contraction['D1']
            D2 = contraction['D2']
            L = contraction['L']
            A2 = 3.1416 * (D2 ** 2) / 4
            V2 = Q / A2
            K_contraction = fluids.fittings.contraction_conical(D1, D2, fd=fd, l=L)
            deltaP = dP_from_K(K_contraction, rho, V2)
            deltaP_contractions_conical += deltaP
        result.update({'deltaP_contractions_conical' : {'_val':deltaP_contractions_conical, '_dim': 'pressure'}})

        #calculating pressure drop for pipe reducers contractions
        deltaP_contractions_reducer = 0
        contractions_reducer = parsed_input.data['contractions_reducer']['_list']
        for contraction in contractions_reducer:
            reducer_size = contraction['reducer_size']
            D1, D2, L = reducer_dimensions(reducer_size)
            A2 = 3.1416 * (D2 ** 2) / 4
            V2 = Q / A2
            K_contraction = fluids.fittings.contraction_conical(D1, D2, fd=fd, l=L)
            deltaP = dP_from_K(K_contraction, rho, V2)
            deltaP_contractions_reducer += deltaP
        result.update({'deltaP_contractions_reducer' : {'_val':deltaP_contractions_reducer, '_dim': 'pressure'}})

        # calculating total pressure drop in all contractions
        deltaP_contractions = deltaP_contractions_sharp + deltaP_contractions_rounded + deltaP_contractions_conical+ deltaP_contractions_reducer
        result.update({'deltaP_contractions' : {'_val':deltaP_contractions, '_dim': 'pressure'}})

        #calculating pressure drop for sharp expansions
        deltaP_expansions_sharp = 0
        expansions_sharp = parsed_input.data['expansions_sharp']['_list']
        for contraction in expansions_sharp:
            D1 = contraction['D1']
            D2 = contraction['D2']
            A1 = 3.1416 * (D1 ** 2) / 4
            V1 = Q / A1
            K_contraction = fluids.fittings.diffuser_sharp(D1, D2)
            deltaP = dP_from_K(K_contraction, rho, V1)
            deltaP_expansions_sharp += deltaP
        result.update({'deltaP_expansions_sharp' : {'_val':deltaP_expansions_sharp, '_dim': 'pressure'}})

        #calculating pressure drop for conical expansions
        deltaP_expansions_conical = 0
        expansions_conical = parsed_input.data['expansions_conical']['_list']
        for contraction in expansions_conical:
            D1 = contraction['D1']
            D2 = contraction['D2']
            L = contraction['L']
            A1 = 3.1416 * (D1 ** 2) / 4
            V1 = Q / A1
            K_contraction = fluids.fittings.diffuser_conical(D1, D2, fd=fd, l=L)
            deltaP = dP_from_K(K_contraction, rho, V1)
            deltaP_expansions_conical += deltaP
        result.update({'deltaP_expansions_conical' : {'_val':deltaP_expansions_conical, '_dim': 'pressure'}})

        #calculating pressure drop for pipe reducer expansions
        deltaP_expansions_reducer = 0
        expansions_reducer = parsed_input.data['expansions_reducer']['_list']
        for contraction in expansions_reducer:
            reducer_size = contraction['reducer_size']
            D2, D1, L = reducer_dimensions(reducer_size)
            A1 = 3.1416 * (D1 ** 2) / 4
            V1 = Q / A1
            K_contraction = fluids.fittings.diffuser_conical(D1, D2, fd=fd, l=L)
            deltaP = dP_from_K(K_contraction, rho, V1)
            deltaP_expansions_reducer += deltaP
        result.update({'deltaP_expansions_reducer' : {'_val':deltaP_expansions_reducer, '_dim': 'pressure'}})

        # calculating total pressure drop in all expansions
        deltaP_expansions = deltaP_expansions_sharp + deltaP_expansions_conical+ deltaP_expansions_reducer
        result.update({'deltaP_expansions' : {'_val':deltaP_expansions, '_dim': 'pressure'}})


        fixed_K_loss = parsed_input.data['fixed_K_losses']['_list']
        for loss in fixed_K_loss:
            K_fixed += loss['K']*loss['quantity']
        deltaP_fixed_K = dP_from_K(K_fixed, rho, V)

        fixed_LbyD_loss = parsed_input.data['fixed_LbyD_losses']['_list']
        for loss in fixed_LbyD_loss:
            L_D = loss['LbyD']
            K_LbyD += K_from_L_equiv(L_D = L_D, fd=fd)*loss['quantity']
        deltaP_fixed_LbyD = dP_from_K(K_LbyD, rho, V)

        fixed_deltaP_loss = parsed_input.data['fixed_deltaP_losses']['_list']
        for loss in fixed_deltaP_loss:
            deltaP_fixed += loss['deltaP']*loss['quantity']
        deltaP_fixed_deltaP = deltaP_fixed

        deltaP_fixed_all = deltaP_fixed_K + deltaP_fixed_LbyD + deltaP_fixed_deltaP
        result.update({'deltaP_fixed_all' : {'_val':deltaP_fixed_all, '_dim': 'pressure'}})

        deltaP_total = deltaP_pipe + deltaP_entry + deltaP_exit + deltaP_fittings + deltaP_contractions + deltaP_expansions+deltaP_fixed_all
        result.update({'deltaP_total' : {'_val':deltaP_total, '_dim': 'pressure'}})

    return result, errors
