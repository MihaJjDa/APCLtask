﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
import datetime
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Referent import Referent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.core.Termin import Termin
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.ner.decree.internal.MetaDecree import MetaDecree
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.date.DateRangeReferent import DateRangeReferent
from pullenti.ner.decree.internal.DecreeToken import DecreeToken

class DecreeReferent(Referent):
    """ Сущность, представляющая ссылку на НПА """
    
    def __init__(self) -> None:
        super().__init__(DecreeReferent.OBJ_TYPENAME)
        self.instance_of = MetaDecree.GLOBAL_META
    
    OBJ_TYPENAME = "DECREE"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_NAME = "NAME"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_DATE = "DATE"
    
    ATTR_SOURCE = "SOURCE"
    
    ATTR_GEO = "GEO"
    
    ATTR_READING = "READING"
    
    ATTR_CASENUMBER = "CASENUMBER"
    
    ATTR_EDITION = "EDITION"
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        ki = self.kind
        out_part = False
        nam = self.name
        if (self.typ is not None): 
            if ((nam is not None and not nam.startswith("О") and self.typ in nam) and ki != DecreeKind.STANDARD): 
                print(MiscHelper.convertFirstCharUpperAndOtherLower(nam), end="", file=res)
                nam = (None)
            elif (ki == DecreeKind.STANDARD and (len(self.typ) < 6)): 
                print(self.typ, end="", file=res)
            else: 
                print(MiscHelper.convertFirstCharUpperAndOtherLower(self.typ), end="", file=res)
        else: 
            print("?", end="", file=res)
        out_src = True
        if (ki == DecreeKind.CONTRACT and self.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
            srcs = list()
            for s in self.slots: 
                if (s.type_name == DecreeReferent.ATTR_SOURCE): 
                    srcs.append(str(s.value))
            if (len(srcs) > 1): 
                ii = 0
                while ii < len(srcs): 
                    if (ii > 0 and ((ii + 1) < len(srcs))): 
                        print(", ", end="", file=res)
                    elif (ii > 0): 
                        print(" и ", end="", file=res)
                    else: 
                        print(" между ", end="", file=res)
                    print(srcs[ii], end="", file=res)
                    out_src = False
                    ii += 1
        num = self.number
        if (num is not None): 
            print(" № {0}".format(num), end="", file=res, flush=True)
            for s in self.slots: 
                if (s.type_name == DecreeReferent.ATTR_NUMBER): 
                    nn = str(s.value)
                    if (nn != num): 
                        print("/{0}".format(nn), end="", file=res, flush=True)
        num = self.case_number
        if ((num) is not None): 
            print(" по делу № {0}".format(num), end="", file=res, flush=True)
        if (self.getStringValue(DecreeReferent.ATTR_DATE) is not None): 
            print(" {0}{1}".format(("" if ki == DecreeKind.PROGRAM else "от "), self.getStringValue(DecreeReferent.ATTR_DATE)), end="", file=res, flush=True)
        if (out_src and self.getSlotValue(DecreeReferent.ATTR_SOURCE) is not None): 
            print("; {0}".format(self.getStringValue(DecreeReferent.ATTR_SOURCE)), end="", file=res, flush=True)
        if (not short_variant): 
            s = self.getStringValue(DecreeReferent.ATTR_GEO)
            if (s is not None): 
                print("; {0}".format(s), end="", file=res, flush=True)
            if (nam is not None): 
                s = self.__getShortName()
                if (s is not None): 
                    print("; \"{0}\"".format(s), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    @property
    def name(self) -> str:
        """ Наименование (если несколько, то самое короткое) """
        nam = None
        for s in self.slots: 
            if (s.type_name == DecreeReferent.ATTR_NAME): 
                n = str(s.value)
                if (nam is None or len(nam) > len(n)): 
                    nam = n
        return nam
    
    def __getShortName(self) -> str:
        nam = self.name
        if (nam is None): 
            return None
        if (len(nam) > 100): 
            i = 100
            while i < len(nam): 
                if (not str.isalpha(nam[i])): 
                    break
                i += 1
            if (i < len(nam)): 
                nam = (nam[0:0+i] + "...")
        return MiscHelper.convertFirstCharUpperAndOtherLower(nam)
    
    def getCompareStrings(self) -> typing.List[str]:
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeReferent.ATTR_NAME or s.type_name == DecreeReferent.ATTR_NUMBER): 
                res.append(str(s.value))
        if (len(res) == 0 and self.typ is not None): 
            for s in self.slots: 
                if (s.type_name == DecreeReferent.ATTR_GEO): 
                    res.append("{0} {1}".format(self.typ, str(s.value)))
        if (self.typ == "КОНСТИТУЦИЯ"): 
            res.append(self.typ)
        if (len(res) > 0): 
            return res
        else: 
            return super().getCompareStrings()
    
    @property
    def date(self) -> datetime.datetime:
        """ Дата подписания (для законов дат может быть много - по редакциям) """
        from pullenti.ner.decree.internal.DecreeHelper import DecreeHelper
        s = self.getStringValue(DecreeReferent.ATTR_DATE)
        if (s is None): 
            return None
        return DecreeHelper.parseDateTime(s)
    
    def _addDate(self, dt : 'DecreeToken') -> bool:
        if (dt is None): 
            return False
        if (dt.ref is not None and (isinstance(dt.ref.referent, DateReferent))): 
            dr = Utils.asObjectOrNull(dt.ref.referent, DateReferent)
            year = dr.year
            mon = dr.month
            day = dr.day
            if (year == 0): 
                return False
            tmp = io.StringIO()
            print(year, end="", file=tmp)
            if (mon > 0): 
                print(".{0}".format("{:02d}".format(mon)), end="", file=tmp, flush=True)
            if (day > 0): 
                print(".{0}".format("{:02d}".format(day)), end="", file=tmp, flush=True)
            self.addSlot(DecreeReferent.ATTR_DATE, Utils.toStringStringIO(tmp), False, 0)
            return True
        if (dt.ref is not None and (isinstance(dt.ref.referent, DateRangeReferent))): 
            self.addSlot(DecreeReferent.ATTR_DATE, dt.ref.referent, False, 0)
            return True
        if (dt.value is not None): 
            self.addSlot(DecreeReferent.ATTR_DATE, dt.value, False, 0)
            return True
        return False
    
    def __allYears(self) -> typing.List[int]:
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeReferent.ATTR_DATE): 
                str0_ = str(s.value)
                i = str0_.find('.')
                if (i == 4): 
                    str0_ = str0_[0:0+4]
                wrapi1084 = RefOutArgWrapper(0)
                inoutres1085 = Utils.tryParseInt(str0_, wrapi1084)
                i = wrapi1084.value
                if (inoutres1085): 
                    res.append(i)
        return res
    
    @property
    def typ(self) -> str:
        """ Тип """
        return self.getStringValue(DecreeReferent.ATTR_TYPE)
    @typ.setter
    def typ(self, value) -> str:
        self.addSlot(DecreeReferent.ATTR_TYPE, value, True, 0)
        return value
    
    @property
    def kind(self) -> 'DecreeKind':
        return DecreeToken.getKind(self.typ)
    
    @property
    def is_law(self) -> bool:
        """ Признак того, что это именно закон, а не подзаконный акт.
         Для законов возможны несколько номеров и дат (редакций) """
        return DecreeToken.isLaw(self.typ)
    
    @property
    def typ0(self) -> str:
        typ_ = self.typ
        if (typ_ is None): 
            return None
        i = typ_.rfind(' ')
        if (i < 0): 
            return typ_
        if (typ_.startswith("ПАСПОРТ")): 
            return "ПАСПОРТ"
        if (typ_.startswith("ОСНОВЫ") or typ_.startswith("ОСНОВИ")): 
            i = typ_.find(' ')
            return typ_[0:0+i]
        return typ_[i + 1:]
    
    @property
    def number(self) -> str:
        """ Номер (для законов номеров может быть много) """
        return self.getStringValue(DecreeReferent.ATTR_NUMBER)
    
    @property
    def case_number(self) -> str:
        return self.getStringValue(DecreeReferent.ATTR_CASENUMBER)
    
    def addSlot(self, attr_name : str, attr_value : object, clear_old_value : bool, stat_count : int=0) -> 'Slot':
        from pullenti.ner.decree.internal.PartToken import PartToken
        if (isinstance(attr_value, PartToken.PartValue)): 
            attr_value = ((attr_value).value)
        s = super().addSlot(attr_name, attr_value, clear_old_value, stat_count)
        if (isinstance(attr_value, PartToken.PartValue)): 
            s.tag = (attr_value).source_value
        return s
    
    def _addNumber(self, dt : 'DecreeToken') -> None:
        if (dt.typ == DecreeToken.ItemType.NUMBER): 
            if (dt.num_year > 0): 
                self.addSlot(DecreeReferent.ATTR_DATE, str(dt.num_year), False, 0)
        if (Utils.isNullOrEmpty(dt.value)): 
            return
        value = dt.value
        if (".,".find(value[len(value) - 1]) >= 0): 
            value = value[0:0+len(value) - 1]
        self.addSlot(DecreeReferent.ATTR_NUMBER, value, False, 0)
    
    def _addName(self, dr : 'DecreeReferent') -> None:
        s = dr.findSlot(DecreeReferent.ATTR_NAME, None, True)
        if (s is None): 
            return
        ss = self.addSlot(DecreeReferent.ATTR_NAME, s.value, False, 0)
        if (ss is not None and ss.tag is None): 
            ss.tag = s.tag
    
    def _addNameStr(self, name_ : str) -> None:
        if (name_ is None or len(name_) == 0): 
            return
        if (name_[len(name_) - 1] == '.'): 
            if (len(name_) > 5 and str.isalpha(name_[len(name_) - 2]) and not str.isalpha(name_[len(name_) - 3])): 
                pass
            else: 
                name_ = name_[0:0+len(name_) - 1]
        name_ = name_.strip()
        uname = name_.upper()
        s = self.addSlot(DecreeReferent.ATTR_NAME, uname, False, 0)
        if (uname != name_): 
            s.tag = name_
    
    def __getNumberDigits(self, num : str) -> str:
        if (num is None): 
            return ""
        tmp = io.StringIO()
        i = 0
        while i < len(num): 
            if (str.isdigit(num[i])): 
                if (num[i] == '0' and tmp.tell() == 0): 
                    pass
                elif (num[i] == '3' and tmp.tell() > 0 and num[i - 1] == 'Ф'): 
                    pass
                else: 
                    print(num[i], end="", file=tmp)
            i += 1
        return Utils.toStringStringIO(tmp)
    
    def __allNumberDigits(self) -> typing.List[str]:
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeReferent.ATTR_NUMBER): 
                res.append(self.__getNumberDigits(Utils.asObjectOrNull(s.value, str)))
        return res
    
    def __allDates(self) -> typing.List[datetime.datetime]:
        from pullenti.ner.decree.internal.DecreeHelper import DecreeHelper
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeReferent.ATTR_DATE): 
                dt = DecreeHelper.parseDateTime(Utils.asObjectOrNull(s.value, str))
                if (dt is not None): 
                    res.append(dt)
        return res
    
    def canBeEquals(self, obj : 'Referent', typ_ : 'EqualType') -> bool:
        b = self.__CanBeEquals(obj, typ_, False)
        return b
    
    def __CanBeEquals(self, obj : 'Referent', typ_ : 'EqualType', ignore_geo : bool) -> bool:
        dr = Utils.asObjectOrNull(obj, DecreeReferent)
        if (dr is None): 
            return False
        if (dr.typ0 is not None and self.typ0 is not None): 
            if (dr.typ0 != self.typ0): 
                return False
        num_eq = 0
        if (self.number is not None or dr.number is not None): 
            if (self.number is not None and dr.number is not None): 
                di1 = self.__allNumberDigits()
                di2 = dr.__allNumberDigits()
                for d1 in di1: 
                    if (d1 in di2): 
                        num_eq = 1
                        break
                if (num_eq == 0 and not self.is_law): 
                    return False
                for s in self.slots: 
                    if (s.type_name == DecreeReferent.ATTR_NUMBER): 
                        if (dr.findSlot(s.type_name, s.value, True) is not None): 
                            num_eq = 2
                            break
                if (num_eq == 0): 
                    return False
        if (self.case_number is not None and dr.case_number is not None): 
            if (self.case_number != dr.case_number): 
                return False
        if (self.findSlot(DecreeReferent.ATTR_GEO, None, True) is not None and dr.findSlot(DecreeReferent.ATTR_GEO, None, True) is not None): 
            if (self.getStringValue(DecreeReferent.ATTR_GEO) != dr.getStringValue(DecreeReferent.ATTR_GEO)): 
                return False
        src_eq = False
        src_not_eq = False
        src = self.findSlot(DecreeReferent.ATTR_SOURCE, None, True)
        if (src is not None and dr.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
            if (dr.findSlot(src.type_name, src.value, True) is None): 
                src_not_eq = True
            else: 
                src_eq = True
        date_not_eq = False
        date_is_equ = False
        years_is_equ = False
        date1 = self.getStringValue(DecreeReferent.ATTR_DATE)
        date2 = dr.getStringValue(DecreeReferent.ATTR_DATE)
        if (date1 is not None or date2 is not None): 
            if (self.is_law): 
                ys1 = self.__allYears()
                ys2 = dr.__allYears()
                for y1 in ys1: 
                    if (y1 in ys2): 
                        years_is_equ = True
                        break
                if (years_is_equ): 
                    dts1 = self.__allDates()
                    dts2 = dr.__allDates()
                    for d1 in dts1: 
                        if (d1 in dts2): 
                            date_is_equ = True
                            break
                if (not date_is_equ): 
                    if (self.typ == "КОНСТИТУЦИЯ"): 
                        return False
                    if (self.date is not None and dr.date is not None): 
                        date_not_eq = True
            elif (date1 == date2 or ((self.date is not None and dr.date is not None and self.date == dr.date))): 
                if (num_eq > 1): 
                    return True
                date_is_equ = True
            elif (self.date is not None and dr.date is not None): 
                if (self.date.year != dr.date.year): 
                    return False
                if (num_eq >= 1): 
                    if (src_eq): 
                        return True
                    if (src_not_eq): 
                        return False
                else: 
                    return False
            elif (typ_ == Referent.EqualType.DIFFERENTTEXTS or self.kind == DecreeKind.PUBLISHER): 
                date_not_eq = True
        if (self.findSlot(DecreeReferent.ATTR_NAME, None, True) is not None and dr.findSlot(DecreeReferent.ATTR_NAME, None, True) is not None): 
            for s in self.slots: 
                if (s.type_name == DecreeReferent.ATTR_NAME): 
                    if (dr.findSlot(s.type_name, s.value, True) is not None): 
                        return True
                    for ss in dr.slots: 
                        if (ss.type_name == s.type_name): 
                            n0 = str(s.value)
                            n1 = str(ss.value)
                            if (n0.startswith(n1) or n1.startswith(n0)): 
                                return True
            if (date_not_eq): 
                return False
            if (self.is_law and not date_is_equ): 
                return False
            if (num_eq > 0): 
                if (src_eq): 
                    return True
                if (src_not_eq and typ_ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
                elif ((not src_not_eq and num_eq > 1 and self.date is None) and dr.date is None): 
                    return True
                return False
        elif (self.is_law and date_not_eq): 
            return False
        if (date_not_eq): 
            return False
        ty = self.typ
        if (ty is None): 
            return num_eq > 0
        t = DecreeToken.getKind(ty)
        if (t == DecreeKind.USTAV or ty == "КОНСТИТУЦИЯ"): 
            return True
        if (num_eq > 0): 
            return True
        if (str(self) == str(obj)): 
            return True
        return False
    
    def canBeGeneralFor(self, obj : 'Referent') -> bool:
        if (not self.__CanBeEquals(obj, Referent.EqualType.WITHINONETEXT, True)): 
            return False
        g1 = Utils.asObjectOrNull(self.getSlotValue(DecreeReferent.ATTR_GEO), GeoReferent)
        g2 = Utils.asObjectOrNull(obj.getSlotValue(DecreeReferent.ATTR_GEO), GeoReferent)
        if (g1 is None and g2 is not None): 
            return True
        return False
    
    def _checkCorrection(self, noun_is_doubtful : bool) -> bool:
        typ_ = self.typ0
        if (typ_ is None): 
            return False
        if (typ_ == "КОНСТИТУЦИЯ" or typ_ == "КОНСТИТУЦІЯ"): 
            return True
        if (self.typ == "ЕДИНЫЙ ОТРАСЛЕВОЙ СТАНДАРТ ЗАКУПОК"): 
            return True
        if ((typ_ == "КОДЕКС" or typ_ == "ОСНОВЫ ЗАКОНОДАТЕЛЬСТВА" or typ_ == "ПРОГРАММА") or typ_ == "ОСНОВИ ЗАКОНОДАВСТВА" or typ_ == "ПРОГРАМА"): 
            if (self.findSlot(DecreeReferent.ATTR_NAME, None, True) is None): 
                return False
            if (self.findSlot(DecreeReferent.ATTR_GEO, None, True) is not None): 
                return True
            return not noun_is_doubtful
        if (typ_.startswith("ОСНОВ")): 
            if (self.findSlot(DecreeReferent.ATTR_GEO, None, True) is not None): 
                return True
            return False
        if ("ЗАКОН" in typ_): 
            if (self.findSlot(DecreeReferent.ATTR_NAME, None, True) is None and self.number is None): 
                return False
            return True
        if (((("ОПРЕДЕЛЕНИЕ" in typ_ or "РЕШЕНИЕ" in typ_ or "ПОСТАНОВЛЕНИЕ" in typ_) or "ПРИГОВОР" in typ_ or "ВИЗНАЧЕННЯ" in typ_) or "РІШЕННЯ" in typ_ or "ПОСТАНОВА" in typ_) or "ВИРОК" in typ_): 
            if (self.number is not None): 
                if (self.findSlot(DecreeReferent.ATTR_DATE, None, True) is not None or self.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is not None or self.findSlot(DecreeReferent.ATTR_NAME, None, True) is not None): 
                    return True
            elif (self.findSlot(DecreeReferent.ATTR_DATE, None, True) is not None and self.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
                return True
            return False
        ty = DecreeToken.getKind(typ_)
        if (ty == DecreeKind.USTAV): 
            if (self.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is not None): 
                return True
        if (ty == DecreeKind.KONVENTION): 
            if (self.findSlot(DecreeReferent.ATTR_NAME, None, True) is not None): 
                if (typ_ != "ДОГОВОР" and typ_ != "ДОГОВІР"): 
                    return True
        if (ty == DecreeKind.STANDARD): 
            if (self.number is not None and len(self.number) > 4): 
                return True
        if (self.number is None): 
            if (self.findSlot(DecreeReferent.ATTR_NAME, None, True) is None or self.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is None or self.findSlot(DecreeReferent.ATTR_DATE, None, True) is None): 
                if (ty == DecreeKind.CONTRACT and self.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is not None and self.findSlot(DecreeReferent.ATTR_DATE, None, True) is not None): 
                    pass
                elif (self.findSlot(DecreeReferent.ATTR_NAME, "ПРАВИЛА ДОРОЖНОГО ДВИЖЕНИЯ", True) is not None): 
                    pass
                elif (self.findSlot(DecreeReferent.ATTR_NAME, "ПРАВИЛА ДОРОЖНЬОГО РУХУ", True) is not None): 
                    pass
                else: 
                    return False
        else: 
            if ((typ_ == "ПАСПОРТ" or typ_ == "ГОСТ" or typ_ == "ПБУ") or typ_ == "ФОРМА"): 
                return True
            if (self.findSlot(DecreeReferent.ATTR_SOURCE, None, True) is None and self.findSlot(DecreeReferent.ATTR_DATE, None, True) is None and self.findSlot(DecreeReferent.ATTR_NAME, None, True) is None): 
                return False
        return True
    
    def mergeSlots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().mergeSlots(obj, merge_statistic)
        i = 0
        while i < (len(self.slots) - 1): 
            j = i + 1
            while j < len(self.slots): 
                if (self.slots[i].type_name == self.slots[j].type_name and self.slots[i].value == self.slots[j].value): 
                    del self.slots[j]
                    j -= 1
                j += 1
            i += 1
        nums = self.getStringValues(DecreeReferent.ATTR_NUMBER)
        if (len(nums) > 1): 
            nums.sort()
            i = 0
            while i < (len(nums) - 1): 
                if (nums[i + 1].startswith(nums[i]) and len(nums[i + 1]) > len(nums[i]) and not str.isdigit(nums[i + 1][len(nums[i])])): 
                    s = self.findSlot(DecreeReferent.ATTR_NUMBER, nums[i], True)
                    if (s is not None): 
                        self.slots.remove(s)
                    del nums[i]
                    i -= 1
                i += 1
    
    def createOntologyItem(self) -> 'IntOntologyItem':
        oi = IntOntologyItem(self)
        vars0_ = list()
        for a in self.slots: 
            if (a.type_name == DecreeReferent.ATTR_NAME): 
                s = str(a.value)
                if (not s in vars0_): 
                    vars0_.append(s)
        if (self.number is not None): 
            for digs in self.__allNumberDigits(): 
                if (not digs in vars0_): 
                    vars0_.append(digs)
        for v in vars0_: 
            oi.termins.append(Termin(v))
        return oi
    
    @staticmethod
    def _new1068(_arg1 : str) -> 'DecreeReferent':
        res = DecreeReferent()
        res.typ = _arg1
        return res