﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.mail.MailKind import MailKind
from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.mail.internal.MetaLetter import MetaLetter
from pullenti.ner.person.PersonReferent import PersonReferent

class MailReferent(Referent):
    """ Письмо (точнее, блок письма) """
    
    def __init__(self) -> None:
        super().__init__(MailReferent.OBJ_TYPENAME)
        self.instance_of = MetaLetter._global_meta
    
    OBJ_TYPENAME = "MAIL"
    
    ATTR_KIND = "TYPE"
    
    ATTR_TEXT = "TEXT"
    
    ATTR_REF = "REF"
    
    @property
    def kind(self) -> 'MailKind':
        """ Тип блока письма """
        val = self.getStringValue(MailReferent.ATTR_KIND)
        try: 
            if (val is not None): 
                return Utils.valToEnum(val, MailKind)
        except Exception as ex1503: 
            pass
        return MailKind.UNDEFINED
    @kind.setter
    def kind(self, value) -> 'MailKind':
        self.addSlot(MailReferent.ATTR_KIND, Utils.enumToString(value).upper(), True, 0)
        return value
    
    @property
    def text(self) -> str:
        return self.getStringValue(MailReferent.ATTR_TEXT)
    @text.setter
    def text(self, value) -> str:
        self.addSlot(MailReferent.ATTR_TEXT, value, True, 0)
        return value
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        print("{0}: ".format(Utils.enumToString(self.kind)), end="", file=res, flush=True)
        for s in self.slots: 
            if (s.type_name == MailReferent.ATTR_REF and (isinstance(s.value, Referent))): 
                print("{0}, ".format((s.value).toString(True, lang, lev + 1)), end="", file=res, flush=True)
        if (res.tell() < 100): 
            str0_ = Utils.ifNotNull(self.text, "")
            str0_ = str0_.replace('\r', ' ').replace('\n', ' ')
            if (len(str0_) > 100): 
                str0_ = (str0_[0:0+100] + "...")
            print(str0_, end="", file=res)
        return Utils.toStringStringIO(res)
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        return obj == self
    
    def _addRef(self, r : 'Referent', lev : int=0) -> None:
        if (r is None or lev > 4): 
            return
        if ((((isinstance(r, PersonReferent)) or (isinstance(r, PersonPropertyReferent)) or r.type_name == "ORGANIZATION") or r.type_name == "PHONE" or r.type_name == "URI") or (isinstance(r, GeoReferent)) or (isinstance(r, AddressReferent))): 
            self.addSlot(MailReferent.ATTR_REF, r, False, 0)
        for s in r.slots: 
            if (isinstance(s.value, Referent)): 
                self._addRef(Utils.asObjectOrNull(s.value, Referent), lev + 1)
    
    @staticmethod
    def _new1499(_arg1 : 'MailKind') -> 'MailReferent':
        res = MailReferent()
        res.kind = _arg1
        return res