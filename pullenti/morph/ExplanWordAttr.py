# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

class ExplanWordAttr:
    """ Дополнительные характеристики слова """
    
    def __init__(self, val : 'ExplanWordAttr'=None) -> None:
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
    def is_animated(self) -> bool:
        """ Одушевлённое """
        return self.__getValue(0)
    @is_animated.setter
    def is_animated(self, value_) -> bool:
        self.__setValue(0, value_)
        return value_
    
    @property
    def is_named(self) -> bool:
        """ Может иметь собственное имя """
        return self.__getValue(1)
    @is_named.setter
    def is_named(self, value_) -> bool:
        self.__setValue(1, value_)
        return value_
    
    @property
    def is_numbered(self) -> bool:
        """ Может иметь номер (например, Олимпиада 80) """
        return self.__getValue(2)
    @is_numbered.setter
    def is_numbered(self, value_) -> bool:
        self.__setValue(2, value_)
        return value_
    
    @property
    def is_measured(self) -> bool:
        """ Может ли иметь числовую характеристику (длина, количество, деньги ...) """
        return self.__getValue(3)
    @is_measured.setter
    def is_measured(self, value_) -> bool:
        self.__setValue(3, value_)
        return value_
    
    @property
    def is_emo_positive(self) -> bool:
        """ Позитивная окраска """
        return self.__getValue(4)
    @is_emo_positive.setter
    def is_emo_positive(self, value_) -> bool:
        self.__setValue(4, value_)
        return value_
    
    @property
    def is_emo_negative(self) -> bool:
        """ Негативная окраска """
        return self.__getValue(5)
    @is_emo_negative.setter
    def is_emo_negative(self, value_) -> bool:
        self.__setValue(5, value_)
        return value_
    
    @property
    def is_animal(self) -> bool:
        """ Это животное, а не человек (для IsAnimated = true) """
        return self.__getValue(6)
    @is_animal.setter
    def is_animal(self, value_) -> bool:
        self.__setValue(6, value_)
        return value_
    
    @property
    def is_can_person_after(self) -> bool:
        """ За словом может быть персона в родительном падеже (слуга Хозяина, отец Ивана ...) """
        return self.__getValue(7)
    @is_can_person_after.setter
    def is_can_person_after(self, value_) -> bool:
        self.__setValue(7, value_)
        return value_
    
    def __str__(self) -> str:
        tmp_str = io.StringIO()
        if (self.is_animated): 
            print("одуш.", end="", file=tmp_str)
        if (self.is_animal): 
            print("животн.", end="", file=tmp_str)
        if (self.is_named): 
            print("именов.", end="", file=tmp_str)
        if (self.is_numbered): 
            print("нумеруем.", end="", file=tmp_str)
        if (self.is_measured): 
            print("измеряем.", end="", file=tmp_str)
        if (self.is_emo_positive): 
            print("позитив.", end="", file=tmp_str)
        if (self.is_emo_negative): 
            print("негатив.", end="", file=tmp_str)
        if (self.is_can_person_after): 
            print("персона_за_родит.", end="", file=tmp_str)
        return Utils.toStringStringIO(tmp_str)
    
    def equals(self, obj : object) -> bool:
        if (not ((isinstance(obj, ExplanWordAttr)))): 
            return False
        return self.value == (obj).value
    
    def __hash__(self) -> int:
        return self.value
    
    def __and__(self : 'ExplanWordAttr', arg2 : 'ExplanWordAttr') -> 'ExplanWordAttr':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return ExplanWordAttr._new41(((val1) & (val2)))
    
    def __or__(self : 'ExplanWordAttr', arg2 : 'ExplanWordAttr') -> 'ExplanWordAttr':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return ExplanWordAttr._new41(((val1) | (val2)))
    
    def __eq__(self : 'ExplanWordAttr', arg2 : 'ExplanWordAttr') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 == val2
    
    def __ne__(self : 'ExplanWordAttr', arg2 : 'ExplanWordAttr') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 != val2
    
    UNDEFINED = None
    
    @staticmethod
    def _new41(_arg1 : int) -> 'ExplanWordAttr':
        res = ExplanWordAttr()
        res.value = _arg1
        return res
    
    # static constructor for class ExplanWordAttr
    @staticmethod
    def _static_ctor():
        ExplanWordAttr.UNDEFINED = ExplanWordAttr()

ExplanWordAttr._static_ctor()