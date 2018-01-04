from marshmallow import Schema, fields, validate, validates_schema
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
from techclappets.pressuredrop.line import reducer_sizes

import CoolProp.CoolProp as CP


class sFluidData(Schema):
    Q = fields.Nested(sXfld , validate=[vd.xNumber(), vd.xDim(['flow'])]) #Capacity, m3/s
    rho = fields.Nested(sXfld , validate=[vd.xNumber(), vd.xDim(['density'])]) #Density, kg/m3
    mu = fields.Nested(sXfld , validate=[vd.xNumber(), vd.xDim(['dynViscosity'])]) #Dynamic Viscosity, Pa.s
    class Meta:
        ordered = True

class sPipe(Schema):
    #size_definition = fields.String(required=True, validate=validate.OneOf(choices=size_definition_list))
    size_definition_list = ["NPS", "Custom"]
    size_definition = fields.Nested(sXfld , validate=vd.xChoice(size_definition_list))
    nps_list = [0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 10,
            12, 14, 16, 18, 20, 24, 26, 28, 30,
            32, 34, 36, 38, 40, 42, 44, 46, 48, 50,
            52, 54, 56, 58, 60, 66, 72, 78, 84, 90, 96,
            102, 108, 114, 120]
    NPS = fields.Nested(sXfld , validate=vd.xChoice(nps_list))
    Dia_inner = fields.Nested(sXfld , validate=vd.xNumber())
    schedule = fields.Nested(sXfld )
    material_list = ["Carbon Steel", "Cast Iron"]
    material = fields.Nested(sXfld )
    roughness_basis_list = ["Material", "Custom"]
    roughness_basis = fields.Nested(sXfld )
    roughness = fields.Nested(sXfld , validate=[vd.xNumber(), vd.xDim(['length', 'length_mili'])])
    length = fields.Nested(sXfld , validate=[vd.xNumber(), vd.xDim(['length'])])
    elevation = fields.Nested(sXfld , validate=[vd.xNumber(), vd.xDim(['length'])])

    class Meta:
        ordered = True


class sEntrance(Schema):
    entry_type_list = ["None", "Sharp", "Rounded", "Angled", "Projecting"]
    entry_type = fields.Nested(sXfld , validate = vd.xChoice(choices=entry_type_list))
    Di = fields.Nested(sXfld , validate=[vd.xNumber(blank=True), vd.xDim(['length', 'length_mili'])])
    Rc = fields.Nested(sXfld , validate=[vd.xNumber(blank=True), vd.xDim(['length', 'length_mili'])])
    angle = fields.Nested(sXfld , validate=[vd.xNumber()])
    wall_thickness = fields.Nested(sXfld , validate=[vd.xNumber(), vd.xDim(['length', 'length_mili'])])

    class Meta:
        ordered = True


    @validates_schema()
    def check_missingvalid(self,data):
        err_fields = []
        if 'entry_type' in data:
            if (data['entry_type']['_val']=='Rounded'):
                if vd.isMissing(data,'Di'):
                    err_fields.append('Di')
                if vd.isMissing(data,'Rc'):
                    err_fields.append('Rc')
            elif (data['entry_type']['_val']=='Angled'):
                if vd.isMissing(data,'angle'):
                    err_fields.append('angle')
            elif (data['entry_type']['_val']=='Projecting'):
                if vd.isMissing(data,'Di'):
                    err_fields.append('Di')
                if vd.isMissing(data,'wall_thickness'):
                    err_fields.append('wall_thickness')

            if (len(err_fields)>0):
                raise ValidationError("Field is required", err_fields)



class sExit(Schema):
    exit_type_list = ["None", "Normal"]
    exit_type = fields.Nested(sXfld , validate=vd.xChoice(exit_type_list))
    class Meta:
        ordered = True

class sFitting_quantity(Schema):
    index = fields.Integer(required=True)
    quantity = fields.Integer(required=True, missing=0)
    class Meta:
        ordered = True

class sColdim_contraction(Schema):
    allowable_dims_length = ['length', 'length_mili']
    D1 = fields.String(validate=validate.OneOf(choices=allowable_dims_length))
    D2 = fields.String(validate=validate.OneOf(choices=allowable_dims_length))
    Rc = fields.String(validate=validate.OneOf(choices=allowable_dims_length))
    L = fields.String(validate=validate.OneOf(choices=allowable_dims_length))

class sContraction_sharp(Schema):
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

class sContractions_sharp(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sContraction_sharp, many=True)


class sContraction_rounded(Schema):
    D1 = fields.Float(required=True, validate=vd.fMinExcl(0))
    D2 = fields.Float(required=True, validate=vd.fMinExcl(0))
    Rc = fields.Float(required=True, validate=vd.fMinExcl(0))
    quantity = fields.Integer(required=True, validate=vd.fMin(0))
    class Meta:
        ordered = True

    @validates_schema()
    def check_contraction(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] < data['D2']):
                raise ValidationError("D1 > D2 required")

class sContractions_rounded(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sContraction_rounded, many=True)


class sContraction_conical(Schema):
    D1 = fields.Float(required=True, validate=vd.fMinExcl(0))
    D2 = fields.Float(required=True, validate=vd.fMinExcl(0))
    L = fields.Float(required=True, validate=vd.fMinExcl(0))
    quantity = fields.Integer(required=True, validate=vd.fMin(0))
    class Meta:
        ordered = True

    @validates_schema()
    def check_contraction(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] < data['D2']):
                raise ValidationError("D1 > D2 required")

class sContractions_conical(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sContraction_conical, many=True)

class sContraction_reducer(Schema):
    size_list = reducer_sizes()
    reducer_size = fields.String(required=True, validate=validate.OneOf(choices=size_list))
    quantity = fields.Integer(required=True)
    class Meta:
        ordered = True

class sContractions_reducer(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sContraction_reducer, many=True)


class sExpansion_sharp(Schema):
    D1 = fields.Float(required=True, validate=vd.fMinExcl(0))
    D2 = fields.Float(required=True, validate=vd.fMinExcl(0))
    quantity = fields.Integer(required=True, validate=vd.fMin(0))
    class Meta:
        ordered = True

    @validates_schema()
    def check_expansion(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] > data['D2']):
                raise ValidationError("D1 < D2 required")

class sExpansions_sharp(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sExpansion_sharp, many=True)

class sExpansion_rounded(Schema):
    D1 = fields.Float(required=True, validate=vd.fMinExcl(0))
    D2 = fields.Float(required=True, validate=vd.fMinExcl(0))
    Rc = fields.Float(required=True, validate=vd.fMinExcl(0))
    quantity = fields.Integer(required=True, validate=vd.fMin(0))
    class Meta:
        ordered = True

    @validates_schema()
    def check_expansion(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] > data['D2']):
                raise ValidationError("D1 < D2 required")

class sExpansions_rounded(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sExpansion_rounded, many=True)

class sExpansion_conical(Schema):
    D1 = fields.Float(required=True, validate=vd.fMinExcl(0))
    D2 = fields.Float(required=True, validate=vd.fMinExcl(0))
    L = fields.Float(required=True, validate=vd.fMinExcl(0))
    quantity = fields.Integer(required=True, validate=vd.fMin(0))
    class Meta:
        ordered = True

    @validates_schema()
    def check_expansion(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] > data['D2']):
                raise ValidationError("D1 < D2 required")

class sExpansions_conical(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sExpansion_conical, many=True)


class sExpansion_reducer(Schema):
    size_list = reducer_sizes()
    reducer_size = fields.String(required=True, validate=validate.OneOf(choices=size_list))
    quantity = fields.Integer(required=True)
    class Meta:
        ordered = True

class sExpansions_reducer(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sExpansion_reducer, many=True)

class sOrifice(Schema):
    orifice_type_list = ["Thin_Sharp", "Thick"]
    orifice_type = fields.String(required=True, validate=validate.OneOf(choices=orifice_type_list))
    quantity = fields.Integer()
    class Meta:
        ordered = True

class sColdim_loss(Schema):
    deltaP = fields.String()


class sFixed_K_loss(Schema):
    K = fields.Float(required=True, validate=validate.Range(min=0))
    remark = fields.String()
    quantity = fields.Integer(required=True, validate=validate.Range(min=0))
    class Meta:
        ordered = True

class sFixed_K_losses(Schema):
    _coldim = fields.Nested(sColdim_loss)
    _default = fields.Nested(sFixed_K_loss)
    _list = fields.Nested(sFixed_K_loss, many=True)
    class Meta:
        ordered = True

class sFixed_LbyD_loss(Schema):
    LbyD = fields.Float(required=True, validate=vd.fMin(0))
    remark = fields.String()
    quantity = fields.Integer(required=True, validate=vd.fMin(0))
    class Meta:
        ordered = True

class sFixed_LbyD_losses(Schema):
    _coldim = fields.Nested(sColdim_loss)
    _default = fields.Nested(sFixed_LbyD_loss)
    _list = fields.Nested(sFixed_LbyD_loss, many=True)
    class Meta:
        ordered = True



class sFixed_deltaP_loss(Schema):
    deltaP = fields.Float(required=True, validate=vd.fMin(0))
    remark = fields.String()
    quantity = fields.Integer(required=True, validate=vd.fMin(0))

    class Meta:
        ordered = True


class sFixed_deltaP_losses(Schema):
    _coldim = fields.Nested(sColdim_loss)
    _default = fields.Nested(sFixed_deltaP_loss)
    _list = fields.Nested(sFixed_deltaP_loss, many=True)

    class Meta:
        ordered = True


class docInput(Schema):
    fluidData = fields.Nested(sFluidData)
    pipe = fields.Nested(sPipe)
    entrance = fields.Nested(sEntrance)
    exit = fields.Nested(sExit)
    fittings = fields.Nested(sFitting_quantity, many=True)
    contractions_sharp = fields.Nested(sContractions_sharp)
    contractions_rounded = fields.Nested(sContractions_rounded)
    contractions_conical = fields.Nested(sContractions_conical)
    contractions_reducer = fields.Nested(sContractions_reducer)
    expansions_sharp = fields.Nested(sExpansions_sharp)
    expansions_rounded = fields.Nested(sExpansions_rounded)
    expansions_conical = fields.Nested(sExpansions_conical)
    expansions_reducer = fields.Nested(sExpansions_reducer)
    orifice = fields.Nested(sOrifice, many=True)
    fixed_K_losses = fields.Nested(sFixed_K_losses)
    fixed_LbyD_losses = fields.Nested(sFixed_LbyD_losses)
    fixed_deltaP_losses = fields.Nested(sFixed_deltaP_losses)

    class Meta:
        ordered = True

class docResult(Schema):
    deltaP = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('pressure')])


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
