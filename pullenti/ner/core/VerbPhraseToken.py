﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphVoice import MorphVoice
from pullenti.morph.MorphClass import MorphClass

class VerbPhraseToken(MetaToken):
    """ Глагольная группа """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.items = list()
    
    @property
    def first_verb(self) -> 'VerbPhraseItemToken':
        """ Первый глагол (всегда есть, иначе это не группа) """
        for it in self.items: 
            if (not it.is_adverb): 
                return it
        return None
    
    @property
    def last_verb(self) -> 'VerbPhraseItemToken':
        """ Последний глагол (если один, то совпадает с первым) """
        for i in range(len(self.items) - 1, -1, -1):
            if (not self.items[i].is_adverb): 
                return self.items[i]
        return None
    
    @property
    def is_verb_passive(self) -> bool:
        """ Признак того, что вся группа в пассивном залоге (по первому глаголу) """
        fi = self.first_verb
        if (fi is None or fi.verb_morph is None): 
            return False
        return fi.verb_morph.misc.voice == MorphVoice.PASSIVE
    
    def __str__(self) -> str:
        if (len(self.items) == 1): 
            return "{0}, {1}".format(str(self.items[0]), str(self.morph))
        tmp = io.StringIO()
        for it in self.items: 
            if (tmp.tell() > 0): 
                print(' ', end="", file=tmp)
            print(it, end="", file=tmp)
        print(", {0}".format(str(self.morph)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def getNormalCaseText(self, mc : 'MorphClass'=None, single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        return super().getNormalCaseText(MorphClass.VERB, single_number, gender, keep_chars)