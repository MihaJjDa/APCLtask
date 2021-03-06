﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.core.Termin import Termin
from pullenti.ner.instrument.InstrumentArtefact import InstrumentArtefact
from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.instrument.internal.MetaInstrumentBlock import MetaInstrumentBlock
from pullenti.ner.instrument.InstrumentBlockReferent import InstrumentBlockReferent
from pullenti.ner.instrument.internal.InstrToken import InstrToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.instrument.internal.InstrumentArtefactMeta import InstrumentArtefactMeta
from pullenti.ner.instrument.internal.MetaInstrument import MetaInstrument
from pullenti.ner.instrument.InstrumentParticipant import InstrumentParticipant
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.instrument.internal.InstrumentParticipantMeta import InstrumentParticipantMeta
from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent

class InstrumentAnalyzer(Analyzer):
    """ Анализатор структуры нормативных актов и договоров """
    
    @property
    def name(self) -> str:
        return InstrumentAnalyzer.ANALYZER_NAME
    
    ANALYZER_NAME = "INSTRUMENT"
    
    @property
    def caption(self) -> str:
        return "Структура нормативно-правовых документов (НПА)"
    
    @property
    def description(self) -> str:
        return "Разбор структуры НПА на разделы и подразделы"
    
    def clone(self) -> 'Analyzer':
        return InstrumentAnalyzer()
    
    @property
    def is_specific(self) -> bool:
        """ Этот анализатор является специфическим """
        return True
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaInstrument.GLOBAL_META, MetaInstrumentBlock.GLOBAL_META, InstrumentParticipantMeta.GLOBAL_META, InstrumentArtefactMeta.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaInstrument.DOC_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("decree.png")
        res[MetaInstrumentBlock.PART_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("part.png")
        res[InstrumentParticipantMeta.IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("participant.png")
        res[InstrumentArtefactMeta.IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("artefact.png")
        return res
    
    def createReferent(self, type0_ : str) -> 'Referent':
        if (type0_ == InstrumentReferent.OBJ_TYPENAME): 
            return InstrumentReferent()
        if (type0_ == InstrumentBlockReferent.OBJ_TYPENAME): 
            return InstrumentBlockReferent()
        if (type0_ == InstrumentParticipant.OBJ_TYPENAME): 
            return InstrumentParticipant()
        if (type0_ == InstrumentArtefact.OBJ_TYPENAME): 
            return InstrumentArtefact()
        return None
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.instrument.internal.FragToken import FragToken
        t = kit.first_token
        t1 = t
        if (t is None): 
            return
        dfr = FragToken.createDocument(t, 0, InstrumentKind.UNDEFINED)
        if (dfr is None): 
            return
        ad = kit.getAnalyzerData(self)
        res = dfr.createReferent(ad)
    
    __m_inited = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.instrument.internal.ParticipantToken import ParticipantToken
        if (InstrumentAnalyzer.__m_inited): 
            return
        InstrumentAnalyzer.__m_inited = True
        InstrumentArtefactMeta.initialize()
        MetaInstrumentBlock.initialize()
        MetaInstrument.initialize()
        InstrumentParticipantMeta.initialize()
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            InstrToken.initialize()
            ParticipantToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.registerAnalyzer(InstrumentAnalyzer())