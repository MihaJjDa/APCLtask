﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.person.internal.MetaPersonProperty import MetaPersonProperty
from pullenti.ner.geo.GeoReferent import GeoReferent

class PersonPropertyReferent(Referent):
    """ Сущность, описывающая некоторое свойство физического лица """
    
    def __init__(self) -> None:
        super().__init__(PersonPropertyReferent.OBJ_TYPENAME)
        self.instance_of = MetaPersonProperty._global_meta
    
    OBJ_TYPENAME = "PERSONPROPERTY"
    
    ATTR_NAME = "NAME"
    
    ATTR_ATTR = "ATTR"
    
    ATTR_REF = "REF"
    
    ATTR_HIGHER = "HIGHER"
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        if (self.name is not None): 
            print(self.name, end="", file=res)
        for r in self.slots: 
            if (r.type_name == PersonPropertyReferent.ATTR_ATTR and r.value is not None): 
                print(", {0}".format(str(r.value)), end="", file=res, flush=True)
        for r in self.slots: 
            if (r.type_name == PersonPropertyReferent.ATTR_REF and (isinstance(r.value, Referent)) and (lev < 10)): 
                print("; {0}".format((r.value).toString(short_variant, lang, lev + 1)), end="", file=res, flush=True)
        hi = self.higher
        if (hi is not None and hi != self and self.__checkCorrectHigher(hi, 0)): 
            print("; {0}".format(hi.toString(short_variant, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def getCompareStrings(self) -> typing.List[str]:
        res = list()
        for s in self.slots: 
            if (s.type_name == PersonPropertyReferent.ATTR_NAME): 
                res.append(str(s.value))
        if (len(res) > 0): 
            return res
        else: 
            return super().getCompareStrings()
    
    @property
    def name(self) -> str:
        """ Наименование """
        return self.getStringValue(PersonPropertyReferent.ATTR_NAME)
    @name.setter
    def name(self, value) -> str:
        self.addSlot(PersonPropertyReferent.ATTR_NAME, value, True, 0)
        return value
    
    @property
    def higher(self) -> 'PersonPropertyReferent':
        """ Вышестоящая должность """
        return self.__getHigher(0)
    @higher.setter
    def higher(self, value) -> 'PersonPropertyReferent':
        if (self.__checkCorrectHigher(value, 0)): 
            self.addSlot(PersonPropertyReferent.ATTR_HIGHER, value, True, 0)
        return value
    
    def __getHigher(self, lev : int) -> 'PersonPropertyReferent':
        hi = Utils.asObjectOrNull(self.getSlotValue(PersonPropertyReferent.ATTR_HIGHER), PersonPropertyReferent)
        if (hi is None): 
            return None
        if (not self.__checkCorrectHigher(hi, lev + 1)): 
            return None
        return hi
    
    def __checkCorrectHigher(self, hi : 'PersonPropertyReferent', lev : int) -> bool:
        if (hi is None): 
            return True
        if (hi == self): 
            return False
        if (lev > 20): 
            return False
        hii = hi.__getHigher(lev + 1)
        if (hii is None): 
            return True
        if (hii == self): 
            return False
        li = list()
        li.append(self)
        pr = hi
        while pr is not None: 
            if (pr in li): 
                return False
            else: 
                li.append(pr)
            pr = pr.__getHigher(lev + 1)
        return True
    
    @property
    def parent_referent(self) -> 'Referent':
        return self.higher
    
    __m_bosses0 = None
    
    __m_bosses1 = None
    
    __tmp_stack = 0
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType') -> bool:
        pr = Utils.asObjectOrNull(obj, PersonPropertyReferent)
        if (pr is None): 
            return False
        n1 = self.name
        n2 = pr.name
        if (n1 is None or n2 is None): 
            return False
        eq_bosses = False
        if (n1 != n2): 
            if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                return False
            if (n1 in PersonPropertyReferent.__m_bosses0 and n2 in PersonPropertyReferent.__m_bosses1): 
                eq_bosses = True
            elif (n1 in PersonPropertyReferent.__m_bosses1 and n2 in PersonPropertyReferent.__m_bosses0): 
                eq_bosses = True
            else: 
                if (not n1.startswith(n2 + " ") and not n2.startswith(n1 + " ")): 
                    return False
                eq_bosses = True
            hi = self.higher
            while hi is not None: 
                PersonPropertyReferent.__tmp_stack += 1
                if ((PersonPropertyReferent.__tmp_stack) > 20): 
                    pass
                elif (hi.canBeEquals(pr, typ)): 
                    PersonPropertyReferent.__tmp_stack -= 1
                    return False
                PersonPropertyReferent.__tmp_stack -= 1
                hi = hi.higher
            hi = pr.higher
            while hi is not None: 
                PersonPropertyReferent.__tmp_stack += 1
                if ((PersonPropertyReferent.__tmp_stack) > 20): 
                    pass
                elif (hi.canBeEquals(self, typ)): 
                    PersonPropertyReferent.__tmp_stack -= 1
                    return False
                PersonPropertyReferent.__tmp_stack -= 1
                hi = hi.higher
        if (self.higher is not None and pr.higher is not None): 
            PersonPropertyReferent.__tmp_stack += 1
            if ((PersonPropertyReferent.__tmp_stack) > 20): 
                pass
            elif (not self.higher.canBeEquals(pr.higher, typ)): 
                PersonPropertyReferent.__tmp_stack -= 1
                return False
            PersonPropertyReferent.__tmp_stack -= 1
        if (self.findSlot("@GENERAL", None, True) is not None or pr.findSlot("@GENERAL", None, True) is not None): 
            return str(self) == str(pr)
        if (self.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is not None or pr.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is not None): 
            refs1 = list()
            refs2 = list()
            for s in self.slots: 
                if (s.type_name == PersonPropertyReferent.ATTR_REF): 
                    refs1.append(s.value)
            for s in pr.slots: 
                if (s.type_name == PersonPropertyReferent.ATTR_REF): 
                    refs2.append(s.value)
            eq = False
            noeq = False
            i = 0
            first_pass3113 = True
            while True:
                if first_pass3113: first_pass3113 = False
                else: i += 1
                if (not (i < len(refs1))): break
                if (refs1[i] in refs2): 
                    eq = True
                    continue
                noeq = True
                if (isinstance(refs1[i], Referent)): 
                    for rr in refs2: 
                        if (isinstance(rr, Referent)): 
                            if ((rr).canBeEquals(Utils.asObjectOrNull(refs1[i], Referent), typ)): 
                                noeq = False
                                eq = True
                                break
            i = 0
            first_pass3114 = True
            while True:
                if first_pass3114: first_pass3114 = False
                else: i += 1
                if (not (i < len(refs2))): break
                if (refs2[i] in refs1): 
                    eq = True
                    continue
                noeq = True
                if (isinstance(refs2[i], Referent)): 
                    for rr in refs1: 
                        if (isinstance(rr, Referent)): 
                            if ((rr).canBeEquals(Utils.asObjectOrNull(refs2[i], Referent), typ)): 
                                noeq = False
                                eq = True
                                break
            if (eq and not noeq): 
                pass
            elif (noeq and ((eq or len(refs1) == 0 or len(refs2) == 0))): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS or n1 != n2): 
                    return False
                if (self.higher is not None or pr.higher is not None): 
                    return False
            else: 
                return False
        elif (not eq_bosses and n1 != n2): 
            return False
        return True
    
    def canBeGeneralFor(self, obj : 'Referent') -> bool:
        pr = Utils.asObjectOrNull(obj, PersonPropertyReferent)
        if (pr is None): 
            return False
        n1 = self.name
        n2 = pr.name
        if (n1 is None or n2 is None): 
            return False
        if (self.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is not None or self.higher is not None): 
            if (n1 != n2 and n1.startswith(n2)): 
                return self.canBeEquals(obj, Referent.EqualType.DIFFERENTTEXTS)
            return False
        if (n1 == n2): 
            if (pr.findSlot(PersonPropertyReferent.ATTR_REF, None, True) is not None or pr.higher is not None): 
                return True
            return False
        if (n2.startswith(n1)): 
            if (n2.startswith(n1 + " ")): 
                return self.canBeEquals(obj, Referent.EqualType.WITHINONETEXT)
        return False
    
    @property
    def kind(self) -> 'PersonPropertyKind':
        from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken
        return PersonAttrToken.checkKind(self)
    
    def createOntologyItem(self) -> 'IntOntologyItem':
        oi = IntOntologyItem(self)
        for a in self.slots: 
            if (a.type_name == PersonPropertyReferent.ATTR_NAME): 
                oi.termins.append(Termin(str(a.value)))
        return oi
    
    def mergeSlots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        nam = self.name
        nam1 = (obj).name
        super().mergeSlots(obj, merge_statistic)
        if (nam != nam1 and nam1 is not None and nam is not None): 
            s = None
            if (nam.startswith(nam1)): 
                s = self.findSlot(PersonPropertyReferent.ATTR_NAME, nam1, True)
            elif (nam1.startswith(nam)): 
                s = self.findSlot(PersonPropertyReferent.ATTR_NAME, nam, True)
            elif (nam in PersonPropertyReferent.__m_bosses0 and nam1 in PersonPropertyReferent.__m_bosses1): 
                s = self.findSlot(PersonPropertyReferent.ATTR_NAME, nam, True)
            elif (nam1 in PersonPropertyReferent.__m_bosses0 and nam in PersonPropertyReferent.__m_bosses1): 
                s = self.findSlot(PersonPropertyReferent.ATTR_NAME, nam1, True)
            if (s is not None): 
                self.slots.remove(s)
    
    def canHasRef(self, r : 'Referent') -> bool:
        """ Проверка, что этот референт может выступать в качестве ATTR_REF
        
        Args:
            r(Referent): 
        
        """
        nam = self.name
        if (nam is None or r is None): 
            return False
        if (isinstance(r, GeoReferent)): 
            g = Utils.asObjectOrNull(r, GeoReferent)
            if (LanguageHelper.endsWithEx(nam, "президент", "губернатор", None, None)): 
                return g.is_state or g.is_region
            if (nam == "мэр" or nam == "градоначальник"): 
                return g.is_city
            if (nam == "глава"): 
                return True
            return False
        if (r.type_name == "ORGANIZATION"): 
            if ((LanguageHelper.endsWith(nam, "губернатор") or nam == "мэр" or nam == "градоначальник") or nam == "президент"): 
                return False
            if ("министр" in nam): 
                if (r.findSlot(None, "министерство", True) is None): 
                    return False
            if (nam.endswith("директор")): 
                if ((r.findSlot(None, "суд", True)) is not None): 
                    return False
            return True
        return False
    
    @staticmethod
    def _new2291(_arg1 : str) -> 'PersonPropertyReferent':
        res = PersonPropertyReferent()
        res.name = _arg1
        return res
    
    # static constructor for class PersonPropertyReferent
    @staticmethod
    def _static_ctor():
        PersonPropertyReferent.__m_bosses0 = list(["глава", "руководитель"])
        PersonPropertyReferent.__m_bosses1 = list(["президент", "генеральный директор", "директор", "председатель"])

PersonPropertyReferent._static_ctor()