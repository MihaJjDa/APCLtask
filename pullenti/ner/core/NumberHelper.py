# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import math
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.NumberExToken import NumberExToken
from pullenti.ner.Token import Token
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.NumberToken import NumberToken
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.Morphology import Morphology
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection

class NumberHelper:
    """ Работа с числовыми значениями """
    
    @staticmethod
    def _tryParseNumber(token : 'Token') -> 'NumberToken':
        """ Попробовать создать числительное (без знака, целочисленное).
         Внимание! Этот метод всегда вызывается процессором при формировании цепочки токенов,
         так что все NumberToken уже созданы.
        
        Args:
            token(Token): 
        
        """
        return NumberHelper.__TryParse(token, None)
    
    @staticmethod
    def __TryParse(token : 'Token', prev_val : 'NumberToken'=None) -> 'NumberToken':
        if (isinstance(token, NumberToken)): 
            return Utils.asObjectOrNull(token, NumberToken)
        tt = Utils.asObjectOrNull(token, TextToken)
        if (tt is None): 
            return None
        et = tt
        val = None
        typ = NumberSpellingType.DIGIT
        term = tt.term
        if (str.isdigit(term[0])): 
            val = term
        if (val is not None): 
            hiph = False
            if ((isinstance(et.next0_, TextToken)) and et.next0_.is_hiphen): 
                if ((et.whitespaces_after_count < 2) and (et.next0_.whitespaces_after_count < 2)): 
                    et = (Utils.asObjectOrNull(et.next0_, TextToken))
                    hiph = True
            mc = None
            if (hiph or not et.is_whitespace_after): 
                rr = NumberHelper.__analizeNumberTail(Utils.asObjectOrNull(et.next0_, TextToken), val)
                if (rr is None): 
                    et = tt
                else: 
                    mc = rr.morph
                    et = (Utils.asObjectOrNull(rr.end_token, TextToken))
            else: 
                et = tt
            if (et.next0_ is not None and et.next0_.isChar('(')): 
                num2 = NumberHelper._tryParseNumber(et.next0_.next0_)
                if ((num2 is not None and num2.value == val and num2.end_token.next0_ is not None) and num2.end_token.next0_.isChar(')')): 
                    et = (Utils.asObjectOrNull(num2.end_token.next0_, TextToken))
            while (isinstance(et.next0_, TextToken)) and not ((isinstance(et.previous, NumberToken))) and et.is_whitespace_before:
                if (et.whitespaces_after_count != 1): 
                    break
                sss = (et.next0_).term
                if (sss == "000"): 
                    val = (val + "000")
                    et = (Utils.asObjectOrNull(et.next0_, TextToken))
                    continue
                if (str.isdigit(sss[0]) and len(sss) == 3): 
                    val2 = val
                    ttt = et.next0_
                    first_pass2806 = True
                    while True:
                        if first_pass2806: first_pass2806 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        ss = ttt.getSourceText()
                        if (ttt.whitespaces_before_count == 1 and ttt.length_char == 3 and str.isdigit(ss[0])): 
                            wrapii554 = RefOutArgWrapper(0)
                            inoutres555 = Utils.tryParseInt(ss, wrapii554)
                            ii = wrapii554.value
                            if (not inoutres555): 
                                break
                            val2 += ss
                            continue
                        if ((ttt.isCharOf(".,") and not ttt.is_whitespace_before and not ttt.is_whitespace_after) and ttt.next0_ is not None and str.isdigit(ttt.next0_.getSourceText()[0])): 
                            if (ttt.next0_.is_whitespace_after and (isinstance(ttt.previous, TextToken))): 
                                et = (Utils.asObjectOrNull(ttt.previous, TextToken))
                                val = val2
                                break
                        break
                break
            for k in range(3):
                if ((isinstance(et.next0_, TextToken)) and et.next0_.chars.is_letter): 
                    tt = (Utils.asObjectOrNull(et.next0_, TextToken))
                    t0 = et
                    coef = None
                    if (k == 0): 
                        coef = "000000000"
                        if (tt.isValue("МИЛЛИАРД", "МІЛЬЯРД") or tt.isValue("BILLION", None) or tt.isValue("BN", None)): 
                            et = tt
                            val += coef
                        elif (tt.isValue("МЛРД", None)): 
                            et = tt
                            val += coef
                            if ((isinstance(et.next0_, TextToken)) and et.next0_.isChar('.')): 
                                et = (Utils.asObjectOrNull(et.next0_, TextToken))
                        else: 
                            continue
                    elif (k == 1): 
                        coef = "000000"
                        if (tt.isValue("МИЛЛИОН", "МІЛЬЙОН") or tt.isValue("MILLION", None)): 
                            et = tt
                            val += coef
                        elif (tt.isValue("МЛН", None)): 
                            et = tt
                            val += coef
                            if ((isinstance(et.next0_, TextToken)) and et.next0_.isChar('.')): 
                                et = (Utils.asObjectOrNull(et.next0_, TextToken))
                        elif ((isinstance(tt, TextToken)) and (tt).term == "M"): 
                            if (NumberHelper._isMoneyChar(et.previous) is not None): 
                                et = tt
                                val += coef
                            else: 
                                break
                        else: 
                            continue
                    else: 
                        coef = "000"
                        if (tt.isValue("ТЫСЯЧА", "ТИСЯЧА") or tt.isValue("THOUSAND", None)): 
                            et = tt
                            val += coef
                        elif (tt.isValue("ТЫС", None) or tt.isValue("ТИС", None)): 
                            et = tt
                            val += coef
                            if ((isinstance(et.next0_, TextToken)) and et.next0_.isChar('.')): 
                                et = (Utils.asObjectOrNull(et.next0_, TextToken))
                        else: 
                            break
                    if (((t0 == token and t0.length_char <= 3 and t0.previous is not None) and not t0.is_whitespace_before and t0.previous.isCharOf(",.")) and not t0.previous.is_whitespace_before and (((isinstance(t0.previous.previous, NumberToken)) or prev_val is not None))): 
                        if (t0.length_char == 1): 
                            val = val[0:0+len(val) - 1]
                        elif (t0.length_char == 2): 
                            val = val[0:0+len(val) - 2]
                        else: 
                            val = val[0:0+len(val) - 3]
                        hi = ((t0.previous.previous).value if isinstance(t0.previous.previous, NumberToken) else prev_val.value)
                        cou = len(coef) - len(val)
                        while cou > 0: 
                            hi = (hi + "0")
                            cou -= 1
                        val = (hi + val)
                        token = t0.previous.previous
                    next0_ = NumberHelper.__TryParse(et.next0_, None)
                    if (next0_ is None or len(next0_.value) > len(coef)): 
                        break
                    tt1 = next0_.end_token
                    if (((isinstance(tt1.next0_, TextToken)) and not tt1.is_whitespace_after and tt1.next0_.isCharOf(".,")) and not tt1.next0_.is_whitespace_after): 
                        re1 = NumberHelper.__TryParse(tt1.next0_.next0_, next0_)
                        if (re1 is not None and re1.begin_token == next0_.begin_token): 
                            next0_ = re1
                    if (len(val) > len(next0_.value)): 
                        val = val[0:0+len(val) - len(next0_.value)]
                    val += next0_.value
                    et = (Utils.asObjectOrNull(next0_.end_token, TextToken))
                    break
            res = NumberToken._new556(token, et, val, typ, mc)
            if (et.next0_ is not None and (len(res.value) < 4) and ((et.next0_.is_hiphen or et.next0_.isValue("ДО", None)))): 
                tt1 = et.next0_.next0_
                first_pass2807 = True
                while True:
                    if first_pass2807: first_pass2807 = False
                    else: tt1 = tt1.next0_
                    if (not (tt1 is not None)): break
                    if (not ((isinstance(tt1, TextToken)))): 
                        break
                    if (str.isdigit((tt1).term[0])): 
                        continue
                    if (tt1.isCharOf(",.") or NumberHelper._isMoneyChar(tt1) is not None): 
                        continue
                    if (tt1.isValue("МИЛЛИОН", "МІЛЬЙОН") or tt1.isValue("МЛН", None) or tt1.isValue("MILLION", None)): 
                        res.value = res.value + "000000"
                    elif ((tt1.isValue("МИЛЛИАРД", "МІЛЬЯРД") or tt1.isValue("МЛРД", None) or tt1.isValue("BILLION", None)) or tt1.isValue("BN", None)): 
                        res.value = res.value + "000000000"
                    elif (tt1.isValue("ТЫСЯЧА", "ТИСЯЧА") or tt1.isValue("ТЫС", "ТИС") or tt1.isValue("THOUSAND", None)): 
                        res.value = res.value + "1000"
                    break
            return res
        int_val = 0
        et = (None)
        loc_value = 0
        is_adj = False
        jprev = -1
        t = tt
        while t is not None: 
            if (t != tt and t.newlines_before_count > 1): 
                break
            term = t.term
            if (not str.isalpha(term[0])): 
                break
            num = NumberHelper._m_nums.tryParse(t, TerminParseAttr.FULLWORDSONLY)
            if (num is None): 
                break
            j = (num.termin.tag)
            if (jprev > 0 and (jprev < 20) and (j < 20)): 
                break
            is_adj = ((j & NumberHelper.__pril_num_tag_bit)) != 0
            j &= (~ NumberHelper.__pril_num_tag_bit)
            if (is_adj and t != tt): 
                if ((t.isValue("ДЕСЯТЫЙ", None) or t.isValue("СОТЫЙ", None) or t.isValue("ТЫСЯЧНЫЙ", None)) or t.isValue("ДЕСЯТИТЫСЯЧНЫЙ", None) or t.isValue("МИЛЛИОННЫЙ", None)): 
                    break
            if (j >= 1000): 
                if (loc_value == 0): 
                    loc_value = 1
                int_val += (loc_value * j)
                loc_value = 0
            else: 
                if (loc_value > 0 and loc_value <= j): 
                    break
                loc_value += j
            et = t
            if (j == 1000 or j == 1000000): 
                if ((isinstance(et.next0_, TextToken)) and et.next0_.isChar('.')): 
                    et = Utils.asObjectOrNull(et.next0_, TextToken)
                    t = et
            jprev = j
            t = (Utils.asObjectOrNull(t.next0_, TextToken))
        if (loc_value > 0): 
            int_val += loc_value
        if (int_val == 0 or et is None): 
            return None
        nt = NumberToken(tt, et, str(int_val), NumberSpellingType.WORDS)
        if (et.morph is not None): 
            nt.morph = MorphCollection(et.morph)
            for wff in et.morph.items: 
                wf = Utils.asObjectOrNull(wff, MorphWordForm)
                if (wf is not None and wf.misc is not None and "собир." in wf.misc.attrs): 
                    nt.morph.class0_ = MorphClass.NOUN
                    break
            if (not is_adj): 
                nt.morph.removeItems((MorphClass.ADJECTIVE) | MorphClass.NOUN, False)
                if (nt.morph.class0_.is_undefined): 
                    nt.morph.class0_ = MorphClass.NOUN
            if (et.chars.is_latin_letter and is_adj): 
                nt.morph.class0_ = MorphClass.ADJECTIVE
        return nt
    
    @staticmethod
    def tryParseRoman(t : 'Token') -> 'NumberToken':
        """ Попробовать выделить римскую цифру
        
        Args:
            t(Token): 
        
        """
        if (isinstance(t, NumberToken)): 
            return Utils.asObjectOrNull(t, NumberToken)
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None or not t.chars.is_letter): 
            return None
        term = tt.term
        if (not NumberHelper.__isRomVal(term)): 
            return None
        if (tt.morph.class0_.is_preposition): 
            if (tt.chars.is_all_lower): 
                return None
        res = NumberToken(t, t, "", NumberSpellingType.ROMAN)
        nums = list()
        val = 0
        while t is not None: 
            if (t != res.begin_token and t.is_whitespace_before): 
                break
            if (not ((isinstance(t, TextToken)))): 
                break
            term = (t).term
            if (not NumberHelper.__isRomVal(term)): 
                break
            for s in term: 
                i = NumberHelper.__romVal(s)
                if (i > 0): 
                    nums.append(i)
            res.end_token = t
            t = t.next0_
        if (len(nums) == 0): 
            return None
        i = 0
        while i < len(nums): 
            if ((i + 1) < len(nums)): 
                if (nums[i] == 1 and nums[i + 1] == 5): 
                    val += 4
                    i += 1
                elif (nums[i] == 1 and nums[i + 1] == 10): 
                    val += 9
                    i += 1
                elif (nums[i] == 10 and nums[i + 1] == 50): 
                    val += 40
                    i += 1
                elif (nums[i] == 10 and nums[i + 1] == 100): 
                    val += 90
                    i += 1
                else: 
                    val += nums[i]
            else: 
                val += nums[i]
            i += 1
        res.int_value = val
        hiph = False
        et = res.end_token.next0_
        if (et is None): 
            return res
        if (et.next0_ is not None and et.next0_.is_hiphen): 
            et = et.next0_
            hiph = True
        if (hiph or not et.is_whitespace_after): 
            mc = NumberHelper.__analizeNumberTail(Utils.asObjectOrNull(et.next0_, TextToken), res.value)
            if (mc is not None): 
                res.end_token = mc.end_token
                res.morph = mc.morph
        if ((res.begin_token == res.end_token and val == 1 and res.begin_token.chars.is_all_lower) and res.begin_token.morph.language.is_ua): 
            return None
        return res
    
    @staticmethod
    def __romVal(ch : 'char') -> int:
        if (ch == 'Х' or ch == 'X'): 
            return 10
        if (ch == 'І' or ch == 'I'): 
            return 1
        if (ch == 'V'): 
            return 5
        if (ch == 'L'): 
            return 50
        if (ch == 'C' or ch == 'С'): 
            return 100
        return 0
    
    @staticmethod
    def __isRomVal(str0_ : str) -> bool:
        for ch in str0_: 
            if (NumberHelper.__romVal(ch) < 1): 
                return False
        return True
    
    @staticmethod
    def tryParseRomanBack(token : 'Token') -> 'NumberToken':
        """ Выделить римскую цифру с token в обратном порядке
        
        Args:
            token(Token): 
        
        """
        t = token
        if (t is None): 
            return None
        if ((t.chars.is_all_lower and t.previous is not None and t.previous.is_hiphen) and t.previous.previous is not None): 
            t = token.previous.previous
        res = None
        while t is not None: 
            nt = NumberHelper.tryParseRoman(t)
            if (nt is not None): 
                if (nt.end_token == token): 
                    res = nt
                else: 
                    break
            if (t.is_whitespace_after): 
                break
            t = t.previous
        return res
    
    @staticmethod
    def tryParseAge(t : 'Token') -> 'NumberToken':
        """ Это выделение числительных типа 16-летие, 50-летний
        
        Args:
            t(Token): 
        
        """
        if (t is None): 
            return None
        nt = Utils.asObjectOrNull(t, NumberToken)
        nt_next = None
        if (nt is not None): 
            nt_next = nt.next0_
        else: 
            if (t.isValue("AGED", None) and (isinstance(t.next0_, NumberToken))): 
                return NumberToken(t, t.next0_, (t.next0_).value, NumberSpellingType.AGE)
            nt = NumberHelper.tryParseRoman(t)
            if ((nt) is not None): 
                nt_next = nt.end_token.next0_
        if (nt is not None): 
            if (nt_next is not None): 
                t1 = nt_next
                if (t1.is_hiphen): 
                    t1 = t1.next0_
                if (isinstance(t1, TextToken)): 
                    v = (t1).term
                    if ((v == "ЛЕТ" or v == "ЛЕТИЯ" or v == "ЛЕТИЕ") or v == "РІЧЧЯ"): 
                        return NumberToken._new556(t, t1, nt.value, NumberSpellingType.AGE, t1.morph)
                    if (t1.isValue("ЛЕТНИЙ", "РІЧНИЙ")): 
                        return NumberToken._new556(t, t1, nt.value, NumberSpellingType.AGE, t1.morph)
                    if (v == "Л" or ((v == "Р" and nt.morph.language.is_ua))): 
                        return NumberToken(t, (t1.next0_ if t1.next0_ is not None and t1.next0_.isChar('.') else t1), nt.value, NumberSpellingType.AGE)
            return None
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        s = tt.term
        if (LanguageHelper.endsWithEx(s, "ЛЕТИЕ", "ЛЕТИЯ", "РІЧЧЯ", None)): 
            term = NumberHelper._m_nums.find(s[0:0+len(s) - 5])
            if (term is not None): 
                return NumberToken._new556(tt, tt, str(term.tag), NumberSpellingType.AGE, tt.morph)
        s = tt.lemma
        if (LanguageHelper.endsWithEx(s, "ЛЕТНИЙ", "РІЧНИЙ", None, None)): 
            term = NumberHelper._m_nums.find(s[0:0+len(s) - 6])
            if (term is not None): 
                return NumberToken._new556(tt, tt, str(term.tag), NumberSpellingType.AGE, tt.morph)
        return None
    
    @staticmethod
    def tryParseAnniversary(t : 'Token') -> 'NumberToken':
        """ Выделение годовщин и летий (XX-летие) ... """
        nt = Utils.asObjectOrNull(t, NumberToken)
        t1 = None
        if (nt is not None): 
            t1 = nt.next0_
        else: 
            nt = NumberHelper.tryParseRoman(t)
            if ((nt) is None): 
                if (isinstance(t, TextToken)): 
                    v = (t).term
                    num = 0
                    if (v.endswith("ЛЕТИЯ") or v.endswith("ЛЕТИЕ")): 
                        if (v.startswith("ВОСЕМЬСОТ") or v.startswith("ВОСЬМИСОТ")): 
                            num = 800
                    if (num > 0): 
                        return NumberToken(t, t, str(num), NumberSpellingType.AGE)
                return None
            t1 = nt.end_token.next0_
        if (t1 is None): 
            return None
        if (t1.is_hiphen): 
            t1 = t1.next0_
        if (isinstance(t1, TextToken)): 
            v = (t1).term
            if ((v == "ЛЕТ" or v == "ЛЕТИЯ" or v == "ЛЕТИЕ") or t1.isValue("ГОДОВЩИНА", None)): 
                return NumberToken(t, t1, nt.value, NumberSpellingType.AGE)
            if (t1.morph.language.is_ua): 
                if (v == "РОКІВ" or v == "РІЧЧЯ" or t1.isValue("РІЧНИЦЯ", None)): 
                    return NumberToken(t, t1, nt.value, NumberSpellingType.AGE)
        return None
    
    __m_samples = None
    
    @staticmethod
    def __analizeNumberTail(tt : 'TextToken', val : str) -> 'MetaToken':
        if (not ((isinstance(tt, TextToken)))): 
            return None
        s = tt.term
        mc = None
        if (not tt.chars.is_letter): 
            if (((s == "<" or s == "(")) and (isinstance(tt.next0_, TextToken))): 
                s = (tt.next0_).term
                if ((s == "TH" or s == "ST" or s == "RD") or s == "ND"): 
                    if (tt.next0_.next0_ is not None and tt.next0_.next0_.isCharOf(">)")): 
                        mc = MorphCollection()
                        mc.class0_ = MorphClass.ADJECTIVE
                        mc.language = MorphLang.EN
                        return MetaToken._new561(tt, tt.next0_.next0_, mc)
            return None
        if ((s == "TH" or s == "ST" or s == "RD") or s == "ND"): 
            mc = MorphCollection()
            mc.class0_ = MorphClass.ADJECTIVE
            mc.language = MorphLang.EN
            return MetaToken._new561(tt, tt, mc)
        if (not tt.chars.is_cyrillic_letter): 
            return None
        if (not tt.is_whitespace_after): 
            if (tt.next0_ is not None and tt.next0_.chars.is_letter): 
                return None
            if (tt.length_char == 1 and ((tt.isValue("X", None) or tt.isValue("Х", None)))): 
                return None
        if (not tt.chars.is_all_lower): 
            ss = (tt).term
            if (ss == "Я" or ss == "Й" or ss == "Е"): 
                pass
            elif (len(ss) == 2 and ((ss[1] == 'Я' or ss[1] == 'Й' or ss[1] == 'Е'))): 
                pass
            else: 
                return None
        if ((tt).term == "М"): 
            if (tt.previous is None or not tt.previous.is_hiphen): 
                return None
        if (Utils.isNullOrEmpty(val)): 
            return None
        dig = ((ord(val[len(val) - 1])) - (ord('0')))
        if ((dig < 0) or dig >= 10): 
            return None
        vars0_ = Morphology.getAllWordforms(NumberHelper.__m_samples[dig], None)
        if (vars0_ is None or len(vars0_) == 0): 
            return None
        for v in vars0_: 
            if (v.class0_.is_adjective and LanguageHelper.endsWith(v.normal_case, s) and v.number != MorphNumber.UNDEFINED): 
                if (mc is None): 
                    mc = MorphCollection()
                ok = False
                for it in mc.items: 
                    if (it.class0_ == v.class0_ and it.number == v.number and ((it.gender == v.gender or v.number == MorphNumber.PLURAL))): 
                        it.case_ = (it.case_) | v.case_
                        ok = True
                        break
                if (not ok): 
                    mc.addItem(MorphBaseInfo(v))
        if (tt.morph.language.is_ua and mc is None and s == "Ї"): 
            mc = MorphCollection()
            mc.addItem(MorphBaseInfo._new563(MorphClass.ADJECTIVE))
        if (mc is not None): 
            return MetaToken._new561(tt, tt, mc)
        if ((((len(s) < 3) and not tt.is_whitespace_before and tt.previous is not None) and tt.previous.is_hiphen and not tt.previous.is_whitespace_before) and tt.whitespaces_after_count == 1 and s != "А"): 
            return MetaToken._new561(tt, tt, MorphCollection._new565(MorphClass.ADJECTIVE))
        return None
    
    @staticmethod
    def __tryParseFloat(t : 'NumberToken', d : float) -> 'Token':
        from pullenti.ner.core.internal.NumberExHelper import NumberExHelper
        d.value = (0)
        if (t is None or t.next0_ is None or t.typ != NumberSpellingType.DIGIT): 
            return None
        tt = t.begin_token
        while tt is not None and tt.end_char <= t.end_char: 
            if ((isinstance(tt, TextToken)) and tt.chars.is_letter): 
                return None
            tt = tt.next0_
        kit = t.kit
        ns = None
        sps = None
        t1 = t
        first_pass2808 = True
        while True:
            if first_pass2808: first_pass2808 = False
            else: t1 = t1.next0_
            if (not (t1 is not None)): break
            if (t1.next0_ is None): 
                break
            if (((isinstance(t1.next0_, NumberToken)) and (t1.whitespaces_after_count < 3) and (t1.next0_).typ == NumberSpellingType.DIGIT) and t1.next0_.length_char == 3): 
                if (ns is None): 
                    ns = list()
                    ns.append(t)
                    sps = list()
                elif (sps[0] != ' '): 
                    return None
                ns.append(Utils.asObjectOrNull(t1.next0_, NumberToken))
                sps.append(' ')
                continue
            if ((t1.next0_.isCharOf(",.") and (isinstance(t1.next0_.next0_, NumberToken)) and (t1.next0_.next0_).typ == NumberSpellingType.DIGIT) and (t1.whitespaces_after_count < 2) and (t1.next0_.whitespaces_after_count < 2)): 
                if (ns is None): 
                    ns = list()
                    ns.append(t)
                    sps = list()
                elif (t1.next0_.is_whitespace_after and t1.next0_.next0_.length_char != 3 and ((('.' if t1.next0_.isChar('.') else ','))) == sps[len(sps) - 1]): 
                    break
                ns.append(Utils.asObjectOrNull(t1.next0_.next0_, NumberToken))
                sps.append(('.' if t1.next0_.isChar('.') else ','))
                t1 = t1.next0_
                continue
            break
        if (sps is None): 
            return None
        is_last_drob = False
        not_set_drob = False
        merge = False
        m_prev_point_char = '.'
        if (len(sps) == 1): 
            if (sps[0] == ' '): 
                is_last_drob = False
            elif (ns[1].length_char != 3): 
                is_last_drob = True
                if (len(ns) == 2): 
                    if (ns[1].end_token.chars.is_letter): 
                        merge = True
                    elif (ns[1].end_token.isChar('.') and ns[1].end_token.previous is not None and ns[1].end_token.previous.chars.is_letter): 
                        merge = True
                    if (ns[1].is_whitespace_before): 
                        if ((isinstance(ns[1].end_token, TextToken)) and (ns[1].end_token).term.endswith("000")): 
                            return None
            elif (ns[0].length_char > 3 or ns[0].real_value == 0): 
                is_last_drob = True
            else: 
                ok = True
                if (len(ns) == 2 and ns[1].length_char == 3): 
                    ttt = NumberExHelper._m_postfixes.tryParse(ns[1].end_token.next0_, TerminParseAttr.NO)
                    if (ttt is not None and (Utils.valToEnum(ttt.termin.tag, NumberExType)) == NumberExType.MONEY): 
                        is_last_drob = False
                        ok = False
                        not_set_drob = False
                    elif (ns[1].end_token.next0_ is not None and ns[1].end_token.next0_.isChar('(') and (isinstance(ns[1].end_token.next0_.next0_, NumberToken))): 
                        nt1 = (Utils.asObjectOrNull(ns[1].end_token.next0_.next0_, NumberToken))
                        if (nt1.real_value == (((ns[0].real_value * (1000)) + ns[1].real_value))): 
                            is_last_drob = False
                            ok = False
                            not_set_drob = False
                if (ok): 
                    if ("pt" in t.kit.misc_data): 
                        m_prev_point_char = (t.kit.misc_data["pt"])
                    if (m_prev_point_char == sps[0]): 
                        is_last_drob = True
                        not_set_drob = True
                    else: 
                        is_last_drob = False
                        not_set_drob = True
        else: 
            last = sps[len(sps) - 1]
            if (last == ' ' and sps[0] != last): 
                return None
            i = 0
            while i < (len(sps) - 1): 
                if (sps[i] != sps[0]): 
                    return None
                elif (ns[i + 1].length_char != 3): 
                    return None
                i += 1
            if (sps[0] != last): 
                is_last_drob = True
            elif (ns[len(ns) - 1].length_char != 3): 
                return None
        i = 0
        while i < len(ns): 
            if ((i < (len(ns) - 1)) or not is_last_drob): 
                if (i == 0): 
                    d.value = ns[i].real_value
                else: 
                    d.value = ((d.value * (1000)) + ns[i].real_value)
                if (i == (len(ns) - 1) and not not_set_drob): 
                    if (sps[len(sps) - 1] == ','): 
                        m_prev_point_char = '.'
                    elif (sps[len(sps) - 1] == '.'): 
                        m_prev_point_char = ','
            else: 
                if (not not_set_drob): 
                    m_prev_point_char = sps[len(sps) - 1]
                    if (m_prev_point_char == ','): 
                        pass
                if (merge): 
                    sss = str(ns[i].value)
                    kkk = 0
                    while kkk < (len(sss) - ns[i].begin_token.length_char): 
                        d.value *= (10)
                        kkk += 1
                    f2 = ns[i].real_value
                    kkk = 0
                    while kkk < ns[i].begin_token.length_char: 
                        f2 /= (10)
                        kkk += 1
                    d.value += f2
                else: 
                    f2 = ns[i].real_value
                    kkk = 0
                    while kkk < ns[i].length_char: 
                        f2 /= (10)
                        kkk += 1
                    d.value += f2
            i += 1
        if ("pt" in kit.misc_data): 
            kit.misc_data["pt"] = (m_prev_point_char)
        else: 
            kit.misc_data["pt"] = m_prev_point_char
        return ns[len(ns) - 1]
    
    @staticmethod
    def tryParseRealNumber(t : 'Token', can_be_integer : bool=False) -> 'NumberToken':
        """ Это разделитель дроби по-умолчанию, используется для случаев, когда невозможно принять однозначного решения.
         Устанавливается на основе последнего успешного анализа.
        Выделить действительное число, знак также выделяется,
         разделители дроби могут быть точка или запятая, разделителями тысячных
         могут быть точки, пробелы и запятые.
        
        Args:
            t(Token): начальный токен
            can_be_integer(bool): число должно быть целым
        
        Returns:
            NumberToken: результат или null
        """
        is_not = False
        t0 = t
        if (t is not None): 
            if (t.is_hiphen or t.isValue("МИНУС", None)): 
                t = t.next0_
                is_not = True
            elif (t.isChar('+') or t.isValue("ПЛЮС", None)): 
                t = t.next0_
        if ((isinstance(t, TextToken)) and ((t.isValue("НОЛЬ", None) or t.isValue("НУЛЬ", None))) and t.next0_ is not None): 
            if (t.next0_.isValue("ЦЕЛЫЙ", None)): 
                t = t.next0_
            res0 = NumberToken(t, t.next0_, "0", NumberSpellingType.WORDS)
            t = t.next0_
            if ((isinstance(t, NumberToken)) and (t).int_value is not None): 
                val = (t).int_value
                if (t.next0_ is not None and val > 0): 
                    if (t.next0_.isValue("ДЕСЯТЫЙ", None)): 
                        res0.end_token = t.next0_
                        res0.real_value = ((val)) / (10)
                    elif (t.next0_.isValue("СОТЫЙ", None)): 
                        res0.end_token = t.next0_
                        res0.real_value = ((val)) / (100)
                    elif (t.next0_.isValue("ТЫСЯЧНЫЙ", None)): 
                        res0.end_token = t.next0_
                        res0.real_value = ((val)) / (1000)
                if (res0.real_value == 0): 
                    res0.end_token = t
                    res0.value = "0.{0}".format(val)
            return res0
        if (isinstance(t, TextToken)): 
            tok = NumberHelper.__m_after_points.tryParse(t, TerminParseAttr.NO)
            if (tok is not None): 
                res0 = NumberExToken(t, tok.end_token, None, NumberSpellingType.WORDS, NumberExType.UNDEFINED)
                res0.real_value = (tok.termin.tag)
                return res0
        if (not ((isinstance(t, NumberToken)))): 
            return None
        if (t.next0_ is not None and t.next0_.isValue("ЦЕЛЫЙ", None) and (((isinstance(t.next0_.next0_, NumberToken)) or (((isinstance(t.next0_.next0_, TextToken)) and t.next0_.next0_.isValue("НОЛЬ", None)))))): 
            res0 = NumberExToken(t, t.next0_, (t).value, NumberSpellingType.WORDS, NumberExType.UNDEFINED)
            t = t.next0_.next0_
            val = 0
            if (isinstance(t, TextToken)): 
                res0.end_token = t
                t = t.next0_
            if (isinstance(t, NumberToken)): 
                res0.end_token = t
                val = (t).real_value
                t = t.next0_
            if (t is not None): 
                if (t.isValue("ДЕСЯТЫЙ", None)): 
                    res0.end_token = t
                    res0.real_value = (((val) / (10))) + res0.real_value
                elif (t.isValue("СОТЫЙ", None)): 
                    res0.end_token = t
                    res0.real_value = (((val) / (100))) + res0.real_value
                elif (t.isValue("ТЫСЯЧНЫЙ", None)): 
                    res0.end_token = t
                    res0.real_value = (((val) / (1000))) + res0.real_value
            if (res0.real_value == 0): 
                str0_ = "0.{0}".format(val)
                dd = 0
                wrapdd569 = RefOutArgWrapper(0)
                inoutres570 = Utils.tryParseFloat(str0_, wrapdd569)
                dd = wrapdd569.value
                if (inoutres570): 
                    pass
                else: 
                    wrapdd567 = RefOutArgWrapper(0)
                    inoutres568 = Utils.tryParseFloat(str0_.replace('.', ','), wrapdd567)
                    dd = wrapdd567.value
                    if (inoutres568): 
                        pass
                    else: 
                        return None
                res0.real_value = dd + res0.real_value
            return res0
        wrapd572 = RefOutArgWrapper(0)
        tt = NumberHelper.__tryParseFloat(Utils.asObjectOrNull(t, NumberToken), wrapd572)
        d = wrapd572.value
        if (tt is None): 
            if ((t.next0_ is None or t.is_whitespace_after or t.next0_.chars.is_letter) or can_be_integer): 
                tt = t
                d = (t).real_value
            else: 
                return None
        if (is_not): 
            d = (- d)
        return NumberExToken._new571(t0, tt, "", NumberSpellingType.DIGIT, NumberExType.UNDEFINED, d)
    
    @staticmethod
    def getNumberAdjective(value : int, gender : 'MorphGender', num : 'MorphNumber') -> str:
        """ Преобразовать число в числительное, записанное буквами, в соотв. роде и числе.
         Например, 5 жен.ед. - ПЯТАЯ,  26 мн. - ДВАДЦАТЬ ШЕСТЫЕ
        
        Args:
            value(int): значение
            gender(MorphGender): род
            num(MorphNumber): число
        
        """
        if ((value < 1) or value >= 100): 
            return None
        words = None
        if (num == MorphNumber.PLURAL): 
            words = NumberHelper.__m_plural_number_words
        elif (gender == MorphGender.FEMINIE): 
            words = NumberHelper.__m_woman_number_words
        elif (gender == MorphGender.NEUTER): 
            words = NumberHelper.__m_neutral_number_words
        else: 
            words = NumberHelper.__m_man_number_words
        if (value < 20): 
            return words[value - 1]
        i = math.floor(value / 10)
        j = value % 10
        i -= 2
        if (i >= len(NumberHelper.__m_dec_dumber_words)): 
            return None
        if (j > 0): 
            return "{0} {1}".format(NumberHelper.__m_dec_dumber_words[i], words[j - 1])
        decs = None
        if (num == MorphNumber.PLURAL): 
            decs = NumberHelper.__m_plural_dec_dumber_words
        elif (gender == MorphGender.FEMINIE): 
            decs = NumberHelper.__m_woman_dec_dumber_words
        elif (gender == MorphGender.NEUTER): 
            decs = NumberHelper.__m_neutral_dec_dumber_words
        else: 
            decs = NumberHelper.__m_man_dec_dumber_words
        return decs[i]
    
    __m_man_number_words = None
    
    __m_neutral_number_words = None
    
    __m_woman_number_words = None
    
    __m_plural_number_words = None
    
    __m_dec_dumber_words = None
    
    __m_man_dec_dumber_words = None
    
    __m_woman_dec_dumber_words = None
    
    __m_neutral_dec_dumber_words = None
    
    __m_plural_dec_dumber_words = None
    
    _m_romans = None
    
    @staticmethod
    def getNumberRoman(val : int) -> str:
        """ Получить для числа римскую запись
        
        Args:
            val(int): 
        
        """
        if (val > 0 and val <= len(NumberHelper._m_romans)): 
            return NumberHelper._m_romans[val - 1]
        return str(val)
    
    @staticmethod
    def tryParseNumberWithPostfix(t : 'Token') -> 'NumberExToken':
        """ Выделение стандартных мер, типа: 10 кв.м.
        
        Args:
            t(Token): начальный токен
        
        """
        from pullenti.ner.core.internal.NumberExHelper import NumberExHelper
        return NumberExHelper.tryParseNumberWithPostfix(t)
    
    @staticmethod
    def tryParsePostfixOnly(t : 'Token') -> 'NumberExToken':
        """ Это попробовать только тип (постфикс) без самого числа.
         Например, куб.м.
        
        Args:
            t(Token): 
        
        """
        from pullenti.ner.core.internal.NumberExHelper import NumberExHelper
        return NumberExHelper.tryAttachPostfixOnly(t)
    
    @staticmethod
    def _isMoneyChar(t : 'Token') -> str:
        """ Если этообозначение денежной единицы (н-р, $), то возвращает код валюты
        
        Args:
            t(Token): 
        
        """
        if (not ((isinstance(t, TextToken))) or t.length_char != 1): 
            return None
        ch = (t).term[0]
        if (ch == '$'): 
            return "USD"
        if (ch == '£' or ch == (chr(0xA3)) or ch == (chr(0x20A4))): 
            return "GBP"
        if (ch == '€'): 
            return "EUR"
        if (ch == '¥' or ch == (chr(0xA5))): 
            return "JPY"
        if (ch == (chr(0x20A9))): 
            return "KRW"
        if (ch == (chr(0xFFE5)) or ch == 'Ұ' or ch == 'Ұ'): 
            return "CNY"
        if (ch == (chr(0x20BD))): 
            return "RUB"
        if (ch == (chr(0x20B4))): 
            return "UAH"
        if (ch == (chr(0x20AB))): 
            return "VND"
        if (ch == (chr(0x20AD))): 
            return "LAK"
        if (ch == (chr(0x20BA))): 
            return "TRY"
        if (ch == (chr(0x20B1))): 
            return "PHP"
        if (ch == (chr(0x17DB))): 
            return "KHR"
        if (ch == (chr(0x20B9))): 
            return "INR"
        if (ch == (chr(0x20A8))): 
            return "IDR"
        if (ch == (chr(0x20B5))): 
            return "GHS"
        if (ch == (chr(0x09F3))): 
            return "BDT"
        if (ch == (chr(0x20B8))): 
            return "KZT"
        if (ch == (chr(0x20AE))): 
            return "MNT"
        if (ch == (chr(0x0192))): 
            return "HUF"
        if (ch == (chr(0x20AA))): 
            return "ILS"
        return None
    
    @staticmethod
    def stringToDouble(str0_ : str) -> float:
        """ Для парсинга действительного числа из строки используйте эту функцию,
         которая работает назависимо от локализьных настроек и на всех языках программирования
        
        Args:
            str0_(str): строка
        
        Returns:
            float: число
        """
        wrapres575 = RefOutArgWrapper(0)
        inoutres576 = Utils.tryParseFloat(str0_, wrapres575)
        res = wrapres575.value
        if (inoutres576): 
            return res
        wrapres573 = RefOutArgWrapper(0)
        inoutres574 = Utils.tryParseFloat(str0_.replace('.', ','), wrapres573)
        res = wrapres573.value
        if (inoutres574): 
            return res
        return None
    
    @staticmethod
    def doubleToString(d : float) -> str:
        """ Независимо от языка и настроек выводит действиельное число в строку,
         разделитель - точка. Ситуация типа 1.0000000001 или 23.7299999999999,
         случающиеся на разных языках, округляются куда надо.
        
        Args:
            d(float): число
        
        Returns:
            str: результат
        """
        res = None
        if (math.trunc(d) == .0): 
            res = str(d).replace(",", ".")
        else: 
            rest = math.fabs(d - math.trunc(d))
            if ((rest < .000000001) and rest > 0): 
                res = str(math.trunc(d))
                if ((res.find('E') < 0) and (res.find('e') < 0)): 
                    ii = res.find('.')
                    if (ii < 0): 
                        ii = res.find(',')
                    if (ii > 0): 
                        return res[0:0+ii]
                    else: 
                        return res
            else: 
                res = str(d).replace(",", ".")
        if (res.endswith(".0")): 
            res = res[0:0+len(res) - 2]
        i = res.find('e')
        if (i < 0): 
            i = res.find('E')
        if (i > 0): 
            exp0_ = 0
            neg = False
            jj = i + 1
            while jj < len(res): 
                if (res[jj] == '+'): 
                    pass
                elif (res[jj] == '-'): 
                    neg = True
                else: 
                    exp0_ = ((exp0_ * 10) + (((ord(res[jj])) - (ord('0')))))
                jj += 1
            res = res[0:0+i]
            if (res.endswith(".0")): 
                res = res[0:0+len(res) - 2]
            nneg = False
            if (res[0] == '-'): 
                nneg = True
                res = res[1:]
            v1 = io.StringIO()
            v2 = io.StringIO()
            i = res.find('.')
            if (i < 0): 
                print(res, end="", file=v1)
            else: 
                print(res[0:0+i], end="", file=v1)
                print(res[i + 1:], end="", file=v2)
            while exp0_ > 0: 
                if (neg): 
                    if (v1.tell() > 0): 
                        Utils.insertStringIO(v2, 0, Utils.getCharAtStringIO(v1, v1.tell() - 1))
                        Utils.setLengthStringIO(v1, v1.tell() - 1)
                    else: 
                        Utils.insertStringIO(v2, 0, '0')
                elif (v2.tell() > 0): 
                    print(Utils.getCharAtStringIO(v2, 0), end="", file=v1)
                    Utils.removeStringIO(v2, 0, 1)
                else: 
                    print('0', end="", file=v1)
                exp0_ -= 1
            if (v2.tell() == 0): 
                res = Utils.toStringStringIO(v1)
            elif (v1.tell() == 0): 
                res = ("0." + Utils.toStringStringIO(v2))
            else: 
                res = "{0}.{1}".format(Utils.toStringStringIO(v1), Utils.toStringStringIO(v2))
            if (nneg): 
                res = ("-" + res)
        i = res.find('.')
        if (i < 0): 
            return res
        i += 1
        j = (i + 1)
        while j < len(res): 
            if (res[j] == '9'): 
                k = 0
                jj = j
                while jj < len(res): 
                    if (res[jj] != '9'): 
                        break
                    else: 
                        k += 1
                    jj += 1
                if (jj >= len(res) or ((jj == (len(res) - 1) and res[jj] == '8'))): 
                    if (k > 5): 
                        while j > i: 
                            if (res[j] != '9'): 
                                if (res[j] != '.'): 
                                    return "{0}{1}".format(res[0:0+j], ((((ord(res[j])) - (ord('0'))))) + 1)
                            j -= 1
                        break
            j += 1
        return res
    
    __pril_num_tag_bit = 0x40000000
    
    @staticmethod
    def _initialize() -> None:
        if (NumberHelper._m_nums is not None): 
            return
        NumberHelper._m_nums = TerminCollection()
        NumberHelper._m_nums.all_add_strs_normalized = True
        NumberHelper._m_nums.addStr("ОДИН", 1, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ПЕРВЫЙ", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ОДИН", 1, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ПЕРШИЙ", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ОДНА", 1, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ОДНО", 1, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("FIRST", 1 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("SEMEL", 1, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ONE", 1, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ДВА", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ВТОРОЙ", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ДВОЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ДВЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ДВУХ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ОБА", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ОБЕ", 2, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ДВА", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ДРУГИЙ", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ДВОЄ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ДВІ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ДВОХ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ОБОЄ", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ОБИДВА", 2, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("SECOND", 2 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("BIS", 2, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("TWO", 2, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ТРИ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ТРЕТИЙ", 3 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ТРЕХ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ТРОЕ", 3, MorphLang.RU, True)
        NumberHelper._m_nums.addStr("ТРИ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ТРЕТІЙ", 3 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ТРЬОХ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("ТРОЄ", 3, MorphLang.UA, True)
        NumberHelper._m_nums.addStr("THIRD", 3 | NumberHelper.__pril_num_tag_bit, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("TER", 3, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("THREE", 3, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ЧЕТЫРЕ", 4, None, False)
        NumberHelper._m_nums.addStr("ЧЕТВЕРТЫЙ", 4 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ЧЕТЫРЕХ", 4, None, False)
        NumberHelper._m_nums.addStr("ЧЕТВЕРО", 4, None, False)
        NumberHelper._m_nums.addStr("ЧОТИРИ", 4, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧЕТВЕРТИЙ", 4 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧОТИРЬОХ", 4, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FORTH", 4 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("QUATER", 4, None, False)
        NumberHelper._m_nums.addStr("FOUR", 4, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ПЯТЬ", 5, None, False)
        NumberHelper._m_nums.addStr("ПЯТЫЙ", 5 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ПЯТИ", 5, None, False)
        NumberHelper._m_nums.addStr("ПЯТЕРО", 5, None, False)
        NumberHelper._m_nums.addStr("ПЯТЬ", 5, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТИЙ", 5 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FIFTH", 5 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("QUINQUIES", 5, None, False)
        NumberHelper._m_nums.addStr("FIVE", 5, MorphLang.EN, True)
        NumberHelper._m_nums.addStr("ШЕСТЬ", 6, None, False)
        NumberHelper._m_nums.addStr("ШЕСТОЙ", 6 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ШЕСТИ", 6, None, False)
        NumberHelper._m_nums.addStr("ШЕСТЕРО", 6, None, False)
        NumberHelper._m_nums.addStr("ШІСТЬ", 6, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШОСТИЙ", 6 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SIX", 6, MorphLang.EN, False)
        NumberHelper._m_nums.addStr("SIXTH", 6 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("SEXIES ", 6, None, False)
        NumberHelper._m_nums.addStr("СЕМЬ", 7, None, False)
        NumberHelper._m_nums.addStr("СЕДЬМОЙ", 7 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("СЕМИ", 7, None, False)
        NumberHelper._m_nums.addStr("СЕМЕРО", 7, None, False)
        NumberHelper._m_nums.addStr("СІМ", 7, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СЬОМИЙ", 7 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SEVEN", 7, None, False)
        NumberHelper._m_nums.addStr("SEVENTH", 7 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("SEPTIES", 7, None, False)
        NumberHelper._m_nums.addStr("ВОСЕМЬ", 8, None, False)
        NumberHelper._m_nums.addStr("ВОСЬМОЙ", 8 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ВОСЬМИ", 8, None, False)
        NumberHelper._m_nums.addStr("ВОСЬМЕРО", 8, None, False)
        NumberHelper._m_nums.addStr("ВІСІМ", 8, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВОСЬМИЙ", 8 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("EIGHT", 8, None, False)
        NumberHelper._m_nums.addStr("EIGHTH", 8 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("OCTIES", 8, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТЬ", 9, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТЫЙ", 9 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТИ", 9, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТЕРО", 9, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТЬ", 9, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯТИЙ", 9 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("NINE", 9, None, False)
        NumberHelper._m_nums.addStr("NINTH", 9 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("NOVIES", 9, None, False)
        NumberHelper._m_nums.addStr("ДЕСЯТЬ", 10, None, False)
        NumberHelper._m_nums.addStr("ДЕСЯТЫЙ", 10 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДЕСЯТИ", 10, None, False)
        NumberHelper._m_nums.addStr("ДЕСЯТИРО", 10, None, False)
        NumberHelper._m_nums.addStr("ДЕСЯТЬ", 10, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕСЯТИЙ", 10 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("TEN", 10, None, False)
        NumberHelper._m_nums.addStr("TENTH", 10 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("DECIES", 10, None, False)
        NumberHelper._m_nums.addStr("ОДИННАДЦАТЬ", 11, None, False)
        NumberHelper._m_nums.addStr("ОДИНАДЦАТЬ", 11, None, False)
        NumberHelper._m_nums.addStr("ОДИННАДЦАТЫЙ", 11 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ОДИННАДЦАТИ", 11, None, False)
        NumberHelper._m_nums.addStr("ОДИННАДЦАТИРО", 11, None, False)
        NumberHelper._m_nums.addStr("ОДИНАДЦЯТЬ", 11, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ОДИНАДЦЯТИЙ", 11 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ОДИНАДЦЯТИ", 11, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ELEVEN", 11, None, False)
        NumberHelper._m_nums.addStr("ELEVENTH", 11 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДВЕНАДЦАТЬ", 12, None, False)
        NumberHelper._m_nums.addStr("ДВЕНАДЦАТЫЙ", 12 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДВЕНАДЦАТИ", 12, None, False)
        NumberHelper._m_nums.addStr("ДВАНАДЦЯТЬ", 12, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВАНАДЦЯТИЙ", 12 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВАНАДЦЯТИ", 12, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("TWELVE", 12, None, False)
        NumberHelper._m_nums.addStr("TWELFTH", 12 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ТРИНАДЦАТЬ", 13, None, False)
        NumberHelper._m_nums.addStr("ТРИНАДЦАТЫЙ", 13 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ТРИНАДЦАТИ", 13, None, False)
        NumberHelper._m_nums.addStr("ТРИНАДЦЯТЬ", 13, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРИНАДЦЯТИЙ", 13 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРИНАДЦЯТИ", 13, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("THIRTEEN", 13, None, False)
        NumberHelper._m_nums.addStr("THIRTEENTH", 13 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ЧЕТЫРНАДЦАТЬ", 14, None, False)
        NumberHelper._m_nums.addStr("ЧЕТЫРНАДЦАТЫЙ", 14 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ЧЕТЫРНАДЦАТИ", 14, None, False)
        NumberHelper._m_nums.addStr("ЧОТИРНАДЦЯТЬ", 14, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧОТИРНАДЦЯТИЙ", 14 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧОТИРНАДЦЯТИ", 14, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FOURTEEN", 14, None, False)
        NumberHelper._m_nums.addStr("FOURTEENTH", 14 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦАТЬ", 15, None, False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦАТЫЙ", 15 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦАТИ", 15, None, False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦЯТЬ", 15, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦЯТИЙ", 15 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТНАДЦЯТИ", 15, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FIFTEEN", 15, None, False)
        NumberHelper._m_nums.addStr("FIFTEENTH", 15 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ШЕСТНАДЦАТЬ", 16, None, False)
        NumberHelper._m_nums.addStr("ШЕСТНАДЦАТЫЙ", 16 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ШЕСТНАДЦАТИ", 16, None, False)
        NumberHelper._m_nums.addStr("ШІСТНАДЦЯТЬ", 16, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШІСТНАДЦЯТИЙ", 16 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШІСТНАДЦЯТИ", 16, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SIXTEEN", 16, None, False)
        NumberHelper._m_nums.addStr("SIXTEENTH", 16 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("СЕМНАДЦАТЬ", 17, None, False)
        NumberHelper._m_nums.addStr("СЕМНАДЦАТЫЙ", 17 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("СЕМНАДЦАТИ", 17, None, False)
        NumberHelper._m_nums.addStr("СІМНАДЦЯТЬ", 17, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СІМНАДЦЯТИЙ", 17 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СІМНАДЦЯТИ", 17, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SEVENTEEN", 17, None, False)
        NumberHelper._m_nums.addStr("SEVENTEENTH", 17 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ВОСЕМНАДЦАТЬ", 18, None, False)
        NumberHelper._m_nums.addStr("ВОСЕМНАДЦАТЫЙ", 18 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ВОСЕМНАДЦАТИ", 18, None, False)
        NumberHelper._m_nums.addStr("ВІСІМНАДЦЯТЬ", 18, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВІСІМНАДЦЯТИЙ", 18 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВІСІМНАДЦЯТИ", 18, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("EIGHTEEN", 18, None, False)
        NumberHelper._m_nums.addStr("EIGHTEENTH", 18 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦАТЬ", 19, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦАТЫЙ", 19 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦАТИ", 19, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦЯТЬ", 19, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦЯТИЙ", 19 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯТНАДЦЯТИ", 19, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("NINETEEN", 19, None, False)
        NumberHelper._m_nums.addStr("NINETEENTH", 19 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДВАДЦАТЬ", 20, None, False)
        NumberHelper._m_nums.addStr("ДВАДЦАТЫЙ", 20 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДВАДЦАТИ", 20, None, False)
        NumberHelper._m_nums.addStr("ДВАДЦЯТЬ", 20, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВАДЦЯТИЙ", 20 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВАДЦЯТИ", 20, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("TWENTY", 20, None, False)
        NumberHelper._m_nums.addStr("TWENTIETH", 20 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ТРИДЦАТЬ", 30, None, False)
        NumberHelper._m_nums.addStr("ТРИДЦАТЫЙ", 30 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ТРИДЦАТИ", 30, None, False)
        NumberHelper._m_nums.addStr("ТРИДЦЯТЬ", 30, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРИДЦЯТИЙ", 30 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРИДЦЯТИ", 30, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("THIRTY", 30, None, False)
        NumberHelper._m_nums.addStr("THIRTIETH", 30 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("СОРОК", 40, None, False)
        NumberHelper._m_nums.addStr("СОРОКОВОЙ", 40 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("СОРОКА", 40, None, False)
        NumberHelper._m_nums.addStr("СОРОК", 40, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СОРОКОВИЙ", 40 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FORTY", 40, None, False)
        NumberHelper._m_nums.addStr("FORTIETH", 40 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ПЯТЬДЕСЯТ", 50, None, False)
        NumberHelper._m_nums.addStr("ПЯТИДЕСЯТЫЙ", 50 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ПЯТИДЕСЯТИ", 50, None, False)
        NumberHelper._m_nums.addStr("ПЯТДЕСЯТ", 50, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТДЕСЯТИЙ", 50 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТДЕСЯТИ", 50, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("FIFTY", 50, None, False)
        NumberHelper._m_nums.addStr("FIFTIETH", 50 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ШЕСТЬДЕСЯТ", 60, None, False)
        NumberHelper._m_nums.addStr("ШЕСТИДЕСЯТЫЙ", 60 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ШЕСТИДЕСЯТИ", 60, None, False)
        NumberHelper._m_nums.addStr("ШІСТДЕСЯТ", 60, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШЕСИДЕСЯТЫЙ", 60 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШІСТДЕСЯТИ", 60, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SIXTY", 60, None, False)
        NumberHelper._m_nums.addStr("SIXTIETH", 60 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("СЕМЬДЕСЯТ", 70, None, False)
        NumberHelper._m_nums.addStr("СЕМИДЕСЯТЫЙ", 70 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("СЕМИДЕСЯТИ", 70, None, False)
        NumberHelper._m_nums.addStr("СІМДЕСЯТ", 70, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СІМДЕСЯТИЙ", 70 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СІМДЕСЯТИ", 70, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("SEVENTY", 70, None, False)
        NumberHelper._m_nums.addStr("SEVENTIETH", 70 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("SEVENTIES", 70 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ВОСЕМЬДЕСЯТ", 80, None, False)
        NumberHelper._m_nums.addStr("ВОСЬМИДЕСЯТЫЙ", 80 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ВОСЬМИДЕСЯТИ", 80, None, False)
        NumberHelper._m_nums.addStr("ВІСІМДЕСЯТ", 80, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВОСЬМИДЕСЯТИЙ", 80 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВІСІМДЕСЯТИ", 80, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("EIGHTY", 80, None, False)
        NumberHelper._m_nums.addStr("EIGHTIETH", 80 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("EIGHTIES", 80 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯНОСТО", 90, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯНОСТЫЙ", 90 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯНОСТО", 90, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯНОСТИЙ", 90 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("NINETY", 90, None, False)
        NumberHelper._m_nums.addStr("NINETIETH", 90 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("NINETIES", 90 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("СТО", 100, None, False)
        NumberHelper._m_nums.addStr("СОТЫЙ", 100 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("СТА", 100, None, False)
        NumberHelper._m_nums.addStr("СТО", 100, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СОТИЙ", 100 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("HUNDRED", 100, None, False)
        NumberHelper._m_nums.addStr("HUNDREDTH", 100 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДВЕСТИ", 200, None, False)
        NumberHelper._m_nums.addStr("ДВУХСОТЫЙ", 200 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДВУХСОТ", 200, None, False)
        NumberHelper._m_nums.addStr("ДВІСТІ", 200, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВОХСОТИЙ", 200 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВОХСОТ", 200, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРИСТА", 300, None, False)
        NumberHelper._m_nums.addStr("ТРЕХСОТЫЙ", 300 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ТРЕХСОТ", 300, None, False)
        NumberHelper._m_nums.addStr("ТРИСТА", 300, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРЬОХСОТИЙ", 300 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТРЬОХСОТ", 300, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧЕТЫРЕСТА", 400, None, False)
        NumberHelper._m_nums.addStr("ЧЕТЫРЕХСОТЫЙ", 400 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ЧОТИРИСТА", 400, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ЧОТИРЬОХСОТИЙ", 400 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТЬСОТ", 500, None, False)
        NumberHelper._m_nums.addStr("ПЯТИСОТЫЙ", 500 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ПЯТСОТ", 500, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ПЯТИСОТИЙ", 500 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШЕСТЬСОТ", 600, None, False)
        NumberHelper._m_nums.addStr("ШЕСТИСОТЫЙ", 600 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ШІСТСОТ", 600, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ШЕСТИСОТИЙ", 600 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СЕМЬСОТ", 700, None, False)
        NumberHelper._m_nums.addStr("СЕМИСОТЫЙ", 700 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("СІМСОТ", 700, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("СЕМИСОТИЙ", 700 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВОСЕМЬСОТ", 800, None, False)
        NumberHelper._m_nums.addStr("ВОСЕМЬСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ВОСЬМИСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ВІСІМСОТ", 800, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ВОСЬМИСОТЫЙ", 800 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯТЬСОТ", 900, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТЬСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТИСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТСОТ", 900, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДЕВЯТЬСОТЫЙ", 900 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДЕВЯТИСОТИЙ", 900 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТЫС", 1000, None, False)
        NumberHelper._m_nums.addStr("ТЫСЯЧА", 1000, None, False)
        NumberHelper._m_nums.addStr("ТЫСЯЧНЫЙ", 1000 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ТИС", 1000, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТИСЯЧА", 1000, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ТИСЯЧНИЙ", 1000 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("ДВУХТЫСЯЧНЫЙ", 2000 | NumberHelper.__pril_num_tag_bit, None, False)
        NumberHelper._m_nums.addStr("ДВОХТИСЯЧНИЙ", 2000 | NumberHelper.__pril_num_tag_bit, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("МИЛЛИОН", 1000000, None, False)
        NumberHelper._m_nums.addStr("МЛН", 1000000, None, False)
        NumberHelper._m_nums.addStr("МІЛЬЙОН", 1000000, MorphLang.UA, False)
        NumberHelper._m_nums.addStr("МИЛЛИАРД", 1000000000, None, False)
        NumberHelper._m_nums.addStr("МІЛЬЯРД", 1000000000, MorphLang.UA, False)
        NumberHelper.__m_after_points = TerminCollection()
        t = Termin._new117("ПОЛОВИНА", .5)
        t.addVariant("ОДНА ВТОРАЯ", False)
        t.addVariant("ПОЛ", False)
        NumberHelper.__m_after_points.add(t)
        t = Termin._new117("ТРЕТЬ", .33)
        t.addVariant("ОДНА ТРЕТЬ", False)
        NumberHelper.__m_after_points.add(t)
        t = Termin._new117("ЧЕТВЕРТЬ", .25)
        t.addVariant("ОДНА ЧЕТВЕРТАЯ", False)
        NumberHelper.__m_after_points.add(t)
        t = Termin._new117("ПЯТАЯ ЧАСТЬ", .2)
        t.addVariant("ОДНА ПЯТАЯ", False)
        NumberHelper.__m_after_points.add(t)
    
    _m_nums = None
    
    __m_after_points = None
    
    # static constructor for class NumberHelper
    @staticmethod
    def _static_ctor():
        NumberHelper.__m_samples = ["ДЕСЯТЫЙ", "ПЕРВЫЙ", "ВТОРОЙ", "ТРЕТИЙ", "ЧЕТВЕРТЫЙ", "ПЯТЫЙ", "ШЕСТОЙ", "СЕДЬМОЙ", "ВОСЬМОЙ", "ДЕВЯТЫЙ"]
        NumberHelper.__m_man_number_words = ["ПЕРВЫЙ", "ВТОРОЙ", "ТРЕТИЙ", "ЧЕТВЕРТЫЙ", "ПЯТЫЙ", "ШЕСТОЙ", "СЕДЬМОЙ", "ВОСЬМОЙ", "ДЕВЯТЫЙ", "ДЕСЯТЫЙ", "ОДИННАДЦАТЫЙ", "ДВЕНАДЦАТЫЙ", "ТРИНАДЦАТЫЙ", "ЧЕТЫРНАДЦАТЫЙ", "ПЯТНАДЦАТЫЙ", "ШЕСТНАДЦАТЫЙ", "СЕМНАДЦАТЫЙ", "ВОСЕМНАДЦАТЫЙ", "ДЕВЯТНАДЦАТЫЙ"]
        NumberHelper.__m_neutral_number_words = ["ПЕРВОЕ", "ВТОРОЕ", "ТРЕТЬЕ", "ЧЕТВЕРТОЕ", "ПЯТОЕ", "ШЕСТОЕ", "СЕДЬМОЕ", "ВОСЬМОЕ", "ДЕВЯТОЕ", "ДЕСЯТОЕ", "ОДИННАДЦАТОЕ", "ДВЕНАДЦАТОЕ", "ТРИНАДЦАТОЕ", "ЧЕТЫРНАДЦАТОЕ", "ПЯТНАДЦАТОЕ", "ШЕСТНАДЦАТОЕ", "СЕМНАДЦАТОЕ", "ВОСЕМНАДЦАТОЕ", "ДЕВЯТНАДЦАТОЕ"]
        NumberHelper.__m_woman_number_words = ["ПЕРВАЯ", "ВТОРАЯ", "ТРЕТЬЯ", "ЧЕТВЕРТАЯ", "ПЯТАЯ", "ШЕСТАЯ", "СЕДЬМАЯ", "ВОСЬМАЯ", "ДЕВЯТАЯ", "ДЕСЯТАЯ", "ОДИННАДЦАТАЯ", "ДВЕНАДЦАТАЯ", "ТРИНАДЦАТАЯ", "ЧЕТЫРНАДЦАТАЯ", "ПЯТНАДЦАТАЯ", "ШЕСТНАДЦАТАЯ", "СЕМНАДЦАТАЯ", "ВОСЕМНАДЦАТАЯ", "ДЕВЯТНАДЦАТАЯ"]
        NumberHelper.__m_plural_number_words = ["ПЕРВЫЕ", "ВТОРЫЕ", "ТРЕТЬИ", "ЧЕТВЕРТЫЕ", "ПЯТЫЕ", "ШЕСТЫЕ", "СЕДЬМЫЕ", "ВОСЬМЫЕ", "ДЕВЯТЫЕ", "ДЕСЯТЫЕ", "ОДИННАДЦАТЫЕ", "ДВЕНАДЦАТЫЕ", "ТРИНАДЦАТЫЕ", "ЧЕТЫРНАДЦАТЫЕ", "ПЯТНАДЦАТЫЕ", "ШЕСТНАДЦАТЫЕ", "СЕМНАДЦАТЫЕ", "ВОСЕМНАДЦАТЫЕ", "ДЕВЯТНАДЦАТЫЕ"]
        NumberHelper.__m_dec_dumber_words = ["ДВАДЦАТЬ", "ТРИДЦАТЬ", "СОРОК", "ПЯТЬДЕСЯТ", "ШЕСТЬДЕСЯТ", "СЕМЬДЕСЯТ", "ВОСЕМЬДЕСЯТ", "ДЕВЯНОСТО"]
        NumberHelper.__m_man_dec_dumber_words = ["ДВАДЦАТЫЙ", "ТРИДЦАТЫЙ", "СОРОКОВОЙ", "ПЯТЬДЕСЯТЫЙ", "ШЕСТЬДЕСЯТЫЙ", "СЕМЬДЕСЯТЫЙ", "ВОСЕМЬДЕСЯТЫЙ", "ДЕВЯНОСТЫЙ"]
        NumberHelper.__m_woman_dec_dumber_words = ["ДВАДЦАТАЯ", "ТРИДЦАТАЯ", "СОРОКОВАЯ", "ПЯТЬДЕСЯТАЯ", "ШЕСТЬДЕСЯТАЯ", "СЕМЬДЕСЯТАЯ", "ВОСЕМЬДЕСЯТАЯ", "ДЕВЯНОСТАЯ"]
        NumberHelper.__m_neutral_dec_dumber_words = ["ДВАДЦАТОЕ", "ТРИДЦАТОЕ", "СОРОКОВОЕ", "ПЯТЬДЕСЯТОЕ", "ШЕСТЬДЕСЯТОЕ", "СЕМЬДЕСЯТОЕ", "ВОСЕМЬДЕСЯТОЕ", "ДЕВЯНОСТОЕ"]
        NumberHelper.__m_plural_dec_dumber_words = ["ДВАДЦАТЫЕ", "ТРИДЦАТЫЕ", "СОРОКОВЫЕ", "ПЯТЬДЕСЯТЫЕ", "ШЕСТЬДЕСЯТЫЕ", "СЕМЬДЕСЯТЫЕ", "ВОСЕМЬДЕСЯТЫЕ", "ДЕВЯНОСТЫЕ"]
        NumberHelper._m_romans = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX"]

NumberHelper._static_ctor()