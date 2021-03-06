﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

class MorphClass:
    """ Часть речи """
    
    def __init__(self, val : 'MorphClass'=None) -> None:
        self.value = 0
        self.value = (0)
        if (val is not None): 
            self.value = val.value
    
    def __getValue(self, i : int) -> bool:
        return (((((self.value) >> i)) & 1)) != 0
    
    def __setValue(self, i : int, val : bool) -> None:
        if (val): 
            self.value |= ((1 << i))
        else: 
            self.value &= (~ ((1 << i)))
    
    @property
    def is_undefined(self) -> bool:
        """ Неопределённый тип """
        return self.value == (0)
    @is_undefined.setter
    def is_undefined(self, value_) -> bool:
        self.value = (0)
        return value_
    
    @property
    def is_noun(self) -> bool:
        """ Существительное """
        return self.__getValue(0)
    @is_noun.setter
    def is_noun(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__setValue(0, value_)
        return value_
    
    @staticmethod
    def isNounInt(val : int) -> bool:
        return ((val & 1)) != 0
    
    @property
    def is_adjective(self) -> bool:
        """ Прилагательное """
        return self.__getValue(1)
    @is_adjective.setter
    def is_adjective(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__setValue(1, value_)
        return value_
    
    @staticmethod
    def isAdjectiveInt(val : int) -> bool:
        return ((val & 2)) != 0
    
    @property
    def is_verb(self) -> bool:
        """ Глагол """
        return self.__getValue(2)
    @is_verb.setter
    def is_verb(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__setValue(2, value_)
        return value_
    
    @staticmethod
    def isVerbInt(val : int) -> bool:
        return ((val & 4)) != 0
    
    @property
    def is_adverb(self) -> bool:
        """ Наречие """
        return self.__getValue(3)
    @is_adverb.setter
    def is_adverb(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__setValue(3, value_)
        return value_
    
    @staticmethod
    def isAdverbInt(val : int) -> bool:
        return ((val & 8)) != 0
    
    @property
    def is_pronoun(self) -> bool:
        """ Местоимение """
        return self.__getValue(4)
    @is_pronoun.setter
    def is_pronoun(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__setValue(4, value_)
        return value_
    
    @staticmethod
    def isPronounInt(val : int) -> bool:
        return ((val & 0x10)) != 0
    
    @property
    def is_misc(self) -> bool:
        """ Всякая ерунда (частицы, междометия) """
        return self.__getValue(5)
    @is_misc.setter
    def is_misc(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__setValue(5, value_)
        return value_
    
    @staticmethod
    def isMiscInt(val : int) -> bool:
        return ((val & 0x20)) != 0
    
    @property
    def is_preposition(self) -> bool:
        """ Предлог """
        return self.__getValue(6)
    @is_preposition.setter
    def is_preposition(self, value_) -> bool:
        self.__setValue(6, value_)
        return value_
    
    @staticmethod
    def isPrepositionInt(val : int) -> bool:
        return ((val & 0x40)) != 0
    
    @property
    def is_conjunction(self) -> bool:
        """ Союз """
        return self.__getValue(7)
    @is_conjunction.setter
    def is_conjunction(self, value_) -> bool:
        self.__setValue(7, value_)
        return value_
    
    @staticmethod
    def isConjunctionInt(val : int) -> bool:
        return ((val & 0x80)) != 0
    
    @property
    def is_proper(self) -> bool:
        """ Собственное имя (фамилия, имя, отчество, геогр.название и др.) """
        return self.__getValue(8)
    @is_proper.setter
    def is_proper(self, value_) -> bool:
        self.__setValue(8, value_)
        return value_
    
    @staticmethod
    def isProperInt(val : int) -> bool:
        return ((val & 0x100)) != 0
    
    @property
    def is_proper_surname(self) -> bool:
        """ Фамилия """
        return self.__getValue(9)
    @is_proper_surname.setter
    def is_proper_surname(self, value_) -> bool:
        if (value_): 
            self.is_proper = True
        self.__setValue(9, value_)
        return value_
    
    @staticmethod
    def isProperSurnameInt(val : int) -> bool:
        return ((val & 0x200)) != 0
    
    @property
    def is_proper_name(self) -> bool:
        """ Фамилия """
        return self.__getValue(10)
    @is_proper_name.setter
    def is_proper_name(self, value_) -> bool:
        if (value_): 
            self.is_proper = True
        self.__setValue(10, value_)
        return value_
    
    @staticmethod
    def isProperNameInt(val : int) -> bool:
        return ((val & 0x400)) != 0
    
    @property
    def is_proper_secname(self) -> bool:
        """ Отчество """
        return self.__getValue(11)
    @is_proper_secname.setter
    def is_proper_secname(self, value_) -> bool:
        if (value_): 
            self.is_proper = True
        self.__setValue(11, value_)
        return value_
    
    @staticmethod
    def isProperSecnameInt(val : int) -> bool:
        return ((val & 0x800)) != 0
    
    @property
    def is_proper_geo(self) -> bool:
        """ Географическое название """
        return self.__getValue(12)
    @is_proper_geo.setter
    def is_proper_geo(self, value_) -> bool:
        if (value_): 
            self.is_proper = True
        self.__setValue(12, value_)
        return value_
    
    @staticmethod
    def isProperGeoInt(val : int) -> bool:
        return ((val & 0x1000)) != 0
    
    @property
    def is_personal_pronoun(self) -> bool:
        """ Личное местоимение (я, мой, ты, он ...) """
        return self.__getValue(13)
    @is_personal_pronoun.setter
    def is_personal_pronoun(self, value_) -> bool:
        self.__setValue(13, value_)
        return value_
    
    @staticmethod
    def isPersonalPronounInt(val : int) -> bool:
        return ((val & 0x2000)) != 0
    
    __m_names = None
    
    def __str__(self) -> str:
        tmp_str = io.StringIO()
        i = 0
        first_pass2723 = True
        while True:
            if first_pass2723: first_pass2723 = False
            else: i += 1
            if (not (i < len(MorphClass.__m_names))): break
            if (self.__getValue(i)): 
                if (i == 5): 
                    if (self.is_conjunction or self.is_preposition or self.is_proper): 
                        continue
                if (tmp_str.tell() > 0): 
                    print("|", end="", file=tmp_str)
                print(MorphClass.__m_names[i], end="", file=tmp_str)
        return Utils.toStringStringIO(tmp_str)
    
    def equals(self, obj : object) -> bool:
        if (not ((isinstance(obj, MorphClass)))): 
            return False
        return self.value == (obj).value
    
    def __hash__(self) -> int:
        return self.value
    
    def __and__(self : 'MorphClass', arg2 : 'MorphClass') -> 'MorphClass':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphClass._new62(((val1) & (val2)))
    
    def __or__(self : 'MorphClass', arg2 : 'MorphClass') -> 'MorphClass':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphClass._new62(((val1) | (val2)))
    
    def __xor__(self : 'MorphClass', arg2 : 'MorphClass') -> 'MorphClass':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphClass._new62(((val1) ^ (val2)))
    
    def __eq__(self : 'MorphClass', arg2 : 'MorphClass') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 == val2
    
    def __ne__(self : 'MorphClass', arg2 : 'MorphClass') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 != val2
    
    UNDEFINED = None
    
    NOUN = None
    
    PRONOUN = None
    
    PERSONAL_PRONOUN = None
    
    VERB = None
    
    ADJECTIVE = None
    
    ADVERB = None
    
    PREPOSITION = None
    
    CONJUNCTION = None
    
    @staticmethod
    def _new62(_arg1 : int) -> 'MorphClass':
        res = MorphClass()
        res.value = _arg1
        return res
    
    @staticmethod
    def _new65(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_undefined = _arg1
        return res
    
    @staticmethod
    def _new66(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_noun = _arg1
        return res
    
    @staticmethod
    def _new67(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_pronoun = _arg1
        return res
    
    @staticmethod
    def _new68(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_personal_pronoun = _arg1
        return res
    
    @staticmethod
    def _new69(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_verb = _arg1
        return res
    
    @staticmethod
    def _new70(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_adjective = _arg1
        return res
    
    @staticmethod
    def _new71(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_adverb = _arg1
        return res
    
    @staticmethod
    def _new72(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_preposition = _arg1
        return res
    
    @staticmethod
    def _new73(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_conjunction = _arg1
        return res
    
    @staticmethod
    def _new2415(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_proper_surname = _arg1
        return res
    
    # static constructor for class MorphClass
    @staticmethod
    def _static_ctor():
        MorphClass.__m_names = ["существ.", "прилаг.", "глагол", "наречие", "местоим.", "разное", "предлог", "союз", "собств.", "фамилия", "имя", "отч.", "геогр.", "личн.местоим."]
        MorphClass.UNDEFINED = MorphClass._new65(True)
        MorphClass.NOUN = MorphClass._new66(True)
        MorphClass.PRONOUN = MorphClass._new67(True)
        MorphClass.PERSONAL_PRONOUN = MorphClass._new68(True)
        MorphClass.VERB = MorphClass._new69(True)
        MorphClass.ADJECTIVE = MorphClass._new70(True)
        MorphClass.ADVERB = MorphClass._new71(True)
        MorphClass.PREPOSITION = MorphClass._new72(True)
        MorphClass.CONJUNCTION = MorphClass._new73(True)

MorphClass._static_ctor()