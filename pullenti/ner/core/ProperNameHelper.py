﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.Token import Token
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.morph.Morphology import Morphology
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper

class ProperNameHelper:
    """ Поддержка работы с собственными именами """
    
    @staticmethod
    def __corrChars(str0_ : str, ci : 'CharsInfo', keep_chars : bool) -> str:
        if (not keep_chars): 
            return str0_
        if (ci.is_all_lower): 
            return str0_.lower()
        if (ci.is_capital_upper): 
            return MiscHelper.convertFirstCharUpperAndOtherLower(str0_)
        return str0_
    
    @staticmethod
    def __getNameWithoutBrackets(begin : 'Token', end : 'Token', normalize_first_noun_group : bool=False, normal_first_group_single : bool=False, ignore_geo_referent : bool=False) -> str:
        """ Получить строковое значение между токенами, при этом исключая кавычки и скобки
        
        Args:
            begin(Token): начальный токен
            end(Token): конечный токен
            normalize_first_noun_group(bool): нормализовывать ли первую именную группу (именит. падеж)
            normal_first_group_single(bool): приводить ли к единственному числу первую именную группу
            ignore_geo_referent(bool): игнорировать внутри географические сущности
        
        """
        res = None
        if (BracketHelper.canBeStartOfSequence(begin, False, False) and BracketHelper.canBeEndOfSequence(end, False, begin, False)): 
            begin = begin.next0_
            end = end.previous
        if (normalize_first_noun_group and not begin.morph.class0_.is_preposition): 
            npt = NounPhraseHelper.tryParse(begin, NounPhraseParseAttr.REFERENTCANBENOUN, 0)
            if (npt is not None): 
                if (npt.noun.getMorphClassInDictionary().is_undefined and len(npt.adjectives) == 0): 
                    npt = (None)
            if (npt is not None and npt.end_token.end_char > end.end_char): 
                npt = (None)
            if (npt is not None): 
                res = npt.getNormalCaseText(None, normal_first_group_single, MorphGender.UNDEFINED, False)
                te = npt.end_token.next0_
                if (((te is not None and te.next0_ is not None and te.is_comma) and (isinstance(te.next0_, TextToken)) and te.next0_.end_char <= end.end_char) and te.next0_.morph.class0_.is_verb and te.next0_.morph.class0_.is_adjective): 
                    for it in te.next0_.morph.items: 
                        if (it.gender == npt.morph.gender or (((it.gender) & (npt.morph.gender))) != (MorphGender.UNDEFINED)): 
                            if (not ((it.case_) & npt.morph.case_).is_undefined): 
                                if (it.number == npt.morph.number or (((it.number) & (npt.morph.number))) != (MorphNumber.UNDEFINED)): 
                                    var = (te.next0_).term
                                    if (isinstance(it, MorphWordForm)): 
                                        var = (it).normal_case
                                    bi = MorphBaseInfo._new549(MorphClass.ADJECTIVE, npt.morph.gender, npt.morph.number, npt.morph.language)
                                    var = Morphology.getWordform(var, bi)
                                    if (var is not None): 
                                        res = "{0}, {1}".format(res, var)
                                        te = te.next0_.next0_
                                    break
                if (te is not None and te.end_char <= end.end_char): 
                    s = ProperNameHelper.getNameEx(te, end, MorphClass.UNDEFINED, MorphCase.UNDEFINED, MorphGender.UNDEFINED, True, ignore_geo_referent)
                    if (not Utils.isNullOrEmpty(s)): 
                        if (not str.isalnum(s[0])): 
                            res = "{0}{1}".format(res, s)
                        else: 
                            res = "{0} {1}".format(res, s)
            elif ((isinstance(begin, TextToken)) and begin.chars.is_cyrillic_letter): 
                mm = begin.getMorphClassInDictionary()
                if (not mm.is_undefined): 
                    res = begin.getNormalCaseText(mm, False, MorphGender.UNDEFINED, False)
                    if (begin.end_char < end.end_char): 
                        res = "{0} {1}".format(res, ProperNameHelper.getNameEx(begin.next0_, end, MorphClass.UNDEFINED, MorphCase.UNDEFINED, MorphGender.UNDEFINED, True, False))
        if (res is None): 
            res = ProperNameHelper.getNameEx(begin, end, MorphClass.UNDEFINED, MorphCase.UNDEFINED, MorphGender.UNDEFINED, True, ignore_geo_referent)
        if (not Utils.isNullOrEmpty(res)): 
            k = 0
            i = len(res) - 1
            while i >= 0: 
                if (res[i] == '*' or Utils.isWhitespace(res[i])): 
                    pass
                else: 
                    break
                i -= 1; k += 1
            if (k > 0): 
                if (k == len(res)): 
                    return None
                res = res[0:0+len(res) - k]
        return res
    
    @staticmethod
    def __getName(begin : 'Token', end : 'Token') -> str:
        """ Получить строковое значение между токенами без нормализации первой группы, всё в верхнем регистре.
        
        Args:
            begin(Token): 
            end(Token): 
        
        """
        res = ProperNameHelper.getNameEx(begin, end, MorphClass.UNDEFINED, MorphCase.UNDEFINED, MorphGender.UNDEFINED, False, False)
        return res
    
    @staticmethod
    def getNameEx(begin : 'Token', end : 'Token', cla : 'MorphClass', mc : 'MorphCase', gender : 'MorphGender'=MorphGender.UNDEFINED, ignore_brackets_and_hiphens : bool=False, ignore_geo_referent : bool=False) -> str:
        if (end is None or begin is None): 
            return None
        if (begin.end_char > end.begin_char and begin != end): 
            return None
        res = io.StringIO()
        prefix = None
        t = begin
        first_pass2809 = True
        while True:
            if first_pass2809: first_pass2809 = False
            else: t = t.next0_
            if (not (t is not None and t.end_char <= end.end_char)): break
            if (res.tell() > 1000): 
                break
            if (t.is_table_control_char): 
                continue
            if (ignore_brackets_and_hiphens): 
                if (BracketHelper.isBracket(t, False)): 
                    if (t == end): 
                        break
                    if (t.isCharOf("(<[")): 
                        br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                        if (br is not None and br.end_char <= end.end_char): 
                            tmp = ProperNameHelper.getNameEx(br.begin_token.next0_, br.end_token.previous, MorphClass.UNDEFINED, MorphCase.UNDEFINED, MorphGender.UNDEFINED, ignore_brackets_and_hiphens, False)
                            if (tmp is not None): 
                                if ((br.end_char == end.end_char and br.begin_token.next0_ == br.end_token.previous and not br.begin_token.next0_.chars.is_letter) and not ((isinstance(br.begin_token.next0_, ReferentToken)))): 
                                    pass
                                else: 
                                    print(" {0}{1}{2}".format(t.getSourceText(), tmp, br.end_token.getSourceText()), end="", file=res, flush=True)
                            t = br.end_token
                    continue
                if (t.is_hiphen): 
                    if (t == end): 
                        break
                    elif (t.is_whitespace_before or t.is_whitespace_after): 
                        continue
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is not None): 
                if (not ignore_brackets_and_hiphens): 
                    if ((tt.next0_ is not None and tt.next0_.is_hiphen and (isinstance(tt.next0_.next0_, TextToken))) and tt != end and tt.next0_ != end): 
                        if (prefix is None): 
                            prefix = tt.term
                        else: 
                            prefix = "{0}-{1}".format(prefix, tt.term)
                        t = tt.next0_
                        if (t == end): 
                            break
                        else: 
                            continue
                s = None
                if (cla.value != (0) or not mc.is_undefined or gender != MorphGender.UNDEFINED): 
                    for wff in tt.morph.items: 
                        wf = Utils.asObjectOrNull(wff, MorphWordForm)
                        if (wf is None): 
                            continue
                        if (cla.value != (0)): 
                            if ((((wf.class0_.value) & (cla.value))) == 0): 
                                continue
                        if (not mc.is_undefined): 
                            if (((wf.case_) & mc).is_undefined): 
                                continue
                        if (gender != MorphGender.UNDEFINED): 
                            if ((((wf.gender) & (gender))) == (MorphGender.UNDEFINED)): 
                                continue
                        if (s is None or wf.normal_case == tt.term): 
                            s = wf.normal_case
                    if (s is None and gender != MorphGender.UNDEFINED): 
                        for wff in tt.morph.items: 
                            wf = Utils.asObjectOrNull(wff, MorphWordForm)
                            if (wf is None): 
                                continue
                            if (cla.value != (0)): 
                                if ((((wf.class0_.value) & (cla.value))) == 0): 
                                    continue
                            if (not mc.is_undefined): 
                                if (((wf.case_) & mc).is_undefined): 
                                    continue
                            if (s is None or wf.normal_case == tt.term): 
                                s = wf.normal_case
                if (s is None): 
                    s = tt.term
                    if (tt.chars.is_last_lower and tt.length_char > 2): 
                        s = tt.getSourceText()
                        for i in range(len(s) - 1, -1, -1):
                            if (str.isupper(s[i])): 
                                s = s[0:0+i + 1]
                                break
                if (prefix is not None): 
                    delim = "-"
                    if (ignore_brackets_and_hiphens): 
                        delim = " "
                    s = "{0}{1}{2}".format(prefix, delim, s)
                prefix = (None)
                if (res.tell() > 0 and len(s) > 0): 
                    if (str.isalnum(s[0])): 
                        ch0 = Utils.getCharAtStringIO(res, res.tell() - 1)
                        if (ch0 == '-'): 
                            pass
                        else: 
                            print(' ', end="", file=res)
                    elif (not ignore_brackets_and_hiphens and BracketHelper.canBeStartOfSequence(tt, False, False)): 
                        print(' ', end="", file=res)
                print(s, end="", file=res)
            elif (isinstance(t, NumberToken)): 
                if (res.tell() > 0): 
                    if (not t.is_whitespace_before and Utils.getCharAtStringIO(res, res.tell() - 1) == '-'): 
                        pass
                    else: 
                        print(' ', end="", file=res)
                nt = Utils.asObjectOrNull(t, NumberToken)
                if ((t.morph.class0_.is_adjective and nt.typ == NumberSpellingType.WORDS and nt.begin_token == nt.end_token) and (isinstance(nt.begin_token, TextToken))): 
                    print((nt.begin_token).term, end="", file=res)
                else: 
                    print(nt.value, end="", file=res)
            elif (isinstance(t, MetaToken)): 
                if ((ignore_geo_referent and t != begin and t.getReferent() is not None) and t.getReferent().type_name == "GEO"): 
                    continue
                s = ProperNameHelper.getNameEx((t).begin_token, (t).end_token, cla, mc, gender, ignore_brackets_and_hiphens, ignore_geo_referent)
                if (not Utils.isNullOrEmpty(s)): 
                    if (res.tell() > 0): 
                        if (not t.is_whitespace_before and Utils.getCharAtStringIO(res, res.tell() - 1) == '-'): 
                            pass
                        else: 
                            print(' ', end="", file=res)
                    print(s, end="", file=res)
            if (t == end): 
                break
        if (res.tell() == 0): 
            return None
        return Utils.toStringStringIO(res)