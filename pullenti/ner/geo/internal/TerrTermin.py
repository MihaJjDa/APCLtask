﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.ner.core.Termin import Termin

class TerrTermin(Termin):
    
    def __init__(self, source : str, lang_ : 'MorphLang'=None) -> None:
        super().__init__(None, lang_, False)
        self.is_state = False
        self.is_region = False
        self.is_adjective = False
        self.is_always_prefix = False
        self.is_doubt = False
        self.is_moscow_region = False
        self.is_strong = False
        self.is_specific_prefix = False
        self.is_sovet = False
        self.initByNormalText(source, lang_)
    
    @staticmethod
    def _new1163(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        return res
    
    @staticmethod
    def _new1164(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        return res
    
    @staticmethod
    def _new1165(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.is_doubt = _arg3
        return res
    
    @staticmethod
    def _new1166(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new1169(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.is_adjective = _arg3
        return res
    
    @staticmethod
    def _new1170(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.is_adjective = _arg4
        return res
    
    @staticmethod
    def _new1171(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        return res
    
    @staticmethod
    def _new1174(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        return res
    
    @staticmethod
    def _new1175(_arg1 : str, _arg2 : bool, _arg3 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new1176(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1181(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_always_prefix = _arg3
        return res
    
    @staticmethod
    def _new1183(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_always_prefix = _arg4
        return res
    
    @staticmethod
    def _new1192(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_strong = _arg3
        return res
    
    @staticmethod
    def _new1195(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_strong = _arg4
        return res
    
    @staticmethod
    def _new1198(_arg1 : str, _arg2 : str, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.canonic_text = _arg2
        res.is_sovet = _arg3
        return res
    
    @staticmethod
    def _new1201(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_adjective = _arg3
        return res
    
    @staticmethod
    def _new1202(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_adjective = _arg4
        return res
    
    @staticmethod
    def _new1203(_arg1 : str, _arg2 : bool, _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_specific_prefix = _arg3
        res.is_always_prefix = _arg4
        return res
    
    @staticmethod
    def _new1204(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool, _arg5 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_specific_prefix = _arg4
        res.is_always_prefix = _arg5
        return res
    
    @staticmethod
    def _new1205(_arg1 : str, _arg2 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.acronym = _arg2
        return res
    
    @staticmethod
    def _new1206(_arg1 : str, _arg2 : str, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.acronym = _arg2
        res.is_region = _arg3
        return res
    
    @staticmethod
    def _new1208(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_moscow_region = _arg2
        return res