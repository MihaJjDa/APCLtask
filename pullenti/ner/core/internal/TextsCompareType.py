﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class TextsCompareType(IntEnum):
    NONCOMPARABLE = 0
    EQUIVALENT = 1
    EARLY = 2
    LATER = 3
    IN = 4
    CONTAINS = 5
    INTERSECT = 6
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)