﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.NumberToken import NumberToken
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.Token import Token
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.Termin import Termin

class TerminCollection:
    """ Коллекций некоторых обозначений, терминов """
    
    class CharNode:
        
        def __init__(self) -> None:
            self.children = None;
            self.termins = None;
    
    def __init__(self) -> None:
        self.termins = list()
        self.all_add_strs_normalized = False
        self.__m_root = TerminCollection.CharNode()
        self.__m_root_ua = TerminCollection.CharNode()
        self.__m_hash1 = dict()
        self.__m_hash_canonic = None
    
    def add(self, term : 'Termin') -> None:
        """ Добавить термин. После добавления в термин нельзя вносить изменений,
         кроме как в значения Tag и Tag2 (иначе потом нужно вызвать Reindex)
        
        Args:
            term(Termin): 
        """
        self.termins.append(term)
        self.__m_hash_canonic = (None)
        self.reindex(term)
    
    def addStr(self, termins_ : str, tag : object=None, lang : 'MorphLang'=None, is_normal_text : bool=False) -> 'Termin':
        """ Добавить строку вместе с морфологическими вариантами
        
        Args:
            termins_(str): 
            tag(object): 
            lang(MorphLang): 
        
        """
        t = Termin(termins_, lang, is_normal_text or self.all_add_strs_normalized)
        t.tag = tag
        if (tag is not None and len(t.terms) == 1): 
            pass
        self.add(t)
        return t
    
    def __getRoot(self, lang : 'MorphLang', is_lat : bool) -> 'CharNode':
        if (lang is not None and lang.is_ua and not lang.is_ru): 
            return self.__m_root_ua
        return self.__m_root
    
    def reindex(self, t : 'Termin') -> None:
        """ Переиндексировать термин (если после добавления у него что-либо поменялось)
        
        Args:
            t(Termin): 
        """
        if (t is None): 
            return
        if (len(t.terms) > 20): 
            pass
        if (t.acronym_smart is not None): 
            self.__addToHash1(ord(t.acronym_smart[0]), t)
        if (t.abridges is not None): 
            for a in t.abridges: 
                if (len(a.parts[0].value) == 1): 
                    self.__addToHash1(ord(a.parts[0].value[0]), t)
        for v in t._getHashVariants(): 
            self.__AddToTree(v, t)
        if (t.additional_vars is not None): 
            for av in t.additional_vars: 
                av.ignore_terms_order = t.ignore_terms_order
                for v in av._getHashVariants(): 
                    self.__AddToTree(v, t)
    
    def remove(self, t : 'Termin') -> None:
        for v in t._getHashVariants(): 
            self.__RemoveFromTree(v, t)
        for li in self.__m_hash1.values(): 
            for tt in li: 
                if (tt == t): 
                    li.remove(tt)
                    break
        i = Utils.indexOfList(self.termins, t, 0)
        if (i >= 0): 
            del self.termins[i]
    
    def __AddToTree(self, key : str, t : 'Termin') -> None:
        if (key is None): 
            return
        nod = self.__getRoot(t.lang, t.lang.is_undefined and LanguageHelper.isLatin(key))
        i = 0
        while i < len(key): 
            ch = ord(key[i])
            if (nod.children is None): 
                nod.children = dict()
            wrapnn612 = RefOutArgWrapper(None)
            inoutres613 = Utils.tryGetValue(nod.children, ch, wrapnn612)
            nn = wrapnn612.value
            if (not inoutres613): 
                nn = TerminCollection.CharNode()
                nod.children[ch] = nn
            nod = nn
            i += 1
        if (nod.termins is None): 
            nod.termins = list()
        if (not t in nod.termins): 
            nod.termins.append(t)
    
    def __RemoveFromTree(self, key : str, t : 'Termin') -> None:
        if (key is None): 
            return
        nod = self.__getRoot(t.lang, t.lang.is_undefined and LanguageHelper.isLatin(key))
        i = 0
        while i < len(key): 
            ch = ord(key[i])
            if (nod.children is None): 
                return
            wrapnn614 = RefOutArgWrapper(None)
            inoutres615 = Utils.tryGetValue(nod.children, ch, wrapnn614)
            nn = wrapnn614.value
            if (not inoutres615): 
                return
            nod = nn
            i += 1
        if (nod.termins is None): 
            return
        if (t in nod.termins): 
            nod.termins.remove(t)
    
    def __FindInTree(self, key : str, lang : 'MorphLang') -> typing.List['Termin']:
        if (key is None): 
            return None
        nod = self.__getRoot(lang, ((lang is None or lang.is_undefined)) and LanguageHelper.isLatin(key))
        i = 0
        while i < len(key): 
            ch = ord(key[i])
            if (nod.children is None): 
                return None
            wrapnn616 = RefOutArgWrapper(None)
            inoutres617 = Utils.tryGetValue(nod.children, ch, wrapnn616)
            nn = wrapnn616.value
            if (not inoutres617): 
                return None
            nod = nn
            i += 1
        return nod.termins
    
    def __addToHash1(self, key : int, t : 'Termin') -> None:
        li = None
        wrapli618 = RefOutArgWrapper(None)
        inoutres619 = Utils.tryGetValue(self.__m_hash1, key, wrapli618)
        li = wrapli618.value
        if (not inoutres619): 
            li = list()
            self.__m_hash1[key] = li
        if (not t in li): 
            li.append(t)
    
    def find(self, key : str) -> 'Termin':
        if (Utils.isNullOrEmpty(key)): 
            return None
        li = [ ]
        if (LanguageHelper.isLatinChar(key[0])): 
            li = self.__FindInTree(key, MorphLang.EN)
        else: 
            li = self.__FindInTree(key, MorphLang.RU)
            if (li is None): 
                li = self.__FindInTree(key, MorphLang.UA)
        return (li[0] if li is not None and len(li) > 0 else None)
    
    def tryParse(self, token : 'Token', pars : 'TerminParseAttr'=TerminParseAttr.NO) -> 'TerminToken':
        """ Попытка привязать к аналитическому контейнеру с указанной позиции
        
        Args:
            token(Token): начальная позиция
            pars(TerminParseAttr): параметры выделения
        
        """
        if (len(self.termins) == 0): 
            return None
        li = self.tryParseAll(token, pars)
        if (li is not None): 
            return li[0]
        else: 
            return None
    
    def tryParseAll(self, token : 'Token', pars : 'TerminParseAttr'=TerminParseAttr.NO) -> typing.List['TerminToken']:
        """ Попытка привязать все возможные варианты
        
        Args:
            token(Token): 
            pars(TerminParseAttr): параметры выделения
        
        """
        if (token is None): 
            return None
        re = self.__TryAttachAll_(token, pars, False)
        if (re is None and token.morph.language.is_ua): 
            re = self.__TryAttachAll_(token, pars, True)
        return re
    
    def __TryAttachAll_(self, token : 'Token', pars : 'TerminParseAttr'=TerminParseAttr.NO, main_root : bool=False) -> typing.List['TerminToken']:
        if (len(self.termins) == 0 or token is None): 
            return None
        s = None
        tt = Utils.asObjectOrNull(token, TextToken)
        if (tt is None and (isinstance(token, ReferentToken))): 
            tt = (Utils.asObjectOrNull((token).begin_token, TextToken))
        res = None
        was_vars = False
        root = (self.__m_root if main_root else self.__getRoot(token.morph.language, token.chars.is_latin_letter))
        if (tt is not None): 
            s = tt.term
            nod = root
            no_vars = False
            len0 = 0
            if ((((pars) & (TerminParseAttr.TERMONLY))) != (TerminParseAttr.NO)): 
                pass
            elif (tt.invariant_prefix_length <= len(s)): 
                len0 = (tt.invariant_prefix_length)
                i = 0
                while i < tt.invariant_prefix_length: 
                    ch = ord(s[i])
                    if (nod.children is None): 
                        no_vars = True
                        break
                    wrapnn620 = RefOutArgWrapper(None)
                    inoutres621 = Utils.tryGetValue(nod.children, ch, wrapnn620)
                    nn = wrapnn620.value
                    if (not inoutres621): 
                        no_vars = True
                        break
                    nod = nn
                    i += 1
            if (not no_vars): 
                wrapres626 = RefOutArgWrapper(res)
                inoutres627 = self.__manageVar(token, pars, s, nod, len0, wrapres626)
                res = wrapres626.value
                if (inoutres627): 
                    was_vars = True
                i = 0
                first_pass2813 = True
                while True:
                    if first_pass2813: first_pass2813 = False
                    else: i += 1
                    if (not (i < tt.morph.items_count)): break
                    if ((((pars) & (TerminParseAttr.TERMONLY))) != (TerminParseAttr.NO)): 
                        continue
                    wf = Utils.asObjectOrNull(tt.morph.getIndexerItem(i), MorphWordForm)
                    if (wf is None): 
                        continue
                    if ((((pars) & (TerminParseAttr.INDICTIONARYONLY))) != (TerminParseAttr.NO)): 
                        if (not wf.is_in_dictionary): 
                            continue
                    ok = True
                    if (wf.normal_case is None or wf.normal_case == s): 
                        ok = False
                    else: 
                        j = 0
                        while j < i: 
                            wf2 = Utils.asObjectOrNull(tt.morph.getIndexerItem(j), MorphWordForm)
                            if (wf2 is not None): 
                                if (wf2.normal_case == wf.normal_case or wf2.normal_full == wf.normal_case): 
                                    break
                            j += 1
                        if (j < i): 
                            ok = False
                    if (ok): 
                        wrapres622 = RefOutArgWrapper(res)
                        inoutres623 = self.__manageVar(token, pars, wf.normal_case, nod, tt.invariant_prefix_length, wrapres622)
                        res = wrapres622.value
                        if (inoutres623): 
                            was_vars = True
                    if (wf.normal_full is None or wf.normal_full == wf.normal_case or wf.normal_full == s): 
                        continue
                    j = 0
                    while j < i: 
                        wf2 = Utils.asObjectOrNull(tt.morph.getIndexerItem(j), MorphWordForm)
                        if (wf2 is not None and wf2.normal_full == wf.normal_full): 
                            break
                        j += 1
                    if (j < i): 
                        continue
                    wrapres624 = RefOutArgWrapper(res)
                    inoutres625 = self.__manageVar(token, pars, wf.normal_full, nod, tt.invariant_prefix_length, wrapres624)
                    res = wrapres624.value
                    if (inoutres625): 
                        was_vars = True
        elif (isinstance(token, NumberToken)): 
            wrapres628 = RefOutArgWrapper(res)
            inoutres629 = self.__manageVar(token, pars, str((token).value), root, 0, wrapres628)
            res = wrapres628.value
            if (inoutres629): 
                was_vars = True
        else: 
            return None
        if (not was_vars and s is not None and len(s) == 1): 
            vars0_ = [ ]
            wrapvars630 = RefOutArgWrapper(None)
            inoutres631 = Utils.tryGetValue(self.__m_hash1, ord(s[0]), wrapvars630)
            vars0_ = wrapvars630.value
            if (inoutres631): 
                for t in vars0_: 
                    if (not t.lang.is_undefined): 
                        if (not token.morph.language.is_undefined): 
                            if (((token.morph.language) & t.lang).is_undefined): 
                                continue
                    ar = t.tryParse(tt, TerminParseAttr.NO)
                    if (ar is None): 
                        continue
                    ar.termin = t
                    if (res is None): 
                        res = list()
                        res.append(ar)
                    elif (ar.tokens_count > res[0].tokens_count): 
                        res.clear()
                        res.append(ar)
                    elif (ar.tokens_count == res[0].tokens_count): 
                        res.append(ar)
        if (res is not None): 
            ii = 0
            max0_ = 0
            i = 0
            while i < len(res): 
                if (res[i].length_char > max0_): 
                    max0_ = res[i].length_char
                    ii = i
                i += 1
            if (ii > 0): 
                v = res[ii]
                del res[ii]
                res.insert(0, v)
        return res
    
    def __manageVar(self, token : 'Token', pars : 'TerminParseAttr', v : str, nod : 'CharNode', i0 : int, res : typing.List['TerminToken']) -> bool:
        i = i0
        while i < len(v): 
            ch = ord(v[i])
            if (nod.children is None): 
                return False
            wrapnn632 = RefOutArgWrapper(None)
            inoutres633 = Utils.tryGetValue(nod.children, ch, wrapnn632)
            nn = wrapnn632.value
            if (not inoutres633): 
                return False
            nod = nn
            i += 1
        vars0_ = nod.termins
        if (vars0_ is None or len(vars0_) == 0): 
            return False
        for t in vars0_: 
            ar = t.tryParse(token, pars)
            if (ar is not None): 
                ar.termin = t
                if (res.value is None): 
                    res.value = list()
                    res.value.append(ar)
                elif (ar.tokens_count > res.value[0].tokens_count): 
                    res.value.clear()
                    res.value.append(ar)
                elif (ar.tokens_count == res.value[0].tokens_count): 
                    j = 0
                    while j < len(res.value): 
                        if (res.value[j].termin == ar.termin): 
                            break
                        j += 1
                    if (j >= len(res.value)): 
                        res.value.append(ar)
            if (t.additional_vars is not None): 
                for av in t.additional_vars: 
                    ar = av.tryParse(token, pars)
                    if (ar is None): 
                        continue
                    ar.termin = t
                    if (res.value is None): 
                        res.value = list()
                        res.value.append(ar)
                    elif (ar.tokens_count > res.value[0].tokens_count): 
                        res.value.clear()
                        res.value.append(ar)
                    elif (ar.tokens_count == res.value[0].tokens_count): 
                        j = 0
                        while j < len(res.value): 
                            if (res.value[j].termin == ar.termin): 
                                break
                            j += 1
                        if (j >= len(res.value)): 
                            res.value.append(ar)
        return len(v) > 1
    
    def tryAttach(self, termin : 'Termin') -> typing.List['Termin']:
        """ Поискать эквивалентные термины
        
        Args:
            termin(Termin): 
        
        """
        res = None
        for v in termin._getHashVariants(): 
            vars0_ = self.__FindInTree(v, termin.lang)
            if (vars0_ is None): 
                continue
            for t in vars0_: 
                if (t.isEqual(termin)): 
                    if (res is None): 
                        res = list()
                    if (not t in res): 
                        res.append(t)
        return res
    
    def tryAttachStr(self, termin : str, lang : 'MorphLang'=None) -> typing.List['Termin']:
        return self.__FindInTree(termin, lang)
    
    def findTerminByCanonicText(self, text : str) -> typing.List['Termin']:
        if (self.__m_hash_canonic is None): 
            self.__m_hash_canonic = dict()
            for t in self.termins: 
                ct = t.canonic_text
                li = [ ]
                wrapli634 = RefOutArgWrapper(None)
                inoutres635 = Utils.tryGetValue(self.__m_hash_canonic, ct, wrapli634)
                li = wrapli634.value
                if (not inoutres635): 
                    li = list()
                    self.__m_hash_canonic[ct] = li
                if (not t in li): 
                    li.append(t)
        res = [ ]
        wrapres636 = RefOutArgWrapper(None)
        inoutres637 = Utils.tryGetValue(self.__m_hash_canonic, text, wrapres636)
        res = wrapres636.value
        if (not inoutres637): 
            return None
        else: 
            return res