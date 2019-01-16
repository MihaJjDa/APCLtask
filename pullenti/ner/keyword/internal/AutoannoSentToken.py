# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import math
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.TextAnnotation import TextAnnotation
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.keyword.KeywordType import KeywordType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.keyword.KeywordReferent import KeywordReferent

class AutoannoSentToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.rank = 0
        self.value = None;
    
    def __str__(self) -> str:
        return "{0}: {1}".format(self.rank, self.value)
    
    @staticmethod
    def __tryParse(t : 'Token') -> 'AutoannoSentToken':
        if (t is None or not MiscHelper.canBeStartOfSentence(t)): 
            return None
        res = AutoannoSentToken(t, t)
        has_verb = False
        while t is not None: 
            if (MiscHelper.canBeStartOfSentence(t) and t != res.begin_token): 
                break
            r = t.getReferent()
            if (isinstance(r, KeywordReferent)): 
                res.rank += (r).rank
                if ((r).typ == KeywordType.PREDICATE): 
                    has_verb = True
            elif (isinstance(t, TextToken)): 
                mc = t.getMorphClassInDictionary()
                if (mc.is_pronoun or mc.is_personal_pronoun): 
                    res.rank -= (1)
                elif (t.length_char > 1): 
                    res.rank -= .1
            res.end_token = t
            t = t.next0_
        if (not has_verb): 
            res.rank /= (3)
        res.value = MiscHelper.getTextValueOfMetaToken(res, Utils.valToEnum((GetTextAttr.KEEPREGISTER) | (GetTextAttr.KEEPQUOTES), GetTextAttr))
        return res
    
    @staticmethod
    def createAnnotation(kit_ : 'AnalysisKit', max_sents : int) -> 'KeywordReferent':
        sents = list()
        t = kit_.first_token
        first_pass3023 = True
        while True:
            if first_pass3023: first_pass3023 = False
            else: t = t.next0_
            if (not (t is not None)): break
            sent = AutoannoSentToken.__tryParse(t)
            if (sent is None): 
                continue
            if (sent.rank > 0): 
                sents.append(sent)
            t = sent.end_token
        if (len(sents) < 2): 
            return None
        i = 0
        while i < len(sents): 
            sents[i].rank *= ((((len(sents) - i))) / (len(sents)))
            i += 1
        if ((max_sents * 3) > len(sents)): 
            max_sents = (math.floor(len(sents) / 3))
            if (max_sents == 0): 
                max_sents = 1
        while len(sents) > max_sents:
            mini = 0
            min0_ = sents[0].rank
            i = 1
            while i < len(sents): 
                if (sents[i].rank <= min0_): 
                    min0_ = sents[i].rank
                    mini = i
                i += 1
            del sents[mini]
        ano = KeywordReferent()
        ano.typ = KeywordType.ANNOTATION
        tmp = io.StringIO()
        for s in sents: 
            if (tmp.tell() > 0): 
                print(' ', end="", file=tmp)
            print(s.value, end="", file=tmp)
            ano.occurrence.append(TextAnnotation._new1488(s.begin_char, s.end_char, ano, kit_.sofa))
        ano.addSlot(KeywordReferent.ATTR_VALUE, Utils.toStringStringIO(tmp), True, 0)
        return ano