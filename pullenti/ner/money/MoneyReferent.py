﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.money.internal.MoneyMeta import MoneyMeta

class MoneyReferent(Referent):
    """ Представление денежных сумм """
    
    def __init__(self) -> None:
        super().__init__(MoneyReferent.OBJ_TYPENAME)
        self.instance_of = MoneyMeta.GLOBAL_META
    
    OBJ_TYPENAME = "MONEY"
    
    ATTR_CURRENCY = "CURRENCY"
    
    ATTR_VALUE = "VALUE"
    
    ATTR_ALTVALUE = "ALTVALUE"
    
    ATTR_REST = "REST"
    
    ATTR_ALTREST = "ALTREST"
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        v = self.getStringValue(MoneyReferent.ATTR_VALUE)
        r = self.rest
        if (v is not None or r > 0): 
            print(Utils.ifNotNull(v, "0"), end="", file=res)
            cou = 0
            for i in range(res.tell() - 1, 0, -1):
                cou += 1
                if ((cou) == 3): 
                    Utils.insertStringIO(res, i, '.')
                    cou = 0
        else: 
            print("?", end="", file=res)
        if (r > 0): 
            print(",{0}".format("{:02d}".format(r)), end="", file=res, flush=True)
        print(" {0}".format(self.currency), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def currency(self) -> str:
        """ Тип валюты (3-х значный код ISO 4217) """
        return self.getStringValue(MoneyReferent.ATTR_CURRENCY)
    @currency.setter
    def currency(self, value_) -> str:
        self.addSlot(MoneyReferent.ATTR_CURRENCY, value_, True, 0)
        return value_
    
    @property
    def value(self) -> float:
        """ Значение """
        val = self.getStringValue(MoneyReferent.ATTR_VALUE)
        if (val is None): 
            return 0
        wrapv1627 = RefOutArgWrapper(0)
        inoutres1628 = Utils.tryParseFloat(val, wrapv1627)
        v = wrapv1627.value
        if (not inoutres1628): 
            return 0
        return v
    
    @property
    def alt_value(self) -> float:
        """ Альтернативное значение (если есть, то значит неправильно написали сумму
         числом и далее прописью в скобках) """
        val = self.getStringValue(MoneyReferent.ATTR_ALTVALUE)
        if (val is None): 
            return None
        wrapv1629 = RefOutArgWrapper(0)
        inoutres1630 = Utils.tryParseFloat(val, wrapv1629)
        v = wrapv1629.value
        if (not inoutres1630): 
            return None
        return v
    
    @property
    def rest(self) -> int:
        """ Остаток (от 0 до 99) - копеек, центов и т.п. """
        val = self.getStringValue(MoneyReferent.ATTR_REST)
        if (val is None): 
            return 0
        wrapv1631 = RefOutArgWrapper(0)
        inoutres1632 = Utils.tryParseInt(val, wrapv1631)
        v = wrapv1631.value
        if (not inoutres1632): 
            return 0
        return v
    
    @property
    def alt_rest(self) -> int:
        """ Остаток (от 0 до 99) - копеек, центов и т.п. """
        val = self.getStringValue(MoneyReferent.ATTR_ALTREST)
        if (val is None): 
            return None
        wrapv1633 = RefOutArgWrapper(0)
        inoutres1634 = Utils.tryParseInt(val, wrapv1633)
        v = wrapv1633.value
        if (not inoutres1634): 
            return None
        return v
    
    @property
    def real_value(self) -> float:
        """ Действительное значение (вместе с копейками) """
        return (self.value) + (((self.rest) / (100)))
    @real_value.setter
    def real_value(self, value_) -> float:
        val = NumberHelper.doubleToString(value_)
        ii = val.find('.')
        if (ii > 0): 
            val = val[0:0+ii]
        self.addSlot(MoneyReferent.ATTR_VALUE, val, True, 0)
        re = ((value_ - self.value)) * (100)
        self.addSlot(MoneyReferent.ATTR_REST, str((math.floor((re + .0001)))), True, 0)
        return value_
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        s = Utils.asObjectOrNull(obj, MoneyReferent)
        if (s is None): 
            return False
        if (s.currency != self.currency): 
            return False
        if (s.value != self.value): 
            return False
        if (s.rest != self.rest): 
            return False
        if (s.alt_value != self.alt_value): 
            return False
        if (s.alt_rest != self.alt_rest): 
            return False
        return True
    
    @staticmethod
    def _new811(_arg1 : str, _arg2 : float) -> 'MoneyReferent':
        res = MoneyReferent()
        res.currency = _arg1
        res.real_value = _arg2
        return res