﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Referent import Referent
from pullenti.ner.booklink.BookLinkRefType import BookLinkRefType
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.booklink.internal.MetaBookLinkRef import MetaBookLinkRef

class BookLinkRefReferent(Referent):
    """ Ссылка на внешний литературный источник (статью, книгу и пр.) """
    
    OBJ_TYPENAME = "BOOKLINKREF"
    
    ATTR_BOOK = "BOOK"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_PAGES = "PAGES"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_MISC = "MISC"
    
    def __init__(self) -> None:
        super().__init__(BookLinkRefReferent.OBJ_TYPENAME)
        self.instance_of = MetaBookLinkRef._global_meta
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        if (self.number is not None): 
            print("[{0}] ".format(self.number), end="", file=res, flush=True)
        if (self.pages is not None): 
            print("{0} {1}; ".format(("pages" if lang is not None and lang.is_en else "стр."), self.pages), end="", file=res, flush=True)
        book_ = self.book
        if (book_ is None): 
            print("?", end="", file=res)
        else: 
            print(book_.toString(short_variant, lang, lev), end="", file=res)
        return Utils.toStringStringIO(res)
    
    @property
    def parent_referent(self) -> 'Referent':
        return Utils.asObjectOrNull(self.getSlotValue(BookLinkRefReferent.ATTR_BOOK), Referent)
    
    @property
    def typ(self) -> 'BookLinkRefType':
        """ Тип ссылки """
        val = self.getStringValue(BookLinkRefReferent.ATTR_TYPE)
        if (val is None): 
            return BookLinkRefType.UNDEFINED
        try: 
            return Utils.valToEnum(val, BookLinkRefType)
        except Exception as ex397: 
            pass
        return BookLinkRefType.UNDEFINED
    @typ.setter
    def typ(self, value) -> 'BookLinkRefType':
        self.addSlot(BookLinkRefReferent.ATTR_TYPE, Utils.enumToString(value), True, 0)
        return value
    
    @property
    def book(self) -> 'Referent':
        """ Собственно ссылка вовне на источник - BookLinkReferent или DecreeReferent """
        return Utils.asObjectOrNull(self.getSlotValue(BookLinkRefReferent.ATTR_BOOK), Referent)
    @book.setter
    def book(self, value) -> 'Referent':
        self.addSlot(BookLinkRefReferent.ATTR_BOOK, value, True, 0)
        return value
    
    @property
    def number(self) -> str:
        """ Порядковый номер в списке """
        return self.getStringValue(BookLinkRefReferent.ATTR_NUMBER)
    @number.setter
    def number(self, value) -> str:
        num = value
        if (num is not None and num.find('-') > 0): 
            num = num.replace(" - ", "-")
        self.addSlot(BookLinkRefReferent.ATTR_NUMBER, num, True, 0)
        return value
    
    @property
    def pages(self) -> str:
        """ Ссылка на страницу или диапазон страниц """
        return self.getStringValue(BookLinkRefReferent.ATTR_PAGES)
    @pages.setter
    def pages(self, value) -> str:
        self.addSlot(BookLinkRefReferent.ATTR_PAGES, value, True, 0)
        return value
    
    def canBeEquals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        r = Utils.asObjectOrNull(obj, BookLinkRefReferent)
        if (r is None): 
            return False
        if (self.book != r.book): 
            return False
        if (self.number != r.number): 
            return False
        if (self.pages != r.pages): 
            return False
        if (((self.typ == BookLinkRefType.INLINE)) != ((r.typ == BookLinkRefType.INLINE))): 
            return False
        return True
    
    @staticmethod
    def getNumberDiff(r1 : 'Referent', r2 : 'Referent') -> int:
        """ Возвращает разницу номеров r2 - r1, иначе null, если номеров нет
        
        Args:
            r1(Referent): 
            r2(Referent): 
        
        """
        num1 = r1.getStringValue(BookLinkRefReferent.ATTR_NUMBER)
        num2 = r2.getStringValue(BookLinkRefReferent.ATTR_NUMBER)
        if (num1 is None or num2 is None): 
            return None
        wrapn1398 = RefOutArgWrapper(0)
        inoutres399 = Utils.tryParseInt(num1, wrapn1398)
        wrapn2400 = RefOutArgWrapper(0)
        inoutres401 = Utils.tryParseInt(num2, wrapn2400)
        n1 = wrapn1398.value
        n2 = wrapn2400.value
        if (not inoutres399 or not inoutres401): 
            return None
        return n2 - n1
    
    @staticmethod
    def _new389(_arg1 : 'Referent') -> 'BookLinkRefReferent':
        res = BookLinkRefReferent()
        res.book = _arg1
        return res