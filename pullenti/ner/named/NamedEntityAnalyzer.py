﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Token import Token
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.Referent import Referent
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.named.NamedEntityKind import NamedEntityKind
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.named.internal.MetaNamedEntity import MetaNamedEntity
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.named.internal.NamedItemToken import NamedItemToken
from pullenti.ner.named.NamedEntityReferent import NamedEntityReferent
from pullenti.ner.geo.GeoReferent import GeoReferent

class NamedEntityAnalyzer(Analyzer):
    """ Анализатор мелких именованных сущностей (планеты, памятники, здания, местоположения, планеты и пр.) """
    
    ANALYZER_NAME = "NAMEDENTITY"
    
    @property
    def name(self) -> str:
        return NamedEntityAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Мелкие именованные сущности"
    
    @property
    def description(self) -> str:
        return "Планеты, памятники, здания, местоположения, планеты и пр."
    
    def clone(self) -> 'Analyzer':
        return NamedEntityAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaNamedEntity.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[Utils.enumToString(NamedEntityKind.MONUMENT)] = EpNerCoreInternalResourceHelper.getBytes("monument.png")
        res[Utils.enumToString(NamedEntityKind.PLANET)] = EpNerCoreInternalResourceHelper.getBytes("planet.png")
        res[Utils.enumToString(NamedEntityKind.LOCATION)] = EpNerCoreInternalResourceHelper.getBytes("location.png")
        res[Utils.enumToString(NamedEntityKind.BUILDING)] = EpNerCoreInternalResourceHelper.getBytes("building.png")
        return res
    
    def createReferent(self, type0_ : str) -> 'Referent':
        if (type0_ == NamedEntityReferent.OBJ_TYPENAME): 
            return NamedEntityReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return [GeoReferent.OBJ_TYPENAME, "ORGANIZATION", "PERSON"]
    
    @property
    def progress_weight(self) -> int:
        return 3
    
    def createAnalyzerData(self) -> 'AnalyzerData':
        return AnalyzerDataWithOntology()
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = Utils.asObjectOrNull(kit.getAnalyzerData(self), AnalyzerDataWithOntology)
        t = kit.first_token
        first_pass3042 = True
        while True:
            if first_pass3042: first_pass3042 = False
            else: t = t.next0_
            if (not (t is not None)): break
            li = NamedItemToken.tryParseList(t, ad.local_ontology)
            if (li is None or len(li) == 0): 
                continue
            rt = NamedEntityAnalyzer.__tryAttach(li)
            if (rt is not None): 
                rt.referent = ad.registerReferent(rt.referent)
                kit.embedToken(rt)
                t = (rt)
                continue
    
    def _processReferent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        li = NamedItemToken.tryParseList(begin, None)
        if (li is None or len(li) == 0): 
            return None
        rt = NamedEntityAnalyzer.__tryAttach(li)
        if (rt is None): 
            return None
        rt.data = begin.kit.getAnalyzerData(self)
        return rt
    
    @staticmethod
    def __canBeRef(ki : 'NamedEntityKind', re : 'Referent') -> bool:
        if (re is None): 
            return False
        if (ki == NamedEntityKind.MONUMENT): 
            if (re.type_name == "PERSON" or re.type_name == "PERSONPROPERTY"): 
                return True
        elif (ki == NamedEntityKind.LOCATION): 
            if (isinstance(re, GeoReferent)): 
                geo_ = Utils.asObjectOrNull(re, GeoReferent)
                if (geo_.is_region or geo_.is_state): 
                    return True
        elif (ki == NamedEntityKind.BUILDING): 
            if (re.type_name == "ORGANIZATION"): 
                return True
        return False
    
    @staticmethod
    def __tryAttach(toks : typing.List['NamedItemToken']) -> 'ReferentToken':
        typ = None
        re = None
        nams = None
        ki = NamedEntityKind.UNDEFINED
        i = 0
        while i < len(toks): 
            if (toks[i].type_value is not None): 
                if (nams is not None and toks[i].name_value is not None): 
                    break
                if (typ is None): 
                    typ = toks[i]
                    ki = typ.kind
                elif (typ.kind != toks[i].kind): 
                    break
            if (toks[i].name_value is not None): 
                if (typ is not None and toks[i].kind != NamedEntityKind.UNDEFINED and toks[i].kind != typ.kind): 
                    break
                if (nams is None): 
                    nams = list()
                elif (nams[0].is_wellknown != toks[i].is_wellknown): 
                    break
                if (ki == NamedEntityKind.UNDEFINED): 
                    ki = toks[i].kind
                nams.append(toks[i])
            if (toks[i].type_value is None and toks[i].name_value is None): 
                break
            if (re is None and NamedEntityAnalyzer.__canBeRef(ki, toks[i].ref)): 
                re = toks[i]
            i += 1
        if ((i < len(toks)) and toks[i].ref is not None): 
            if (NamedEntityAnalyzer.__canBeRef(ki, toks[i].ref)): 
                re = toks[i]
                i += 1
        ok = False
        if (typ is not None): 
            if (nams is None): 
                if (re is None): 
                    ok = False
                else: 
                    ok = True
            elif ((nams[0].begin_char < typ.end_char) and not nams[0].is_wellknown): 
                if (re is not None): 
                    ok = True
                elif ((nams[0].chars.is_capital_upper and not MiscHelper.canBeStartOfSentence(nams[0].begin_token) and typ.morph.number != MorphNumber.PLURAL) and typ.morph.case_.is_nominative): 
                    ok = True
            else: 
                ok = True
        elif (nams is not None): 
            if (len(nams) == 1 and nams[0].chars.is_all_lower): 
                pass
            elif (nams[0].is_wellknown): 
                ok = True
        if (not ok or ki == NamedEntityKind.UNDEFINED): 
            return None
        nam = NamedEntityReferent._new1642(ki)
        if (typ is not None): 
            nam.addSlot(NamedEntityReferent.ATTR_TYPE, typ.type_value.lower(), False, 0)
        if (nams is not None): 
            if (len(nams) == 1 and nams[0].is_wellknown and nams[0].type_value is not None): 
                nam.addSlot(NamedEntityReferent.ATTR_TYPE, nams[0].type_value.lower(), False, 0)
            if (typ is not None and (typ.end_char < nams[0].begin_char)): 
                str0_ = MiscHelper.getTextValue(nams[0].begin_token, nams[len(nams) - 1].end_token, GetTextAttr.NO)
                nam.addSlot(NamedEntityReferent.ATTR_NAME, str0_, False, 0)
            tmp = io.StringIO()
            for n in nams: 
                if (tmp.tell() > 0): 
                    print(' ', end="", file=tmp)
                print(n.name_value, end="", file=tmp)
            nam.addSlot(NamedEntityReferent.ATTR_NAME, Utils.toStringStringIO(tmp), False, 0)
        if (re is not None): 
            nam.addSlot(NamedEntityReferent.ATTR_REF, re.ref, False, 0)
        return ReferentToken(nam, toks[0].begin_token, toks[i - 1].end_token)
    
    __m_inited = None
    
    @staticmethod
    def initialize() -> None:
        if (NamedEntityAnalyzer.__m_inited): 
            return
        NamedEntityAnalyzer.__m_inited = True
        try: 
            MetaNamedEntity.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            NamedItemToken._initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.registerAnalyzer(NamedEntityAnalyzer())