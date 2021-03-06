﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.Referent import Referent
from pullenti.ner.measure.internal.UnitMeta import UnitMeta

class UnitReferent(Referent):
    """ Ежиница измерения """
    
    def __init__(self) -> None:
        super().__init__(UnitReferent.OBJ_TYPENAME)
        self._m_unit = None;
        self.instance_of = UnitMeta.GLOBAL_META
    
    OBJ_TYPENAME = "MEASUREUNIT"
    
    ATTR_FULLNAME = "FULLNAME"
    
    ATTR_NAME = "NAME"
    
    ATTR_POW = "POW"
    
    ATTR_BASEFACTOR = "BASEFACTOR"
    
    ATTR_BASEUNIT = "BASEUNIT"
    
    ATTR_UNKNOWN = "UNKNOWN"
    
    @property
    def parent_referent(self) -> 'Referent':
        return Utils.asObjectOrNull(self.getSlotValue(UnitReferent.ATTR_BASEUNIT), Referent)
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        nam = None
        for l_ in range(2):
            for s in self.slots: 
                if (((s.type_name == UnitReferent.ATTR_NAME and short_variant)) or ((s.type_name == UnitReferent.ATTR_FULLNAME and not short_variant))): 
                    val = Utils.asObjectOrNull(s.value, str)
                    if (lang is not None and l_ == 0): 
                        if (lang.is_ru != LanguageHelper.isCyrillic(val)): 
                            continue
                    nam = val
                    break
            if (nam is not None): 
                break
        if (nam is None): 
            nam = self.getStringValue(UnitReferent.ATTR_NAME)
        pow0_ = self.getStringValue(UnitReferent.ATTR_POW)
        if (Utils.isNullOrEmpty(pow0_) or lev > 0): 
            return Utils.ifNotNull(nam, "?")
        res = ("{0}{1}".format(nam, pow0_) if (pow0_[0] != '-') else "{0}<{1}>".format(nam, pow0_))
        if (not short_variant and self.is_unknown): 
            res = ("(?)" + res)
        return res
    
    @property
    def is_unknown(self) -> bool:
        """ Признак того, что это неизвестная метрика """
        return self.getStringValue(UnitReferent.ATTR_UNKNOWN) == "true"
    @is_unknown.setter
    def is_unknown(self, value) -> bool:
        self.addSlot(UnitReferent.ATTR_UNKNOWN, ("true" if value else None), True, 0)
        return value
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        ur = Utils.asObjectOrNull(obj, UnitReferent)
        if (ur is None): 
            return False
        for s in self.slots: 
            if (ur.findSlot(s.type_name, s.value, True) is None): 
                return False
        for s in ur.slots: 
            if (self.findSlot(s.type_name, s.value, True) is None): 
                return False
        return True