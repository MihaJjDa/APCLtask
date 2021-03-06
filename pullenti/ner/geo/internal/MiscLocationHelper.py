﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.TextToken import TextToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken

class MiscLocationHelper:
    
    @staticmethod
    def checkGeoObjectBefore(t : 'Token') -> bool:
        if (t is None): 
            return False
        tt = t.previous
        first_pass2896 = True
        while True:
            if first_pass2896: first_pass2896 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if ((tt.isCharOf(",.;:") or tt.is_hiphen or tt.is_and) or tt.morph.class0_.is_conjunction or tt.morph.class0_.is_preposition): 
                continue
            if (tt.isValue("ТЕРРИТОРИЯ", "ТЕРИТОРІЯ")): 
                continue
            if ((tt.isValue("ПРОЖИВАТЬ", "ПРОЖИВАТИ") or tt.isValue("РОДИТЬ", "НАРОДИТИ") or tt.isValue("ЗАРЕГИСТРИРОВАТЬ", "ЗАРЕЄСТРУВАТИ")) or tt.isValue("АДРЕС", None)): 
                return True
            if (tt.isValue("УРОЖЕНЕЦ", "УРОДЖЕНЕЦЬ") or tt.isValue("УРОЖЕНКА", "УРОДЖЕНКА")): 
                return True
            rt = Utils.asObjectOrNull(tt, ReferentToken)
            if (rt is None): 
                break
            if ((isinstance(rt.referent, GeoReferent)) or (isinstance(rt.referent, AddressReferent)) or (isinstance(rt.referent, StreetReferent))): 
                return True
            break
        if (t.previous is not None and t.previous.previous is not None): 
            pass
        return False
    
    @staticmethod
    def checkGeoObjectAfter(t : 'Token') -> bool:
        if (t is None): 
            return False
        cou = 0
        tt = t.next0_
        first_pass2897 = True
        while True:
            if first_pass2897: first_pass2897 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if ((tt.isCharOf(",.;") or tt.is_hiphen or tt.morph.class0_.is_conjunction) or tt.morph.class0_.is_preposition): 
                continue
            if (tt.isValue("ТЕРРИТОРИЯ", "ТЕРИТОРІЯ")): 
                continue
            rt = Utils.asObjectOrNull(tt, ReferentToken)
            if (rt is None): 
                if ((isinstance(tt, TextToken)) and tt.length_char > 2 and cou == 0): 
                    cou += 1
                    continue
                else: 
                    break
            if ((isinstance(rt.referent, GeoReferent)) or (isinstance(rt.referent, AddressReferent)) or (isinstance(rt.referent, StreetReferent))): 
                return True
            break
        return False
    
    @staticmethod
    def checkNearBefore(t : 'Token') -> 'Token':
        if (t is None or not t.morph.class0_.is_preposition): 
            return None
        if (t.isValue("У", None) or t.isValue("ОКОЛО", None) or t.isValue("ВБЛИЗИ", None)): 
            return t
        if (t.isValue("ОТ", None) and t.previous is not None): 
            if (t.previous.isValue("НЕДАЛЕКО", None) or t.previous.isValue("ВБЛИЗИ", None) or t.previous.isValue("НЕПОДАЛЕКУ", None)): 
                return t.previous
        return None
    
    @staticmethod
    def checkUnknownRegion(t : 'Token') -> 'Token':
        """ Проверка, что здесь какой-то непонятный регион типа "Европа", "Средняя Азия", "Дикий запад" и т.п.
        
        Args:
            t(Token): 
        
        """
        if (not ((isinstance(t, TextToken)))): 
            return None
        npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
        if (npt is None): 
            return None
        if (TerrItemToken._m_unknown_regions.tryParse(npt.end_token, TerminParseAttr.FULLWORDSONLY) is not None): 
            return npt.end_token
        return None
    
    @staticmethod
    def getStdAdjFull(t : 'Token', gen : 'MorphGender', num : 'MorphNumber', strict : bool) -> typing.List[str]:
        if (not ((isinstance(t, TextToken)))): 
            return None
        return MiscLocationHelper.getStdAdjFullStr((t).term, gen, num, strict)
    
    @staticmethod
    def getStdAdjFullStr(v : str, gen : 'MorphGender', num : 'MorphNumber', strict : bool) -> typing.List[str]:
        res = list()
        if (v.startswith("Б")): 
            if (num == MorphNumber.PLURAL): 
                res.append("БОЛЬШИЕ")
                return res
            if (not strict and (((num) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                res.append("БОЛЬШИЕ")
            if ((((gen) & (MorphGender.FEMINIE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("БОЛЬШАЯ")
            if ((((gen) & (MorphGender.MASCULINE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("БОЛЬШОЙ")
            if ((((gen) & (MorphGender.NEUTER))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("БОЛЬШОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("М")): 
            if (num == MorphNumber.PLURAL): 
                res.append("МАЛЫЕ")
                return res
            if (not strict and (((num) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                res.append("МАЛЫЕ")
            if ((((gen) & (MorphGender.FEMINIE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("МАЛАЯ")
            if ((((gen) & (MorphGender.MASCULINE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("МАЛЫЙ")
            if ((((gen) & (MorphGender.NEUTER))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("МАЛОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("В")): 
            if (num == MorphNumber.PLURAL): 
                res.append("ВЕРХНИЕ")
                return res
            if (not strict and (((num) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                res.append("ВЕРХНИЕ")
            if ((((gen) & (MorphGender.FEMINIE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("ВЕРХНЯЯ")
            if ((((gen) & (MorphGender.MASCULINE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("ВЕРХНИЙ")
            if ((((gen) & (MorphGender.NEUTER))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("ВЕРХНЕЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v == "Н"): 
            r1 = MiscLocationHelper.getStdAdjFullStr("НОВ", gen, num, strict)
            r2 = MiscLocationHelper.getStdAdjFullStr("НИЖ", gen, num, strict)
            if (r1 is None and r2 is None): 
                return None
            if (r1 is None): 
                return r2
            if (r2 is None): 
                return r1
            r1.insert(1, r2[0])
            del r2[0]
            r1.extend(r2)
            return r1
        if (v == "С" or v == "C"): 
            r1 = MiscLocationHelper.getStdAdjFullStr("СТ", gen, num, strict)
            r2 = MiscLocationHelper.getStdAdjFullStr("СР", gen, num, strict)
            if (r1 is None and r2 is None): 
                return None
            if (r1 is None): 
                return r2
            if (r2 is None): 
                return r1
            r1.insert(1, r2[0])
            del r2[0]
            r1.extend(r2)
            return r1
        if (v.startswith("НОВ")): 
            if (num == MorphNumber.PLURAL): 
                res.append("НОВЫЕ")
                return res
            if (not strict and (((num) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                res.append("НОВЫЕ")
            if ((((gen) & (MorphGender.FEMINIE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("НОВАЯ")
            if ((((gen) & (MorphGender.MASCULINE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("НОВЫЙ")
            if ((((gen) & (MorphGender.NEUTER))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("НОВОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("НИЖ")): 
            if (num == MorphNumber.PLURAL): 
                res.append("НИЖНИЕ")
                return res
            if (not strict and (((num) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                res.append("НИЖНИЕ")
            if ((((gen) & (MorphGender.FEMINIE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("НИЖНЯЯ")
            if ((((gen) & (MorphGender.MASCULINE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("НИЖНИЙ")
            if ((((gen) & (MorphGender.NEUTER))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("НИЖНЕЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("СТ")): 
            if (num == MorphNumber.PLURAL): 
                res.append("СТАРЫЕ")
                return res
            if (not strict and (((num) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                res.append("СТАРЫЕ")
            if ((((gen) & (MorphGender.FEMINIE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("СТАРАЯ")
            if ((((gen) & (MorphGender.MASCULINE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("СТАРЫЙ")
            if ((((gen) & (MorphGender.NEUTER))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("СТАРОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("СР")): 
            if (num == MorphNumber.PLURAL): 
                res.append("СРЕДНИЕ")
                return res
            if (not strict and (((num) & (MorphNumber.PLURAL))) != (MorphNumber.UNDEFINED)): 
                res.append("СРЕДНИЕ")
            if ((((gen) & (MorphGender.FEMINIE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("СРЕДНЯЯ")
            if ((((gen) & (MorphGender.MASCULINE))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("СРЕДНИЙ")
            if ((((gen) & (MorphGender.NEUTER))) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("СРЕДНЕЕ")
            if (len(res) > 0): 
                return res
            return None
        return None
    
    @staticmethod
    def getGeoReferentByName(name : str) -> 'GeoReferent':
        """ Прлучить глобальный экземпляр существующего объекта по ALPHA2 или краткой текстовой форме (РФ, РОССИЯ, КИТАЙ ...)
        
        Args:
            name(str): 
        
        """
        res = None
        wrapres1138 = RefOutArgWrapper(None)
        inoutres1139 = Utils.tryGetValue(MiscLocationHelper.__m_geo_ref_by_name, name, wrapres1138)
        res = wrapres1138.value
        if (inoutres1139): 
            return res
        for r in TerrItemToken._m_all_states: 
            if (r.findSlot(None, name, True) is not None): 
                res = (Utils.asObjectOrNull(r, GeoReferent))
                break
        MiscLocationHelper.__m_geo_ref_by_name[name] = res
        return res
    
    __m_geo_ref_by_name = None
    
    @staticmethod
    def tryAttachNordWest(t : 'Token') -> 'MetaToken':
        """ Выделение существительных и прилагательных типа "северо-западное", "южное"
        
        Args:
            t(Token): 
        
        """
        if (not ((isinstance(t, TextToken)))): 
            return None
        tok = MiscLocationHelper.__m_nords.tryParse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        res = MetaToken._new561(t, t, t.morph)
        t1 = None
        if ((t.next0_ is not None and t.next0_.is_hiphen and not t.is_whitespace_after) and not t.is_whitespace_after): 
            t1 = t.next0_.next0_
        elif (t.morph.class0_.is_adjective and (t.whitespaces_after_count < 2)): 
            t1 = t.next0_
        if (t1 is not None): 
            tok = MiscLocationHelper.__m_nords.tryParse(t1, TerminParseAttr.NO)
            if ((tok) is not None): 
                res.end_token = tok.end_token
                res.morph = tok.morph
        return res
    
    @staticmethod
    def _initialize() -> None:
        if (MiscLocationHelper.__m_nords is not None): 
            return
        MiscLocationHelper.__m_nords = TerminCollection()
        for s in ["СЕВЕРНЫЙ", "ЮЖНЫЙ", "ЗАПАДНЫЙ", "ВОСТОЧНЫЙ", "ЦЕНТРАЛЬНЫЙ", "БЛИЖНИЙ", "ДАЛЬНИЙ", "СРЕДНИЙ", "СЕВЕР", "ЮГ", "ЗАПАД", "ВОСТОК", "СЕВЕРО", "ЮГО", "ЗАПАДНО", "ВОСТОЧНО", "СЕВЕРОЗАПАДНЫЙ", "СЕВЕРОВОСТОЧНЫЙ", "ЮГОЗАПАДНЫЙ", "ЮГОВОСТОЧНЫЙ"]: 
            MiscLocationHelper.__m_nords.add(Termin(s, MorphLang.RU, True))
        table = "\nAF\tAFG\nAX\tALA\nAL\tALB\nDZ\tDZA\nAS\tASM\nAD\tAND\nAO\tAGO\nAI\tAIA\nAQ\tATA\nAG\tATG\nAR\tARG\nAM\tARM\nAW\tABW\nAU\tAUS\nAT\tAUT\nAZ\tAZE\nBS\tBHS\nBH\tBHR\nBD\tBGD\nBB\tBRB\nBY\tBLR\nBE\tBEL\nBZ\tBLZ\nBJ\tBEN\nBM\tBMU\nBT\tBTN\nBO\tBOL\nBA\tBIH\nBW\tBWA\nBV\tBVT\nBR\tBRA\nVG\tVGB\nIO\tIOT\nBN\tBRN\nBG\tBGR\nBF\tBFA\nBI\tBDI\nKH\tKHM\nCM\tCMR\nCA\tCAN\nCV\tCPV\nKY\tCYM\nCF\tCAF\nTD\tTCD\nCL\tCHL\nCN\tCHN\nHK\tHKG\nMO\tMAC\nCX\tCXR\nCC\tCCK\nCO\tCOL\nKM\tCOM\nCG\tCOG\nCD\tCOD\nCK\tCOK\nCR\tCRI\nCI\tCIV\nHR\tHRV\nCU\tCUB\nCY\tCYP\nCZ\tCZE\nDK\tDNK\nDJ\tDJI\nDM\tDMA\nDO\tDOM\nEC\tECU\nEG\tEGY\nSV\tSLV\nGQ\tGNQ\nER\tERI\nEE\tEST\nET\tETH\nFK\tFLK\nFO\tFRO\nFJ\tFJI\nFI\tFIN\nFR\tFRA\nGF\tGUF\nPF\tPYF\nTF\tATF\nGA\tGAB\nGM\tGMB\nGE\tGEO\nDE\tDEU\nGH\tGHA\nGI\tGIB\nGR\tGRC\nGL\tGRL\nGD\tGRD\nGP\tGLP\nGU\tGUM\nGT\tGTM\nGG\tGGY\nGN\tGIN\nGW\tGNB\nGY\tGUY\nHT\tHTI\nHM\tHMD\nVA\tVAT\nHN\tHND\nHU\tHUN\nIS\tISL\nIN\tIND\nID\tIDN\nIR\tIRN\nIQ\tIRQ\nIE\tIRL\nIM\tIMN\nIL\tISR\nIT\tITA\nJM\tJAM\nJP\tJPN\nJE\tJEY\nJO\tJOR\nKZ\tKAZ\nKE\tKEN\nKI\tKIR\nKP\tPRK\nKR\tKOR\nKW\tKWT\nKG\tKGZ\nLA\tLAO\nLV\tLVA\nLB\tLBN\nLS\tLSO\nLR\tLBR\nLY\tLBY\nLI\tLIE\nLT\tLTU\nLU\tLUX\nMK\tMKD\nMG\tMDG\nMW\tMWI\nMY\tMYS\nMV\tMDV\nML\tMLI\nMT\tMLT\nMH\tMHL\nMQ\tMTQ\nMR\tMRT\nMU\tMUS\nYT\tMYT\nMX\tMEX\nFM\tFSM\nMD\tMDA\nMC\tMCO\nMN\tMNG\nME\tMNE\nMS\tMSR\nMA\tMAR\nMZ\tMOZ\nMM\tMMR\nNA\tNAM\nNR\tNRU\nNP\tNPL\nNL\tNLD\nAN\tANT\nNC\tNCL\nNZ\tNZL\nNI\tNIC\nNE\tNER\nNG\tNGA\nNU\tNIU\nNF\tNFK\nMP\tMNP\nNO\tNOR\nOM\tOMN\nPK\tPAK\nPW\tPLW\nPS\tPSE\nPA\tPAN\nPG\tPNG\nPY\tPRY\nPE\tPER\nPH\tPHL\nPN\tPCN\nPL\tPOL\nPT\tPRT\nPR\tPRI\nQA\tQAT\nRE\tREU\nRO\tROU\nRU\tRUS\nRW\tRWA\nBL\tBLM\nSH\tSHN\nKN\tKNA\nLC\tLCA\nMF\tMAF\nPM\tSPM\nVC\tVCT\nWS\tWSM\nSM\tSMR\nST\tSTP\nSA\tSAU\nSN\tSEN\nRS\tSRB\nSC\tSYC\nSL\tSLE\nSG\tSGP\nSK\tSVK\nSI\tSVN\nSB\tSLB\nSO\tSOM\nZA\tZAF\nGS\tSGS\nSS\tSSD\nES\tESP\nLK\tLKA\nSD\tSDN\nSR\tSUR\nSJ\tSJM\nSZ\tSWZ\nSE\tSWE\nCH\tCHE\nSY\tSYR\nTW\tTWN\nTJ\tTJK\nTZ\tTZA\nTH\tTHA\nTL\tTLS\nTG\tTGO\nTK\tTKL\nTO\tTON\nTT\tTTO\nTN\tTUN\nTR\tTUR\nTM\tTKM\nTC\tTCA\nTV\tTUV\nUG\tUGA\nUA\tUKR\nAE\tARE\nGB\tGBR\nUS\tUSA\nUM\tUMI\nUY\tURY\nUZ\tUZB\nVU\tVUT\nVE\tVEN\nVN\tVNM\nVI\tVIR\nWF\tWLF\nEH\tESH\nYE\tYEM\nZM\tZMB\nZW\tZWE "
        for s in Utils.splitString(table, '\n', False): 
            ss = s.strip()
            if ((len(ss) < 6) or not Utils.isWhitespace(ss[2])): 
                continue
            cod2 = ss[0:0+2]
            cod3 = ss[3:].strip()
            if (len(cod3) != 3): 
                continue
            if (not cod2 in MiscLocationHelper._m_alpha2_3): 
                MiscLocationHelper._m_alpha2_3[cod2] = cod3
            if (not cod3 in MiscLocationHelper._m_alpha3_2): 
                MiscLocationHelper._m_alpha3_2[cod3] = cod2
    
    __m_nords = None
    
    _m_alpha2_3 = None
    
    _m_alpha3_2 = None
    
    @staticmethod
    def _deflate(zip0_ : bytearray) -> bytearray:
        with io.BytesIO() as unzip: 
            data = io.BytesIO(zip0_)
            data.seek(0, io.SEEK_SET)
            MorphSerializeHelper.deflateGzip(data, unzip)
            data.close()
            return bytearray(unzip.getvalue())
    
    # static constructor for class MiscLocationHelper
    @staticmethod
    def _static_ctor():
        MiscLocationHelper.__m_geo_ref_by_name = dict()
        MiscLocationHelper._m_alpha2_3 = dict()
        MiscLocationHelper._m_alpha3_2 = dict()

MiscLocationHelper._static_ctor()