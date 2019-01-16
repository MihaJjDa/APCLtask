﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.named.NamedEntityKind import NamedEntityKind
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.named.internal.MetaNamedEntity import MetaNamedEntity
from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.core.MiscHelper import MiscHelper

class NamedEntityReferent(Referent):
    """ Текоторые мелкие именованные сущности (планеты, памятники, здания, местоположения, планеты и пр.) """
    
    def __init__(self) -> None:
        super().__init__(NamedEntityReferent.OBJ_TYPENAME)
        self.instance_of = MetaNamedEntity.GLOBAL_META
    
    OBJ_TYPENAME = "NAMEDENTITY"
    
    ATTR_NAME = "NAME"
    
    ATTR_KIND = "KIND"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_REF = "REF"
    
    ATTR_MISC = "MISC"
    
    def toString(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        typ = self.getStringValue(NamedEntityReferent.ATTR_TYPE)
        if (typ is not None): 
            print(typ, end="", file=res)
        name = self.getStringValue(NamedEntityReferent.ATTR_NAME)
        if (name is not None): 
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            print(MiscHelper.convertFirstCharUpperAndOtherLower(name), end="", file=res)
        re = Utils.asObjectOrNull(self.getSlotValue(NamedEntityReferent.ATTR_REF), Referent)
        if (re is not None): 
            if (res.tell() > 0): 
                print("; ", end="", file=res)
            print(re.toString(short_variant, lang, lev + 1), end="", file=res)
        return Utils.toStringStringIO(res)
    
    @property
    def kind(self) -> 'NamedEntityKind':
        """ Класс сущности """
        str0_ = self.getStringValue(NamedEntityReferent.ATTR_KIND)
        if (str0_ is None): 
            return NamedEntityKind.UNDEFINED
        try: 
            return Utils.valToEnum(str0_, NamedEntityKind)
        except Exception as ex1643: 
            pass
        return NamedEntityKind.UNDEFINED
    @kind.setter
    def kind(self, value) -> 'NamedEntityKind':
        self.addSlot(NamedEntityReferent.ATTR_KIND, Utils.enumToString(value).lower(), True, 0)
        return value
    
    def toSortString(self) -> str:
        return Utils.enumToString(self.kind) + self.toString(True, MorphLang.UNKNOWN, 0)
    
    def getCompareStrings(self) -> typing.List[str]:
        res = list()
        for s in self.slots: 
            if (s.type_name == NamedEntityReferent.ATTR_NAME): 
                str0_ = str(s.value)
                if (not str0_ in res): 
                    res.append(str0_)
                if (str0_.find(' ') > 0 or str0_.find('-') > 0): 
                    str0_ = str0_.replace(" ", "").replace("-", "")
                    if (not str0_ in res): 
                        res.append(str0_)
        if (len(res) == 0): 
            for s in self.slots: 
                if (s.type_name == NamedEntityReferent.ATTR_TYPE): 
                    t = str(s.value)
                    if (not t in res): 
                        res.append(t)
        if (len(res) > 0): 
            return res
        else: 
            return super().getCompareStrings()
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType') -> bool:
        ent = Utils.asObjectOrNull(obj, NamedEntityReferent)
        if (ent is None): 
            return False
        if (ent.kind != self.kind): 
            return False
        names = self.getStringValues(NamedEntityReferent.ATTR_NAME)
        names2 = obj.getStringValues(NamedEntityReferent.ATTR_NAME)
        eq_names = False
        if ((names is not None and len(names) > 0 and names2 is not None) and len(names2) > 0): 
            for n in names: 
                if (n in names2): 
                    eq_names = True
            if (not eq_names): 
                return False
        typs = self.getStringValues(NamedEntityReferent.ATTR_TYPE)
        typs2 = obj.getStringValues(NamedEntityReferent.ATTR_TYPE)
        eq_typs = False
        if ((typs is not None and len(typs) > 0 and typs2 is not None) and len(typs2) > 0): 
            for ty in typs: 
                if (ty in typs2): 
                    eq_typs = True
            if (not eq_typs): 
                return False
        if (not eq_typs and not eq_names): 
            return False
        re1 = Utils.asObjectOrNull(self.getSlotValue(NamedEntityReferent.ATTR_REF), Referent)
        re2 = Utils.asObjectOrNull(obj.getSlotValue(NamedEntityReferent.ATTR_REF), Referent)
        if (re1 is not None and re2 is not None): 
            if (not re1.canBeEquals(re2, typ)): 
                return False
        elif (re1 is not None or re2 is not None): 
            pass
        return True
    
    def createOntologyItem(self) -> 'IntOntologyItem':
        """ Признак того, что была попытка привязаться к внешней онтологии """
        return self._CreateOntologyItem(2, False, False)
    
    def _CreateOntologyItem(self, min_len : int, only_names : bool=False, pure_names : bool=False) -> 'IntOntologyItem':
        oi = IntOntologyItem(self)
        vars0_ = list()
        typs = Utils.ifNotNull(self.getStringValues(NamedEntityReferent.ATTR_TYPE), list())
        for a in self.slots: 
            if (a.type_name == NamedEntityReferent.ATTR_NAME): 
                s = str(a.value).upper()
                if (not s in vars0_): 
                    vars0_.append(s)
                if (not pure_names): 
                    sp = 0
                    jj = 0
                    while jj < len(s): 
                        if (s[jj] == ' '): 
                            sp += 1
                        jj += 1
                    if (sp == 1): 
                        s = s.replace(" ", "")
                        if (not s in vars0_): 
                            vars0_.append(s)
        if (not only_names): 
            if (len(vars0_) == 0): 
                for t in typs: 
                    up = t.upper()
                    if (not up in vars0_): 
                        vars0_.append(up)
        max0_ = 20
        cou = 0
        for v in vars0_: 
            if (len(v) >= min_len): 
                oi.termins.append(Termin(v))
                cou += 1
                if ((cou) >= max0_): 
                    break
        if (len(oi.termins) == 0): 
            return None
        return oi
    
    @staticmethod
    def _new1642(_arg1 : 'NamedEntityKind') -> 'NamedEntityReferent':
        res = NamedEntityReferent()
        res.kind = _arg1
        return res