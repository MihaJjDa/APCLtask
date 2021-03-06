﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.morph.DerivateWord import DerivateWord
from pullenti.morph.MorphLang import MorphLang

class DerivateGroup:
    """ Дериватная группа """
    
    def __init__(self) -> None:
        self.words = list()
        self.prefix = None;
        self.is_dummy = False
        self.not_generate = False
        self.is_generated = False
        self.m_transitive = -1
        self.nexts = None;
        self._lazy_pos = 0
        self.tag = None;
    
    @property
    def transitive(self) -> int:
        """ Признак транзитивности группы (не только глаголов!) """
        if (self.m_transitive >= 0): 
            return self.m_transitive
        return -1
    
    def containsWord(self, word : str, lang : 'MorphLang') -> bool:
        """ Содержит ли группа слово
        
        Args:
            word(str): слово
            lang(MorphLang): возможный язык
        
        """
        for w in self.words: 
            if (w.spelling == word): 
                if (lang is None or lang.is_undefined or w.lang is None): 
                    return True
                if (not ((lang) & w.lang).is_undefined): 
                    return True
        return False
    
    def __str__(self) -> str:
        res = "?"
        if (len(self.words) > 0): 
            res = "<{0}>".format(self.words[0].spelling)
        if (self.is_dummy): 
            res = "DUMMY: {0}".format(res)
        elif (self.is_generated): 
            res = "GEN: {0}".format(res)
        return res
    
    def createByPrefix(self, pref : str, lang : 'MorphLang') -> 'DerivateGroup':
        res = DerivateGroup._new39(True, pref)
        for w in self.words: 
            if (lang is not None and not lang.is_undefined and ((w.lang) & lang).is_undefined): 
                continue
            rw = DerivateWord._new40(res, pref + w.spelling, w.lang, w.class0_, w.aspect, w.reflexive, w.tense, w.voice, w.attrs)
            res.words.append(rw)
        return res
    
    @staticmethod
    def _new39(_arg1 : bool, _arg2 : str) -> 'DerivateGroup':
        res = DerivateGroup()
        res.is_generated = _arg1
        res.prefix = _arg2
        return res