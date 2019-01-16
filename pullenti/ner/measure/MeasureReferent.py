﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.measure.UnitReferent import UnitReferent
from pullenti.ner.measure.MeasureKind import MeasureKind
from pullenti.ner.Referent import Referent
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.measure.internal.MeasureMeta import MeasureMeta
from pullenti.ner.measure.internal.MeasureHelper import MeasureHelper

class MeasureReferent(Referent):
    """ Величина или диапазон величин, измеряемая в некоторых единицах """
    
    def __init__(self) -> None:
        super().__init__(MeasureReferent.OBJ_TYPENAME)
        self.instance_of = MeasureMeta.GLOBAL_META
    
    OBJ_TYPENAME = "MEASURE"
    
    ATTR_TEMPLATE = "TEMPLATE"
    
    ATTR_VALUE = "VALUE"
    
    ATTR_UNIT = "UNIT"
    
    ATTR_REF = "REF"
    
    ATTR_NAME = "NAME"
    
    ATTR_KIND = "KIND"
    
    @property
    def template(self) -> str:
        """ Шаблон для значений, например, [1..2], 1x2, 1 ]..1] """
        return Utils.ifNotNull(self.getStringValue(MeasureReferent.ATTR_TEMPLATE), "1")
    @template.setter
    def template(self, value) -> str:
        self.addSlot(MeasureReferent.ATTR_TEMPLATE, value, True, 0)
        return value
    
    @property
    def double_values(self) -> typing.List[float]:
        res = list()
        for s in self.slots: 
            if (s.type_name == MeasureReferent.ATTR_VALUE and (isinstance(s.value, str))): 
                wrapd1624 = RefOutArgWrapper(0)
                inoutres1625 = MeasureHelper.tryParseDouble(Utils.asObjectOrNull(s.value, str), wrapd1624)
                d = wrapd1624.value
                if (inoutres1625): 
                    res.append(d)
        return res
    
    def addValue(self, d : float) -> None:
        self.addSlot(MeasureReferent.ATTR_VALUE, NumberHelper.doubleToString(d), False, 0)
    
    @property
    def units(self) -> typing.List['UnitReferent']:
        res = list()
        for s in self.slots: 
            if (s.type_name == MeasureReferent.ATTR_UNIT and (isinstance(s.value, UnitReferent))): 
                res.append(Utils.asObjectOrNull(s.value, UnitReferent))
        return res
    
    @property
    def kind(self) -> 'MeasureKind':
        str0_ = self.getStringValue(MeasureReferent.ATTR_KIND)
        if (str0_ is None): 
            return MeasureKind.UNDEFINED
        try: 
            return Utils.valToEnum(str0_, MeasureKind)
        except Exception as ex1626: 
            pass
        return MeasureKind.UNDEFINED
    @kind.setter
    def kind(self, value) -> 'MeasureKind':
        if (value != MeasureKind.UNDEFINED): 
            self.addSlot(MeasureReferent.ATTR_KIND, Utils.enumToString(value).upper(), True, 0)
        return value
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = Utils.newStringIO(self.template)
        vals = list()
        for s in self.slots: 
            if (s.type_name == MeasureReferent.ATTR_VALUE): 
                if (isinstance(s.value, str)): 
                    vals.append(Utils.asObjectOrNull(s.value, str))
                elif (isinstance(s.value, Referent)): 
                    vals.append((s.value).toString(True, lang, 0))
        for i in range(res.tell() - 1, -1, -1):
            ch = Utils.getCharAtStringIO(res, i)
            if (not str.isdigit(ch)): 
                continue
            j = ((ord(ch)) - (ord('1')))
            if ((j < 0) or j >= len(vals)): 
                continue
            Utils.removeStringIO(res, i, 1)
            Utils.insertStringIO(res, i, vals[j])
        uu = self.units
        if (len(uu) > 0): 
            print(uu[0].toString(True, lang, 0), end="", file=res)
            i = 1
            while i < len(uu): 
                pow0_ = uu[i].getStringValue(UnitReferent.ATTR_POW)
                if (not Utils.isNullOrEmpty(pow0_) and pow0_[0] == '-'): 
                    print("/{0}".format(uu[i].toString(True, lang, 1)), end="", file=res, flush=True)
                    if (pow0_ != "-1"): 
                        print("<{0}>".format(pow0_[1:]), end="", file=res, flush=True)
                else: 
                    print("*{0}".format(uu[i].toString(True, lang, 0)), end="", file=res, flush=True)
                i += 1
        if (not short_variant): 
            nam = self.getStringValue(MeasureReferent.ATTR_NAME)
            if (nam is not None): 
                print(" - {0}".format(nam), end="", file=res, flush=True)
            for s in self.slots: 
                if (s.type_name == MeasureReferent.ATTR_REF and (isinstance(s.value, MeasureReferent))): 
                    print(" / {0}".format((s.value).toString(True, lang, 0)), end="", file=res, flush=True)
            ki = self.kind
            if (ki != MeasureKind.UNDEFINED): 
                print(" ({0})".format(Utils.enumToString(ki).upper()), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        mr = Utils.asObjectOrNull(obj, MeasureReferent)
        if (mr is None): 
            return False
        if (self.template != mr.template): 
            return False
        vals1 = self.getStringValues(MeasureReferent.ATTR_VALUE)
        vals2 = mr.getStringValues(MeasureReferent.ATTR_VALUE)
        if (len(vals1) != len(vals2)): 
            return False
        i = 0
        while i < len(vals2): 
            if (vals1[i] != vals2[i]): 
                return False
            i += 1
        units1 = self.units
        units2 = mr.units
        if (len(units1) != len(units2)): 
            return False
        i = 0
        while i < len(units2): 
            if (units1[i] != units2[i]): 
                return False
            i += 1
        for s in self.slots: 
            if (s.type_name == MeasureReferent.ATTR_REF or s.type_name == MeasureReferent.ATTR_NAME): 
                if (mr.findSlot(s.type_name, s.value, True) is None): 
                    return False
        for s in mr.slots: 
            if (s.type_name == MeasureReferent.ATTR_REF or s.type_name == MeasureReferent.ATTR_NAME): 
                if (self.findSlot(s.type_name, s.value, True) is None): 
                    return False
        return True