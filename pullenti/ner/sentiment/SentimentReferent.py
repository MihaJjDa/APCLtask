﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.sentiment.SentimentKind import SentimentKind
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.sentiment.internal.MetaSentiment import MetaSentiment
from pullenti.ner.Referent import Referent

class SentimentReferent(Referent):
    """ Фрагмент, соответсвующий сентиментной оценке """
    
    def __init__(self) -> None:
        super().__init__(SentimentReferent.OBJ_TYPENAME)
        self.instance_of = MetaSentiment._global_meta
    
    OBJ_TYPENAME = "SENTIMENT"
    
    ATTR_KIND = "KIND"
    
    ATTR_COEF = "COEF"
    
    ATTR_REF = "REF"
    
    ATTR_SPELLING = "SPELLING"
    
    def toString(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        print(MetaSentiment.FTYP.convertInnerValueToOuterValue(self.getStringValue(SentimentReferent.ATTR_KIND), lang), end="", file=res)
        print(" {0}".format(Utils.ifNotNull(self.spelling, "")), end="", file=res, flush=True)
        if (self.coef > 0): 
            print(" (coef={0})".format(self.coef), end="", file=res, flush=True)
        r = self.getSlotValue(SentimentReferent.ATTR_REF)
        if (r is not None and not short_variant): 
            print(" -> {0}".format(r), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def kind(self) -> 'SentimentKind':
        s = self.getStringValue(SentimentReferent.ATTR_KIND)
        if (s is None): 
            return SentimentKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, SentimentKind)
            if (isinstance(res, SentimentKind)): 
                return Utils.valToEnum(res, SentimentKind)
        except Exception as ex2497: 
            pass
        return SentimentKind.UNDEFINED
    @kind.setter
    def kind(self, value) -> 'SentimentKind':
        if (value != SentimentKind.UNDEFINED): 
            self.addSlot(SentimentReferent.ATTR_KIND, Utils.enumToString(value), True, 0)
        return value
    
    @property
    def spelling(self) -> str:
        return self.getStringValue(SentimentReferent.ATTR_SPELLING)
    @spelling.setter
    def spelling(self, value) -> str:
        self.addSlot(SentimentReferent.ATTR_SPELLING, value, True, 0)
        return value
    
    @property
    def coef(self) -> int:
        val = self.getStringValue(SentimentReferent.ATTR_COEF)
        if (val is None): 
            return 0
        wrapi2498 = RefOutArgWrapper(0)
        inoutres2499 = Utils.tryParseInt(val, wrapi2498)
        i = wrapi2498.value
        if (not inoutres2499): 
            return 0
        return i
    @coef.setter
    def coef(self, value) -> int:
        self.addSlot(SentimentReferent.ATTR_COEF, str(value), True, 0)
        return value
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        sr = Utils.asObjectOrNull(obj, SentimentReferent)
        if (sr is None): 
            return False
        if (sr.kind != self.kind): 
            return False
        if (sr.spelling != self.spelling): 
            return False
        return True
    
    def canBeGeneralFor(self, obj : 'Referent') -> bool:
        return False
    
    def createOntologyItem(self) -> 'IntOntologyItem':
        oi = IntOntologyItem(self)
        oi.termins.append(Termin(self.spelling))
        return oi