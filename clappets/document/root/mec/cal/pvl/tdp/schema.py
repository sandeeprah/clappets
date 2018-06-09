from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld, xisBlank, xisMissing
from clappets.core import validator as vd

class docInput(Schema):
    Shape = fields.Nested(sXfld)
    Orientation = fields.Nested(sXfld)
    Head_A = fields.Nested(sXfld)
    Head_B = fields.Nested(sXfld)
    D_basis = fields.Nested(sXfld)
    D = fields.Nested(sXfld)
    Do = fields.Nested(sXfld)
    L = fields.Nested(sXfld)
    Pi = fields.Nested(sXfld)
    Ti = fields.Nested(sXfld)
    full_vacuum = fields.Nested(sXfld)
    ca = fields.Nested(sXfld)
    E = fields.Nested(sXfld)
    MOC = fields.Nested(sXfld)
    S = fields.Nested(sXfld)
    tn = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_Shape(self, data):
        fName = 'Shape'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        Shape_options = ["cylindrical", "spherical"]
        vd.xChoice(value, Shape_options, fName)

    @validates_schema()
    def check_Orientation(self, data):
        fName = 'Orientation'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        Orientation_options = ["horizontal", "vertical"]
        vd.xChoice(value, Orientation_options, fName)

    @validates_schema()
    def check_Head_A(self, data):
        fName = 'Head_A'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        head_options = ["ellipsoidal", "torispherical", "hemispherical", "conical", "toriconical"]
        vd.xChoice(value, head_options, fName)

    @validates_schema()
    def check_Head_B(self, data):
        fName = 'Head_B'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        head_options = ["ellipsoidal", "torispherical", "hemispherical", "conical", "toriconical"]
        vd.xChoice(value, head_options, fName)

    @validates_schema()
    def check_D_basis(self, data):
        fName = 'D_basis'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        D_basis_options = ["inner","outer"]
        vd.xChoice(value, D_basis_options, fName)

    @validates_schema()
    def check_D(self, data):
        if ('D_basis' not in data):
            return
        if (data['D_basis']['_val'] !='inner'):
            return
        fName = 'D'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value,['length'],fName)


    @validates_schema()
    def check_Do(self, data):
        if ('D_basis' not in data):
            return
        if (data['D_basis']['_val'] !='outer'):
            return
        fName = 'Do'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value,['length'],fName)

    @validates_schema()
    def check_L(self, data):
        fName = 'L'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value,['length'],fName)


    @validates_schema()
    def check_Pi(self, data):
        fName = 'Pi'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value,['pressure'],fName)

    @validates_schema()
    def check_Ti(self, data):
        fName = 'Ti'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['temperature'],fName)

    @validates_schema()
    def check_full_vacuum(self, data):
        fName = 'full_vacuum'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        full_vacuum_options = ["yes", "no"]
        vd.xChoice(value, full_vacuum_options, fName)

    @validates_schema()
    def check_ca(self, data):
        fName = 'ca'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['length'],fName)

    @validates_schema()
    def check_E(self, data):
        fName = 'E'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)

    @validates_schema()
    def check_MOC(self, data):
        fName = 'MOC'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        MOC_options = ["SA285-GrC", "SA516-Gr55","SA516-Gr60", "SA516-Gr70","SA240-Tp304L","SA240-Tp316L", "Other"]
        vd.xChoice(value, MOC_options, fName)

    @validates_schema()
    def check_S(self, data):
        fName = 'S'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value,['pressure'],fName)

    @validates_schema()
    def check_tn(self, data):
        fName = 'tn'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value,['length'],fName)

class docResult(Schema):
    R_calc = fields.Nested(sXfld)
    Ro_calc = fields.Nested(sXfld)
    S = fields.Nested(sXfld)

    ta = fields.Nested(sXfld)

    condn_Pc = fields.Nested(sXfld)
    tc = fields.Nested(sXfld)
    condn_tc = fields.Nested(sXfld)
    MAWPc = fields.Nested(sXfld)

    condn_Pl = fields.Nested(sXfld)
    tl = fields.Nested(sXfld)
    condn_tl = fields.Nested(sXfld)
    MAWPl = fields.Nested(sXfld)

    tu = fields.Nested(sXfld)
    t = fields.Nested(sXfld)
    tr = fields.Nested(sXfld)
    MAWP = fields.Nested(sXfld)
    tn_adequate = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
