﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class MorphMood(IntEnum):
    """ Наклонение (для глаголов) """
    UNDEFINED = 0
    INDICATIVE = 1
    SUBJUNCTIVE = 2
    IMPERATIVE = 4
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)